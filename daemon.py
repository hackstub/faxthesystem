import os
import sys
import time
import requests
from dotenv import load_dotenv
from escpos.printer import Usb

load_dotenv()
SECRET = os.getenv("SECRET")
if not SECRET:
    print("You should define the shared SECRET inside the .env file. Eg. SECRET=foobar")
    sys.exit(1)

# FIXME : move to conf ?
ENDPOINT = "http://127.0.0.1:5000/pop"
QUERY_SLEEP = 10

# FIXME : move to conf ?
# Check lsusb to get these ids
p = Usb(0x04b8, 0x0e28)

# https://python-escpos.readthedocs.io/en/latest/api/escpos.html#escpos.escpos.Escpos.set

#        p.set(
#            align="center",
#            font="a",
#            bold=False,
#            underline=0,
#            width=1,
#            height=1,
#            density=9,
#            invert=False,
#            smooth=False,
#            flip=False,
#            double_width=False,
#            double_height=False,
#            custom_size=False,
#        )


def print_message(data):

    p.text("=" * 30 + "\n")
    p.text(f"Le : {data['date']}\n")
    p.text(f"De : {data['from']}\n")
    p.text("=" * 30 + "\n")
    text = data["text"]

    # FIXME : check block_text ?
    # https://python-escpos.readthedocs.io/en/latest/api/escpos.html#escpos.escpos.Escpos.block_text
    chunks = [text[i:i + 35] for i in range(0, len(text), 35)]
    for chunk in chunks:
        p.text(chunk + "\n")
    p.text("\n" * 8)


while True:

    try:
        r = requests.get(ENDPOINT, headers={"secret": SECRET}, timeout=30)

        print(r)

        assert r.status_code == 200, f"Uhoh, status code is {r.status_code}"

        data = r.json()
        print(data)
        assert isinstance(data, list), "Uhoh, data obtained from the server is not a list ?"
        assert all(isinstance(d, dict) for d in data), "Uhoh, data obtained from the server is not a list of dict ?"
    except Exception as e:
        print("Uhoh, failed to query the server  ?")
        import traceback
        traceback.print_exception(e)
    else:
        for d in data:
            print(d)
            try:
                assert isinstance(d, dict), f"Uhoh, data fetched is not a list of dict ?! Type: {type(d)}"
                assert "from" in d and isinstance(d["from"], str), "Uhoh, no 'from' info or it's not an str ?!"
                assert "text" in d and isinstance(d["text"], str), "Uhoh, no 'text' info or it's not an str ?!"
                assert "date" in d and isinstance(d["date"], str), "Uhoh, no 'date' info or it's not an str ?!"
                assert 3 <= len(d["from"]) <= 30, "Uhoh, 'from' length is too small or too high"
                assert 1 <= len(d["text"]) <= 500, "Uhoh, 'text' length is too small or too high"
            except Exception as e:
                print(f"Failed to validate data: {e}")
            else:
                try:
                    print_message(d)
                except Exception as e:
                    print(f"Failed to print message: {e}")
                    import traceback
                    traceback.print_exception(e)
                finally:
                    time.sleep(2)

    time.sleep(QUERY_SLEEP)
