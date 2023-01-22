THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help migrate
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
migrate_and_run:
	alembic upgrade head
	uvicorn main:app --host 0.0.0.0
