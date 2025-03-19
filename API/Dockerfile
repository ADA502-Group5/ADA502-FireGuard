FROM python:3.12 AS builder
WORKDIR /app 
COPY . .
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN /root/.local/bin/poetry install
RUN /root/.local/bin/poetry build


FROM python:3.12-alpine
RUN addgroup -g 1000 app
RUN adduser -G app -D -u 1000 -h /app app
WORKDIR /app
USER app
COPY --from=builder --chown=1000:1000 /app/dist .
RUN pip install locationreg-0.1.0-py3-none-any.whl
CMD ["python", "-m", "locationreg.main"]

