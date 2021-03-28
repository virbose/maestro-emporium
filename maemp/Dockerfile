FROM python:3.8-slim

# Set working dir
WORKDIR /app/maemp

# Upgrade pip
RUN pip install --upgrade pip

# Set some env vars
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE maemp.settings

# Install requirements
COPY requirements.txt /app/maemp
RUN python -m pip install -r requirements.txt