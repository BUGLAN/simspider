from setuptools import setup, find_packages


setup(
    name='simper-spider',
    version='0.1.0',
    description='This is a simper spider framework',
    author='buglan',
    author_email='1831353087@qq.com',
    url='https://github.com/BUGLAN/simspider',
    packages=find_packages(),
    install_requires=['lxml', 'requests', 'cssselect']
)
