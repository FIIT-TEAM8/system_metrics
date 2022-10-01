from flask import Blueprint, request
from .recount import Counter


scraping_route = Blueprint("scraping", __name__, url_prefix="/scraping")

@scraping_route.route("/recount")
def recount():
    flag = Counter.run_recount()
    if flag == 0:
        return "Recount started", 202
    if flag == 1:
        return "Recount still running", 202
    if flag == 2:
        return "Recount finished!", 200
    
    else:
        return "Finished with exception :(", 500

@scraping_route.route("/update", methods=["POST"])
def update_daily():
    return "bruh"

