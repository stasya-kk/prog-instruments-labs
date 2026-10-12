.PHONY: lint format format-check typecheck fullcheck test fulltest precommit run

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format . --check

typecheck:
	pyright .

fullcheck: lint format-check typecheck

test:
	pytest . -v

fulltest: fullcheck test

precommit:
	pre-commit install --hook-type pre-commit --hook-type pre-push

run:
	python lab1.py 