run:
	uvicorn app.main:app --reload

test-p1:
	curl -X POST http://127.0.0.1:8000/ingest/email -H "Content-Type: application/json" -d @tests/p1_exemplo.json | jq .priority

lint:
	python -m py_compile $(git ls-files '*.py')
