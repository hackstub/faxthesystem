Fax the system
==============

![](assets/faxthesystem.png)

This is a Flask app to allow people to send messages and image, that get sent to a queue, which is then printed on a thermal EPSON TM printer

The web front is separated from the printing backend, such that one part can be hosted from a different machine than the other. Typically the front end is exposed on the global internet, and the printing backend may be unavailable from time to time, and will fetch the queue when it gets back online. (They can also run on the same machine anway)

**NB: this is work in progress, paint is not dry !**

Developement
------------

For the web front-end:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements-front.txt
(cd assets && bash fetch_assets)
echo "SECRET=pikachu" > .env

# Then start the server with
flask run --debug
# And go to http://127.0.0.1:5000
```

For the print daemon:

```bash
python3 -m venv venv
source venv/bin/activate
# (You can have both things in the same venv as the front, just run this command to install the additional dependencies)
pip3 install -r requirements-print-daemon.txt

echo "SECRET=pikachu" > .env
python3 print-daemon.py
```

Production
----------

### Front end

systemd setup This assume that you did setup stuff in `/var/www/faxthesystem`

```bash
# Create the needed user and chown all the files
useradd faxthesystem
usermod -a -G lp faxthesystem
chown -R faxthesystem:faxthesystem /var/www/faxthesystem

# Copy the service conf
cp systemd.service /etc/systemd/system/faxthesystem.service

# Tweak the absolute path or other parameters if needed:
nano /etc/systemd/system/faxthesystem.service

systemctl daemon-reload
systemctl enable faxthesystem --now

# Check is is indeed running with
systemctl status faxthesystem
```

Then configure your reverse-proxy to `127.0.0.1:1312` or whatever the `bind` statement in `gunicorn.py` points to

If you're hosting the service on a sub-path (for example `https://foobar.tld/fax`) you may need to append this snippet to `gunicorn.py` : 

```
raw_env = [
    "SCRIPT_NAME=/fax"
]
```

### Print daemon

- TODO 🙃
