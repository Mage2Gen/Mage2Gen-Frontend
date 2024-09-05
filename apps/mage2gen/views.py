import os
import re
import io
import zipfile
import tarfile
import json
import inspect
import logging
from docutils.core import publish_parts

from django.core.cache import cache
from django_jsend import JsendView
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from django.templatetags.static import static
from django.utils.html import escape
from django.conf import settings

from . import utils
from .models import Module


logger = logging.getLogger(__name__)


class AboutView(TemplateView):
	template_name = 'about.html'


class CommandlineView(TemplateView):
	template_name = 'commandline.html'


class SnippetsView(TemplateView):
	template_name = 'snippets.html'

	def get_context_data(self, config_id=None, **kwargs):
		data = super().get_context_data(**kwargs)
		snippets = []
		magento_version = self.request.GET.get('main_version', '3')

		for snippet in utils.get_snippets(magento_version, self.request):
			try:
				desc = publish_parts(inspect.cleandoc(snippet.description), writer_name='html', 
					settings_overrides={'initial_header_level': 3})['html_body'] if snippet.description else ''
			except Exception:
				desc = ''
			
			snippets.append({
				'name': snippet.name(),
				'description': desc,
				'label': snippet.label()
				})
		snippets = sorted(snippets, key=lambda k: k['name'])

		data['snippets'] = snippets

		return data


class SnippetView(TemplateView):
	template_name = 'snippet.html'

	def get_context_data(self, snippet_name=None, **kwargs):
		data = super().get_context_data(**kwargs)
		magento_version = self.request.GET.get('main_version', '3')

		for snippet in utils.get_snippets(magento_version, self.request):
			if snippet.name().lower() == snippet_name.lower():
				try:
					desc = publish_parts(inspect.cleandoc(snippet.description), writer_name='html',
						settings_overrides={'initial_header_level': 2,})['html_body'] if snippet.description else ''
				except Exception:
					desc = ''

				# Generate files
				cache_key = 'snippet_files_{}'.format(snippet.name())
				file_contents = cache.get(cache_key)
				if not file_contents:
					try:
						params = {}
						for param in snippet.params():
							if param.required and not param.default:
								params[param.name] = 'Test'

						config = {
							'package_name': 'Mage2Gen',
							'module_name': 'Module',
							'snippets': {
								snippet.name(): [params]
							}
						}

						module = Module().load_by_config(config)

						temp_path = utils.random_tmp_path()	
						try:
							os.makedirs(temp_path)
						except Exception:
							pass

						try:
							module.generate_module(temp_path)
						except Exception as e:
							logger.exception(e)
							utils.tmp_remove(temp_path)

						file_contents = []
						re_dirname = re.compile(r'^{}/{}/{}(.*)'.format(temp_path, module.package, module.name))
						for dirName, subdirList, fileList in os.walk(temp_path):
							match = re_dirname.match(dirName)
							if match and match.group(1):
								path =  '/'.join(match.group(1).split('/'))
								for fname in fileList:
									full_file_path = os.path.join(dirName, fname)
									module_path = os.path.join(path, fname).lstrip('/')
									if module_path in ['composer.json', 'registration.php', 'etc/module.xml']:
										continue
									with open(full_file_path, 'rb') as mfile:
										file_contents.append([
											module_path,
											escape(mfile.read().decode('utf-8'))
											])

						utils.tmp_remove(temp_path)
						cache.set(cache_key, file_contents, 60*60*24)
					except Exception as e:
						logger.exception(e)

				data['snippet'] = {
					'name': snippet.name(),
					'description': desc,
					'files': file_contents,
				}
				break

		return data


