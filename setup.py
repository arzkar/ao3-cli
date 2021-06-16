from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='ao3-cli',
    author='Arbaaz Laskar',
    author_email="arzkar.dev@gmail.com",
    description="A CLI to download from archiveofourown.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.1.2',
    license='MIT',
    url="https://github.com/arzkar/ao3-cli/",
    packages=find_packages(include=['ao3_cli', 'ao3_cli.*']),
    include_package_data=True,
    install_requires=[
        'click>=7.1.2',
        'rich>=10.3.0',
        'requests>=2.25.1',
        'loguru>=0.5.3',
        'tqdm>=4.60.0',
        'BeautifulSoup4>=4.9.3',
        'colorama>=0.4.4'
    ],
    entry_points='''
        [console_scripts]
        ao3_cli=ao3_cli.cli:run_cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
