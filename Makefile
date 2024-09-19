.PHONY: run run_python tests dependencies

PID_FILE=python_process.pid

run: dependencies
	python3 main.py

tests: 
	python3 integration_tests.py

dependencies:
	pip install -r requirements.txt