bootstrap:
	pip install -e .
	pip install "file://`pwd`#egg=pkobfusticator[tests]"

test:
	py.test tests.py -q --cov src/

.PHONY: bootstrap test