class Mage2GenView(TemplateView):
	template_name = 'parts/module_generate.html'

	def get_context_data(self, config_id=None, **kwargs):
		data = super().get_context_data(**kwargs)
		snippets = []
		magento_version = self.request.GET.get('main_version', '4')

		try:
			if not config_id:
				config_id = self.request.COOKIES.get('mage2gen_module_id')
			module = Module.objects.get(id=config_id)
			config = module.config
		except Exception as e:
			config = None

		for snippet in utils.get_snippets(magento_version, self.request):
			try:
				desc = publish_parts(inspect.cleandoc(snippet.description), writer_name='html', 
					settings_overrides={'initial_header_level': 5,})['html_body'] if snippet.description else ''
			except Exception:
				desc = ''
			
			extra_params = []
			for param in snippet.extra_params():
				if not isinstance(param, str):
					param_dict = param.__dict__
					param_dict['name'] = "__extra__{}".format(param_dict['name'])
					extra_params.append(param_dict)
				else:
					extra_params.append(param)
			snippets.append({
				'name': snippet.name(),
				'label': snippet.label(),
				'description': desc,
				'params': list(param.__dict__ for param in snippet.params()),
				'extra_params': extra_params,
				})
		snippets = sorted(snippets, key=lambda k: k['name'])
		
		try:
			data['snippets'] = json.dumps(snippets)
		except Exception:
			data['snippets'] = json.dumps([])

		data.update({
			'config': json.dumps(config) if config else None,
			'selected_version': magento_version,
			'versions': utils.get_magento_versions(),
		})
		
		return data


class SaveModuleJsendView(JsendView):

	def handle_request(self, request, config_id=None):
		try:
			module = Module.objects.get(id=config_id)
		except Exception:
			module = Module()

		try:
			data = json.loads(self.request.POST.get('mage2gen-data'))
		except Exception:
			raise Exception('Data is not valid json')

		if not data['package_name'] or not data['module_name']:
			raise Exception('package_name and/or module_name is missing in config')

		if not module.user and request.user.is_authenticated:
			module.user = request.user
		module.package_name = data['package_name']
		module.name = data['module_name']
		module.config = data
		module.save()

		if settings.MODULE_GENERATION_PATH:
			
			mage2gen_module = Module().load_by_config(data)

			module_path = '{}/{}/'.format(settings.MODULE_GENERATION_PATH, mage2gen_module.package)
			try:
				utils.remove_folder(module_path)
			except Exception:
				pass

			try:
				mage2gen_module.generate_module(settings.MODULE_GENERATION_PATH)
			except Exception as e:
				logger.exception(e)

		return str(module.id)

class UserModulesJsendView(JsendView):

	def handle_request(self, request):
		if not request.user.is_authenticated:
			raise Exception('Not logged in')

		modules = []
		for module in Module.objects.filter(user=request.user).order_by('-created_at'):
			modules.append({
				'id': str(module.id),
				'package_name': module.package_name,
				'name': module.name,
				'config': module.config,
				})

		return modules


class DownloadModule(View):

	def get(self, request, config_id, extension, download_type='module'):
		try:
			module = Module.objects.get(id=config_id)
		except Exception:
			return HttpResponse("Module does not exists")

		if extension not in ['zip', 'tar']:
			return HttpResponse("Only zip or tar is supported")

		try:
			module.download_count += 1
			module.save()
		except Exception:
			pass

		config = module.config
		module = module.load_by_config()

		# generate module
		temp_path = utils.random_tmp_path()	
		try:
			os.makedirs(temp_path)
		except Exception:
			pass
		
		try:
			module.generate_module(temp_path)
		except Exception as e:
			utils.tmp_remove(temp_path)
			return HttpResponse("Error generating module: {}".format(e))
		
		stream_file = io.BytesIO()

		if extension == 'zip':
			content_type = 'application/x-zip-compressed'
			re_path_comp = re.compile(temp_path.rstrip('/') + '/(.*)')
			def zipdir(path, ziph):
				# ziph is zipfile handle
				for root, dirs, files in os.walk(path):
					for file in files:
						path = os.path.join(root, file)
						re_filename = re.compile(r'^{}/{}/{}/((src)/(.*))'.format(temp_path, module.package, module.name))
						match = re_filename.match(path)
						if not match and download_type == 'module':
							rel_path = re_path_comp.match(path).group(1)
							ziph.write(path, rel_path)
			zipf = zipfile.ZipFile(stream_file, 'w', zipfile.ZIP_DEFLATED)
			zipdir(temp_path, zipf)
			zipf.close()
		else:
			content_type = 'application/x-gzip'
			re_path_comp = re.compile(temp_path.rstrip('/') + '/(.*)')
			with tarfile.open(fileobj=stream_file, mode="w:gz") as tar:
				for root, _, files in os.walk(temp_path):
					for f in files:
						path = os.path.join(root, f)
						re_filename = re.compile(r'^{}/{}/{}/((src)/(.*))'.format(temp_path, module.package, module.name))
						match = re_filename.match(path)
						if not match and download_type == 'module':
							rel_path = re_path_comp.match(path).group(1)
							tar.add(path, rel_path)

		utils.tmp_remove(temp_path)

		response = HttpResponse(stream_file.getvalue(), content_type=content_type)
		response['Content-Disposition'] = 'attachment; filename={}.{}'.format(module.module_name, extension)
		return response


