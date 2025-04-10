FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

ENV FLASK_APP=run.py
ENV FLASK_ENV=development

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
