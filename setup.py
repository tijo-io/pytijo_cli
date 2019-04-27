from setuptools import setup

from os import listdir
from os.path import isfile, join

#TEMPLATES_DIR='tijocli/templates'
#templates = ["{}/{}".format(TEMPLATES_DIR,f) for f in listdir(TEMPLATES_DIR) if isfile(join(TEMPLATES_DIR, f))]

setup(
    zip_safe=True,
    name='tijocli',
    version='0.1',
    author='Jon Castro',
    author_email='jon@tijo.io',
    packages=[
        'tijocli'
    ],
#    data_files=[(TEMPLATES_DIR, templates)],
    description='Tijo Command line interface',
    license='LICENSE',
    install_requires=[
        "click",
        "structifytext"
    ],
    entry_points={
        'console_scripts': [
            'tijo = tijocli.cli:main'
        ]
    }

)
