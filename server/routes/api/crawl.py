from flask import Blueprint, jsonify
from server.crawl import crawl

router = Blueprint('crawl', __name__, url_prefix="/api")

@router.route("/crawl")
def crawl_route():
    crawl()

    return jsonify({
        "ok": True
    })
