FROM python:3.11

COPY . /api
WORKDIR /api

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8000"]