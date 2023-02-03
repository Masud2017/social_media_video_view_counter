from src.main import app
from src.main import socket_

import os

if __name__ == "__main__":
    port = os.environ.get("PORT",5000)
    socket_.run(app,debug=False,host="0.0.0.0",port=port)
#$