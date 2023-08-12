from setuptools import setup

setup(
    name='mypass-cli',
    version='1.0.0',
    description='CLI application for MyPass',
    author='ricky :) (: skyzip',
    license='MIT',
    packages=['mypass_cli'],
    package_dir={'mypass_cli': 'mypass'},
    install_requires=[
        'rich', 'click', 'click_shell', 'pyperclip'
    ],
)
