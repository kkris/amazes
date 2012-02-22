from distutils.core import setup

setup(
    name = 'amazes',
    version = '0.1alpha',
    author = 'Kristoffer Kleine (kris.kleine@yahoo.de)',
    url = 'http://github.com/kkris/amazes',
    package_dir = {'amazes': 'src/'},
    packages = ['amazes', 'amazes.generator', 'amazes.solver', 'amazes.ui'],
)
