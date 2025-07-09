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
                {"tag_list": keyword},
                {"title": {"$regex": keyword, "$options": "i"}}
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
        if request.method == "POST":
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

        elif request.method == "GET":
            page = int(request.args.get("page", 1))
            keyword = request.args.get("keyword", "").strip()

            if keyword:
                result = search_card(keyword)
                cards = result["cards"]

                per_page = 12
                start_idx = (page-1) * per_page
                end_idx = start_idx + per_page
                cards = cards[start_idx:end_idx]
            else:
                cards = get_cards(page)

            return jsonify({"result": "success", "cards": cards})

    except Exception as e:
        return jsonify({"result": "error", "message": f"서버 에러: {str(e)}"})


@card_bp.route("/post_card", methods=['POST'])
@auth_required
def post_card(current_user):
    data = request.get_json()
    title = data.get('til_title')
    til_url = data.get('til_url')
    tag_list = data.get('tag_list')

    if not title:
        return jsonify({
            "success": False,
            "message": "Fail: 제목을 입력해주세요"
        }), 400

    if not til_url:
        return jsonify({
            "success": False,
            "message": "Fail: 원본 링크를 등록해주세요"
        }), 400

    author_name = current_user.get('name', '익명')
    img = fetch_thumbnail(til_url)

    card_data = {
        "title": title,
        "author": author_name,
        "img": img,
        "tag_list": tag_list,
        "date": "2025-테스트",
        "likes": 0,
        "url": til_url,
    }

    try:
        result = cards_collection.insert_one(card_data)
        print("inserted id: ", result.inserted_id)
    except Exception as e:
        print("fail", str(e))
        return jsonify({
            "sucess": False,
            "message": "Fail: DB insert 오류"
        }), 500

    return jsonify({
        "success": True,
        "message": "Success: 카드 포스팅 성공!"
    })
