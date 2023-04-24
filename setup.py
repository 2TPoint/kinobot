from setuptools import setup, find_packages

from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

name = 'kinobot'
version = '1.0.0'
release = '1.0.0'
setup(
    name=name,
    author='Fedor Shmakov, Nikolay Khorov, Ivan Demin',
    version=release,
    cmdclass=cmdclass,
    # these are optional and override conf.py settings
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'docs')}},
)

setup(
    name='kinobot',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'alabaster',
        'Babel',
        'beautifulsoup4',
        'CacheControl',
        'cachy',
        'certifi',
        'charset-normalizer',
        'cleo',
        'clikit',
        'colorama',
        'crashtest',
        'distlib',
        'docutils',
        'filelock',
        'future',
        'html5lib',
        'idna',
        'imagesize',
        'importlib-metadata',
        'importlib-resources',
        'Jinja2',
        'keyring',
        'kinopoiskpy',
        'lockfile',
        'lxml',
        'MarkupSafe',
        'msgpack',
        'packaging',
        'pastel',
        'pexpect',
        'pkginfo',
        'platformdirs',
        'poetry',
        'poetry-core',
        'ptyprocess',
        'Pygments',
        'pylev',
        'pyparsing',
        'pyTelegramBotAPI',
        'python-dateutil',
        'pytz',
        'pywin32-ctypes',
        'requests',
        'requests-toolbelt',
        'shellingham',
        'simplejson',
        'six',
        'snowballstemmer',
        'soupsieve',
        'Sphinx',
        'sphinxcontrib-applehelp',
        'sphinxcontrib-devhelp',
        'sphinxcontrib-htmlhelp',
        'sphinxcontrib-jsmath',
        'sphinxcontrib-qthelp',
        'sphinxcontrib-serializinghtml',
        'telebot',
        'tomlkit',
        'typing_extensions',
        'urllib3',
        'virtualenv',
        'webencodings',
        'zipp'
    ],
)