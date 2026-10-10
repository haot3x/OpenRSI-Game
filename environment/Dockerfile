FROM mcr.microsoft.com/playwright/python:v1.62.0-noble@sha256:aa81288e738725378becba5b3e06cb0f3a7f012a610e87e8d767a090ea3f740d
WORKDIR /workspace/openrsi-game
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY task-source.tar.gz source-manifest.json /tmp/
RUN python -c "import hashlib,json,pathlib; p=pathlib.Path('/tmp/task-source.tar.gz'); assert hashlib.sha256(p.read_bytes()).hexdigest()==json.loads(pathlib.Path('/tmp/source-manifest.json').read_text())['archive_sha256']" \
    && tar -xzf /tmp/task-source.tar.gz -C /workspace/openrsi-game \
    && rm /tmp/task-source.tar.gz /tmp/source-manifest.json
# Judge-only tests are injected at /tests by RSI-Harness, not copied to Work.
