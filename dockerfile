# Use an official Python runtime as a parent image
FROM python:3.10-slim

WORKDIR /ideas-bucket-backend

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install git -y

RUN pip install -r requirements.txt

RUN pip install "git+https://github.com/openai/whisper.git"

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

EXPOSE 3001

# Define the command to run your application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]
