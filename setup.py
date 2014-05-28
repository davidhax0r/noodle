from setuptools import setup

setup(
    name='noodle',
    version='0.2',
    py_modules=['noodle'],
    description='A stupid command-line soundcloud track downloader with puns',
    url='http://github.com/itsnauman/noodle',
    author='Nauman Ahmad',
    author_email='nauman-ahmad@outlook.com',
    license='MIT',
    include_package_data=True,
    install_requires=[
        'requests',
        'soundcloud',
        'termcolor',
    ],
    entry_points='''
        [console_scripts]
        noodle=noodle:downloader
    ''',
)
