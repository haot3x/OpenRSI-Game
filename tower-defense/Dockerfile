FROM mcr.microsoft.com/playwright/python:v1.62.0-noble@sha256:aa81288e738725378becba5b3e06cb0f3a7f012a610e87e8d767a090ea3f740d
ENV PYTHONDONTWRITEBYTECODE=1 PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
WORKDIR /workspace/openrsi-game
COPY requirements.txt /tmp/requirements.txt
RUN /usr/bin/python3 -m pip install --no-cache-dir --break-system-packages -r /tmp/requirements.txt
COPY . .
