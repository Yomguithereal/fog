from setuptools import setup, find_packages

with open('./README.md', 'r') as f:
    long_description = f.read()

setup(name='fog',
      version='0.1.1',
      description='A fuzzy matching & clustering library for python.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/Yomguithereal/fog',
      license='MIT',
      author='Guillaume Plique',
      author_email='kropotkinepiotr@gmail.com',
      keywords='fuzzy',
      python_requires='>=3',
      packages=find_packages(exclude=['test']),
      package_data={'docs': ['README.md']},
      zip_safe=True)
