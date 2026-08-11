FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

ENV TRANSPORT=streamable-http
ENV HOST=0.0.0.0

CMD ["fiverr-mcp-server"]
