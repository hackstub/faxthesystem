#!/usr/bin/env python3

import os

this_dir = os.path.dirname(os.path.realpath(__file__))
app = "faxthesystem"

command = f"{this_dir}/venv/bin/gunicorn"
pythonpath = f"{this_dir}/"
workers = 4
user = app
#bind = f"unix:{this_dir}/sock"
bind = "127.0.0.1:1312"
pid = f"{this_dir}/pid"
errorlog = f"{this_dir}/error.log"
accesslog = f"{this_dir}/access.log"
access_log_format = '%({X-Real-IP}i)s %({X-Forwarded-For}i)s %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = "warning"
capture_output = True
