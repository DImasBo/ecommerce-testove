FROM python:3.9

WORKDIR /app/

COPY ./app /app
ENV PYTHONPATH=/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install libary
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888"]
