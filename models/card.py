from bson import datetime
from models.database import cards_collection
from flask import Blueprint, jsonify, request
from utils.auth_required import auth_required
from utils.bs4_crawler import fetch_thumbnail


card_bp = Blueprint('card', __name__)

def search_card(keyword):  
    try:
        query = {
            "$or": [
                { "tag_list": keyword },
                { "title": { "$regex": keyword, "$options": "i" } }
            ]
        }

        cards_cursor = cards_collection.find(query)

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

        return {
            "success": True,
            "cards": cards
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"카드 검색 실패: {str(e)}"
        }
    
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

@card_bp.route("/load_cards", methods=["POST", "GET"])
def load_cards():
    try:
        data = request.get_json()

        keyword = data.get("keyword", "").strip()

        if keyword:
            result = search_card(keyword)
            if result["success"]:
                return jsonify({"result": "success", "cards": result["cards"]})
            else:
                return jsonify({"result": "error", "message": result["message"]})
        else:
            return jsonify({"result": "error", "message": "검색어가 비어 있습니다."})

    except Exception as e:
        return jsonify({"result": "error", "message": f"서버 에러: {str(e)}"})
