from setuptools import find_packages, setup

import kha


def read(f):
    return open(f, 'r', encoding='utf-8').read()


with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()


setup(
    name='kha-cli',
    version=kha.__version__,
    py_modules=['kha-cli'],
    description='kha',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='khahux',
    author_email='khahux@gmail.com',
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points='''
        [console_scripts]
        kha=kha.cli:cli
    '''
)
