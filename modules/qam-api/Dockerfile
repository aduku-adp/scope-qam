ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim-bookworm

# Print logs immediately instead of buffering
ENV PYTHONUNBUFFERED=True \
    # Application
    APP_PATH=/app \
    APP_USER=uvicorn \
    APP_RUN=app \
    # Server
    PORT=8080 \
    MAIN=main

COPY requirements.txt $APP_PATH/

RUN echo "" \
    && useradd --system --shell /bin/true --home $APP_PATH $APP_USER \
    && python -m pip install --no-cache-dir -r $APP_PATH/requirements.txt \
    && rm -f $APP_PATH/requirements.txt

COPY src/ $APP_PATH/

EXPOSE $PORT
USER $APP_USER
WORKDIR $APP_PATH

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
