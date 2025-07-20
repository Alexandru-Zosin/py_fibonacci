# ---------- single-stage image ----------
FROM python:3.11-slim

# OS packages needed by cx_Oracle
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libaio1 && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------
#  Layers that seldom change (keeps rebuilds fast)
# ------------------------------------------------------------------------
WORKDIR /usr/src/app
COPY app/Pipfile app/Pipfile.lock ./
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --system     
# installs your deps **and gunicorn**

# ------------------------------------------------------------------------
#  Your source code – keep it as a *package*
# ------------------------------------------------------------------------
COPY ./app ./app            
# <-- now /usr/src/app/app/__init__.py exists

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
# --chdir app adds /usr/src/app/app to PYTHONPATH, so imports resolve
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.Controller.app:app"]
