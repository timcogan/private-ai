PYTHON=python3
SRC=src

run:
	${PYTHON} ${SRC}/main.py

init:
	bash ${SRC}/setup.sh

run-msg:
	${PYTHON} ${SRC}/message.py

run-ai:
	${PYTHON} ${SRC}/ai.py

clean:
	rm -f config.json
	rm -rf tools

test:
	${PYTHON} -m pytest tests -s --cov=./${SRC}
