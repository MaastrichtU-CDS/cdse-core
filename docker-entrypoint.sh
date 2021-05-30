#!/bin/bash
python manage.py migrate && gunicorn core.wsgi -b 0.0.0.0:8000