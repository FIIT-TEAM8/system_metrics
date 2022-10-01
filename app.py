import os
if os.path.exists("./.env"):
    from dotenv import load_dotenv
    load_dotenv()
from flask import Flask
from targets.scraping.routes import scraping_route

app = Flask(__name__)

app.register_blueprint(scraping_route, name="scraping_route")


@app.route("/")
def root():
    return "pes haf", 200

if __name__ == "__main__":
    app.run()