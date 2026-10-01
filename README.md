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

For the front-end:
- The `gunicorn.py` conf can be used to run gunicorn in a systemd service with something along the lines of `ExecStart=/var/www/faxthesystem/venv/bin/gunicorn -c /var/www/faxthesystem/gunicorn.py wsgi:app`

For the print daemon:
- TODO 🙃
