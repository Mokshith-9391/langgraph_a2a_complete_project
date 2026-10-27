install:
	python -m pip install -r requirements.txt

research:
	uvicorn agents.research_agent:app --host 0.0.0.0 --port 8001

writer:
	uvicorn agents.writer_agent:app --host 0.0.0.0 --port 8002

supervisor:
	uvicorn supervisor.app:app --host 0.0.0.0 --port 8000

docker:
	docker compose up --build

test:
	pytest -q
