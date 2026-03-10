.PHONY: check format lint

check:
	@$(MAKE) --no-print-directory lint

format:
	@set -x; ruff format

lint:
	@set -x; ruff format --diff
	@set -x; ruff check