class ModuleFileStructureJsendView(JsendView):

	def handle_request(self, request, config_id=None):
		try:
			data = json.loads(self.request.POST.get('mage2gen-data'))
		except Exception:
			raise Exception('Data is not valid json')

		if not data['package_name'] or not data['module_name']:
			raise Exception('package_name and/or module_name is missing in config')

		user = None
		if request.user.is_authenticated:
			user = request.user
		module = Module(user=user).load_by_config(data)


		# generate module
		temp_path = utils.random_tmp_path()
		try:
			os.makedirs(temp_path)
		except Exception:
			pass

		try:
			module.generate_module(temp_path)
		except Exception as e:
			logger.exception(e)
			utils.tmp_remove(temp_path)
			raise e
		jstree = []
		file_contents = {}
		re_dirname = re.compile(r'^{}/{}/(.*)'.format(temp_path, module.package))
		for dirName, subdirList, fileList in os.walk(temp_path):
			match = re_dirname.match(dirName)
			if match:
				dir_list = match.group(1).split('/')
				dir_id = '_'.join(dir_list)
				src_dir_id = '{}-src'.format(dir_id)
				parent_id = '_'.join(dir_list[:-1])
				name = dir_list[-1]
				if not parent_id:
					name = 'app/code/{}/{}'.format(module.package, module.name)
					parent_id = '#'

				icon = False
				if 'js' in dir_list:
					icon = static('img/folder-javascript.svg')
				elif 'layout' in dir_list or 'ui_component' in dir_list:
					icon = static('img/folder-layout.svg')
				elif 'view' in dir_list:
					icon = static('img/folder-views.svg')
				elif 'etc' in dir_list:
					icon = static('img/folder-src.svg')
				elif 'i18n' in dir_list:
					icon = static('img/folder-i18n.svg')

				icon_path = icon
				if 'src' not in dir_list or parent_id == '#':
					if not icon:
						icon_path = static('img/folder-php.svg')
					jstree.append({'id': dir_id, 'parent': parent_id, 'text': name, 'state': {'opened': 1 }, 'icon': icon_path})

				for fname in fileList:
					dir_path = dir_list[1:]
					file_path = fname
					if dir_path:
						file_path = '{}/{}'.format("/".join(dir_path), fname)

					full_file_path = os.path.join(dirName, fname)
					file_id = '{}_{}'.format(dir_id, fname)
					filename, file_extension = os.path.splitext(fname.lower())
					file_extension = file_extension.strip('.')
					icon = 'document.svg'
					if file_extension in ['php', 'xml', 'html', '.css', 'js', 'graphqls', 'json', 'graphql']:
						icon = '{}.svg'.format(file_extension)

					icon_path = icon = '{}/{}'.format(static('img'), icon)

					with open(full_file_path, 'rb') as mfile:
						file_contents[file_id] = escape(mfile.read().decode('utf-8'))

					jstree.append({'id': file_id, 'parent': dir_id, 'text': fname, 'path': file_path, 'icon': icon, 'state': {'opened': True }, 'file_content': 'some file content'})

		utils.tmp_remove(temp_path)

		# Save module
		try:
			mod = Module.objects.get(id=config_id)
			if mod.user and mod.user != request.user:
				mod = Module()
		except Exception as e:
			print(e)
			mod = Module()

		if request.user and request.user.is_authenticated:
			mod.user = request.user
		mod.package_name = data['package_name']
		mod.name = data['module_name']
		mod.config = data

		try:
			mod.save()
		except Exception:
			pass

		return {
			'module_id': str(mod.id),
			'jstree': jstree,
			'file_contents': file_contents,
		}
