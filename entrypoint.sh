#!/bin/bash

# gunicorn doesn't seem to work
#gunicorn --bind 0.0.0.0:8080 app:app

python app.py
