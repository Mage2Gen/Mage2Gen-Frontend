import uuid
import collections

# import mage2gen
# import mage2gen.snippets
# from mage2gen import Snippet
# from mage2gen.license import GPLV3, OSLV3, License
from django.db import models
from jsonfield import JSONField
from django.conf import settings
from . import utils


class BaseModel(models.Model):
	"""Base model for all Merlin models"""
	
	created_at = models.DateTimeField(auto_now_add=True)
	"""Created at field, date is set when model is created"""

	updated_at = models.DateTimeField(auto_now=True)
	"""Update at field, date is set when model is saved"""

	class Meta:
		abstract = True


class Module(BaseModel):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modules', null=True, blank=True, on_delete=models.SET_NULL)
	config = JSONField(default={}, load_kwargs={'object_pairs_hook': collections.OrderedDict})
	package_name = models.CharField(max_length=128, default='')
	name = models.CharField(max_length=128, default='')
	download_count = models.IntegerField(default=0)

	def load_by_config(self, config=None):
		# prevent import loop
		from apps.account.models import License as LicenseModel
		if not config:
			config = self.config

		if not config:
			raise Exception('No config to load Module')

		main_version = config.get('magento_version', '3')

		desc = config['description'] if 'description' in config else ''

		module = utils.create_module(main_version, config['package_name'], config['module_name'], desc)
		license_desc = desc if desc else 'A Magento 2 module named {}/{}'.format(module.package, module.name)

		if self.user:
			module._composer['authors'].append({
				'name': self.user.first_name + ' ' + self.user.last_name,
				'email': self.user.email
			})

		fallback_license = utils.create_license(main_version, 'GPLV3',
												copyright=config.get('copyright'),
												module_name='{}/{}'.format(module.package, module.name),
												description=license_desc)
		if config.get('license') == 'custom':
			license_model, _ = LicenseModel.objects.get_or_create(user=self.user)

			if license_model.license_short_text and license_model.license_text:
				module.license = utils.create_license(main_version, 'License',
													  copyright=config.get('copyright'),
													  module_name='{}/{}'.format(module.package, module.name),
													  description=license_desc,
													  license_text=license_model.license_text,
													  short_license_text=license_model.license_short_text)
			else:
				module.license = fallback_license
		elif config.get('license') in ('gplv3', 'oslv3', 'apache2', 'mit'):
			module.license = utils.create_license(main_version, config.get('license').upper(),
						  copyright=config.get('copyright'),
						  module_name='{}/{}'.format(module.package, module.name),
						  description=license_desc)

		# add snippets
		snippets = {}
		for SnippetClass in utils.get_snippets(main_version, 'skip'):
			snippets[SnippetClass.name()] = SnippetClass

		for snippet_name, kwargss in config.get('snippets', {}).items():
			SnippetClass = snippets.get(snippet_name)
			if SnippetClass:
				snippet_object = SnippetClass(module)
				for index, kwargs in enumerate(kwargss):
					if index >= 100: # prevent huge modules
						break
					snippet_object.add(**kwargs)

		return module
