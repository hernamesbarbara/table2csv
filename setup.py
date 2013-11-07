from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='table2csv',
        version='0.1.2',
        description='Extract data from an HTML table and store results to a csv file.',
        long_description=readme(),
        keywords='Extract HTML tables csv data',
        url='https://github.com/hernamesbarbara/table2csv',
        author='Austin Ogilvie',
        author_email='a@yhathq.com',
        license='MIT',
        packages=['table2csv'],
        install_requires = [
            'pandas',
            'requests',
            'beautifulsoup4',
            'docopt'
        ],
        include_package_data=True,
        zip_safe=False,
        entry_points = {
            'console_scripts': ['table2csv=table2csv.command_line:main'],
        }
    )
