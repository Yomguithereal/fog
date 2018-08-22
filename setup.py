from setuptools import setup, find_packages
from Cython.Build import cythonize

with open('./README.md', 'r') as f:
    long_description = f.read()

setup(name='fog',
    version='0.5.2',
    description='A fuzzy matching & clustering library for python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/Yomguithereal/fog',
    license='MIT',
    author='Guillaume Plique',
    author_email='kropotkinepiotr@gmail.com',
    keywords='fuzzy',
    python_requires='>=3',
    packages=find_packages(exclude=['experiments', 'test']),
    ext_modules=cythonize('fog/metrics/*.pyx'),
    package_data={'': ['*.pyx'], 'docs': ['README.md']},
    install_requires=[
        'dill==0.2.7.1',
        'phylactery==0.1.1',
        'Unidecode==1.0.22'
    ],
    setup_requires=[
        'setuptools>=18.0',
        'cython'
    ],
    entry_points={
        'console_scripts': ['fog=fog.cli']
    },
    zip_safe=True)
