SETUP = python setup.py

clean:
	# Delete all .pyc and .pyo files.
	find . \( -name "*~" -o -name "*.py[co]" -o -name ".#*" -o -name "#*#" \) -exec rm '{}' +
	rm -rf build
	rm -rf dist


build:
	${SETUP} sdist
	${SETUP} bdist_wheel

pip:
	twine upload dist/*