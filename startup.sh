#!/bin/bash

gunicorn yo_parser_bot:app --bind 0.0.0.0:8001 --worker-class uvicorn.workers.UvicornWorker
