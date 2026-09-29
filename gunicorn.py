#!/usr/bin/env python3

import os

this_dir = os.path.dirname(os.path.realpath(__file__))
app = "faxthesystem"

command = f"{this_dir}/venv/bin/gunicorn"
pythonpath = f"{this_dir}/"
workers = 4
user = app
bind = f"unix:{this_dir}/sock"
pid = f"{this_dir}/pid"
errorlog = "{this_dir}/error.log"
accesslog = "{this_dir}/access.log"
access_log_format = '%({X-Real-IP}i)s %({X-Forwarded-For}i)s %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = "warning"
capture_output = True
