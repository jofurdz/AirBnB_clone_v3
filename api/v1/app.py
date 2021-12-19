#!/usr.bin/python3
"""sets up flask"""

from flask import Flask

app = Flask(__name__)

@app.teardown_appcontext
def teardown_DB(context):
    storage.close()

if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port="5000")
