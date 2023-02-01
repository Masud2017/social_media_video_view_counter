from src.main import app
import os

if __name__ == "__main__":
    port = os.environment.get("PORT",5000)
    app.run(debug=False,host="0.0.0.0",port=port)
#$