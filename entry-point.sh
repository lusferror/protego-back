#!/bin/bash
flask db migrate
flask db upgrade
python /app/app.py