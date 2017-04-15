from setuptools import setup, find_packages
setup(
    name='json_to_csv',
    version='0.0.4',
    description='Converts nested json object to csv and csv back to json',
    author='Nag Varun Chunduru',
    author_email='cnv1989@gmail.com',
    long_description=(
        open('README.rst').read() + '\n\n' +
        open('CHANGELOG.rst').read()),
    url='https://github.com/cnv1989/json_to_csv',  # use the URL to the github repo
    # I'll explain this in a second
    download_url='https://github.com/cnv1989/json_to_csv/archive/v0.0.4.tar.gz',
    keywords=['json', 'csv', 'converter'],  # arbitrary keywords
    classifiers=[],
    package_dir={'': 'src'},
    packages=find_packages('src'),
)
