FROM python:3.10.12
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "127.0.0.2:8000"]