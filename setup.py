import os
from distutils.core import setup

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    path = os.path.realpath(path)
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package( dir ):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages

setup(name          = 'pluginmate',
      description   = 'Python plugin framework, that will be yours best mate',
      author        = 'Wojciech Danilo',
      author_email  = 'wojciech.danilo@gmail.com',
      version       = '0.1a',
      packages      = find_packages('.').keys(),
      #package_dir   = {'': 'pluginmate'},
#     py_modules    = ['pluginmate'],
)