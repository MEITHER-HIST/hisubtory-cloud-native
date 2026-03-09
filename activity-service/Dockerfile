FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY activity-service/requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt
RUN python manage.py collectstatic --noinput || true

# Copy shared apps from root context
COPY accounts/ ./accounts/
COPY stories/ ./stories/
COPY library/ ./library/
COPY pages/ ./pages/
COPY subway/ ./subway/
COPY supabase/ ./supabase/

# Copy service specific code
COPY activity-service/ .

ENV PYTHONPATH="/app"
CMD ["gunicorn", "--bind", "0.0.0.0:80", "project.wsgi:application"]
