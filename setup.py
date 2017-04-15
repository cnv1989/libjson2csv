from setuptools import setup, find_packages
setup(
    name='json2csv',
    version='0.0.1',
    description='Converts nested json object to csv and csv back to json',
    author='Nag Varun Chunduru',
    author_email='cnv1989@gmail.com',
    long_description=(
        open('README.md').read() + '\n\n' +
        open('CHANGELOG.md').read()),
    url='https://github.com/cnv1989/json2csv',  # use the URL to the github repo
    # I'll explain this in a second
    download_url='https://github.com/cnv1989/json2csv/archive/v0.0.1.tar.gz',
    keywords=['json', 'csv', 'converter'],  # arbitrary keywords
    classifiers=[],
    package_dir={'': 'src'},
    packages=find_packages('src'),
)
