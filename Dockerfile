FROM python:3.11

COPY . /api
WORKDIR /api

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app",  "--port", "8000"]