from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='site_parser',
    version='0.1.3',
    author='Alexander Dubrovin',
    author_email='da070116@gmail.com',
    description='A Python site source application',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/da070116/site_parser',
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GPL v.3",
                 "Operating System :: OS Independent", ],
    python_requires='>=3.7',
)
