from src.main import app
import os

if __name__ == "__main__":
    port = os.environ.get("PORT",5000)
    app.run(debug=False,host="0.0.0.0",port=port)
    # socket_.run(app,debug=True)
#$