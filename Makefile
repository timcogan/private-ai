PYTHON=python

run:
	${PYTHON} src/main.py

init:
	bash src/setup.sh

run-msg:
	${PYTHON} src/message.py

run-ai:
	${PYTHON} src/ai.py

clean:
	rm -f config.json
	rm -rf tools

test:
	pytest tests -s
