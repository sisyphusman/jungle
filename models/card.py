from models.database import cards_collection
from flask import Blueprint, jsonify, request

card_bp = Blueprint('card', __name__)


def get_cards(page):
    per_page = 12
    skip_count = (page - 1) * per_page
    cards_cursor = cards_collection.find().skip(skip_count).limit(per_page)

    cards = []
    for card in cards_cursor:
        cards.append({
            "img": card.get("img", ""),
            "title": card.get("title", ""),
            "author": card.get("author", ""),
            "tag_list": card.get("tag_list", []),
            "date": card.get("date", ""),
            "likes": card.get("likes", 0)
        })
    return cards


@card_bp.route("/load_cards")
def load_cards():
    page = int(request.args.get("page", 1))
    cards = get_cards(page)
    return jsonify({"result": "success", "cards": cards})
