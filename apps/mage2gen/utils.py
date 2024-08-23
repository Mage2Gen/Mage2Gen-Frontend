import os
import random
import string
import shutil
import importlib

from django.conf import settings


def random_string(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def tmp_dir(path=''):
    return os.path.join(settings.TMP_DIR, path.lstrip('/'))


def random_tmp_path():
    return os.path.join(settings.TMP_DIR, random_string(32))


def tmp_remove(path):
    if len(path) > len(tmp_dir()) and tmp_dir() == path[:len(tmp_dir())]:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def remove_folder(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def get_module_name(version=None):
    return 'mage2gen{}'.format(version) if version else 'mage2gen'


def create_module(version=None, *args, **kwargs):
    mage2gen = importlib.import_module(get_module_name(version))
    return mage2gen.Module(*args, **kwargs)


def create_license(version, license, *args, **kwargs):
    License = getattr(importlib.import_module('{}.license'.format(get_module_name(version))), license)
    return License(*args, **kwargs)


def get_snippets(version=None, request=None):
    module = importlib.import_module(get_module_name(version))
    snippets = module.Snippet.snippets()
    if request != None:
        ip = False
        if isinstance(request, str) == False:
            if 'HTTP_CLIENT_IP' in request.META:
                ip = request.META['HTTP_CLIENT_IP']
            elif 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            elif 'REMOTE_ADDR' in request.META:
                ip = request.META['REMOTE_ADDR']
        if request == 'skip' or (ip != False and (ip == '157.97.119.14' or ip == '127.0.0.1' or ip == '136.144.135.125' or ip == '161.51.68.158')):
            try:
                module = importlib.import_module('experius')
                snippets = snippets + module.Snippet.snippets()
            except:
                return snippets

    return snippets


def get_magento_versions():
    versions = []
    for version in range(3, 25):
        try:
            importlib.import_module(get_module_name(version))
            versions.append(version)
        except:
            break
    return versions
