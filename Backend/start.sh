#!/usr/bin/env bash
service nginx start
gunicorn -w 3 --bind unix:resnal.sock -m 777 resanalDjango.wsgi