#!/bin/bash
echo `sudo apt install virtualenv`
echo `virtualenv --python=python3.5 myvenv`
echo `source myvenv/bin/activate`
echo `pip install -r requirements.txt`
echo `python manage.py migrate`
