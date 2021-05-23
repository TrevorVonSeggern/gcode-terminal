.PHONY: install run test

install:
	pip3 install -r requirements.txt

clean:
	rm -rf __pycache__

run:
	@./src/main.py

test:
	python3 -m unittest discover .
