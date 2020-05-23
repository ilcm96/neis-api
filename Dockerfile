FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN pip install --no-cache-dir fastapi rejson aiohttp requests regex

COPY ./main.py /app/ && ./schoolcode.py /app/ && ./schoolmeal.py /app/
