FROM python:3.13.0-slim-bookworm

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV FLASK_ENV=development
EXPOSE 5000
CMD ["python", "app.py"]
