from setuptools import setup, find_packages
from distutils.extension import Extension
import subprocess
import os
import os.path
import shutil
import platform

from pip._internal.utils.compatibility_tags import get_supported

wheel_tags = get_supported()[0]

system_type = platform.system()

license_text = b''
with open('LICENSE', 'rb') as fd:
    license_text = license_text + fd.read()
with open(os.path.join('licenses', 'LICENSE.append.txt'), 'rb') as fd:
    license_text = license_text + fd.read()
with open(os.path.join('pptk', 'LICENSE'), 'wb') as fd:
    fd.write(license_text)

def make_mod(x):
    if system_type == 'Windows':
        return x + '.pyd'
    elif system_type == 'Linux':
        return x + '.so'
    elif system_type == 'Darwin':
        return x + '.so'
    else:
        raise RuntimeError('Unknown system type %s', system_type)


def make_lib(x, version_suffix=''):
    if system_type == 'Windows':
        return x + '.dll'
    elif system_type == 'Linux':
        return 'lib' + x + '.so' + version_suffix
    elif system_type == 'Darwin':
        return 'lib' + x + '.dylib'
    else:
        raise RuntimeError('Unknown system type %s', system_type)


def make_exe(x):
    if system_type == 'Windows':
        return x + '.exe'
    else:
        return x


def list_libs():
    libs_dir = os.path.join('pptk', 'libs')
    exclude_list = ['Makefile', 'cmake_install.cmake']
    return [f for f in os.listdir(libs_dir)
            if os.path.isfile(os.path.join(libs_dir, f))
            and f not in exclude_list]


setup(
    name='pptk',
    version='0.1.1',
    description='A Python package for facilitating point cloud processing.',
    author='HERE Europe B.V.',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License'],
    license='MIT',
    install_requires=['numpy'],
    project_urls={
        'Source': 'https://github.com/heremaps/pptk'},
    packages=find_packages(),
    package_data={
        'pptk': [
            os.path.join('libs', f) for f in list_libs()] + [
            'LICENSE',
            os.path.join('libs',
                         'qt_plugins', 'platforms', make_lib('*', '*')),
            os.path.join('libs',
                         'qt_plugins', 'xcbglintegrations', make_lib('*', '*'))
            ],
        'pptk.kdtree': [make_mod('kdtree')],
        'pptk.processing.estimate_normals': [make_mod('estimate_normals')],
        'pptk.vfuncs': [make_mod('vfuncs')],
        'pptk.viewer': [make_exe('viewer'), 'qt.conf']},
    options={
        'bdist_wheel': {
            'python_tag': wheel_tags.interpreter,
            'plat_name': wheel_tags.platform,
        }
    }
)
