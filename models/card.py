from datetime import datetime
from bson import ObjectId
from models.database import cards_collection
from flask import Blueprint, jsonify, request
from utils.auth_required import auth_required
from utils.bs4_crawler import fetch_thumbnail
from models.user import find_user_by_id
from models.user import find_user_by_name

from utils.slack_helper import create_dm_conversation


card_bp = Blueprint('card', __name__)


def search_card(keyword):
    try:
        query = {
            "$or": [
                {"tag_list": {"$regex": keyword, "$options": "i"}},
                {"title": {"$regex": keyword, "$options": "i"}}
            ]
        }

        cards_cursor = cards_collection.find(query)

        cards = []
        for card in cards_cursor:
            cards.append({
                "_id": str(card.get("_id")),
                "img": card.get("img", ""),
                "title": card.get("title", ""),
                "author": card.get("author", ""),
                "tag_list": card.get("tag_list", []),
                "date": card.get("date", ""),
                "likes": card.get("likes", 0),
                "url": card.get("url", "")

            })
            print(str(card.get("_id")))

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
            "_id": str(card.get("_id")),
            "img": card.get("img", ""),
            "title": card.get("title", ""),
            "author": card.get("author", ""),
            "tag_list": card.get("tag_list", []),
            "date": card.get("date", ""),
            "likes": card.get("likes", 0),
            "url": card.get("url", "")
        })
        print(str(card.get("_id")))
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
    today = datetime.today()
    date_str = today.strftime("%Y-%m-%d")

    user_id = ObjectId(current_user['id'])
    user = find_user_by_id(user_id)
    if not user:
        return jsonify({
            "success": False,
            "message": "Fail: 사용자를 찾을 수 없음"
        }), 404

    card_data = {
        "author_id": user_id,
        "title": title,
        "author": author_name,
        "img": img,
        "tag_list": tag_list,
        "date": date_str,
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


@card_bp.route("/like_card/<card_id>", methods=['POST'])
@auth_required
def like_card(current_user, card_id):
    try:
        result = cards_collection.update_one(
            {"_id": ObjectId(card_id)},
            {"$inc": {"likes": 1}}
        )
        if result.matched_count == 0:
            return jsonify({"success": False, "message": "카드를 찾을 수 없습니다."}),
        404

        # 업데이트 후 현재 좋아요 수 반환
        card = cards_collection.find_one({"_id": ObjectId(card_id)})
        return jsonify({
            "success": True,
            "message": "좋아요 추가 성공!",
            "likes": card["likes"]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"좋아요 추가 실패: {str(e)}"
        }), 500


@card_bp.route("/create-dm", methods=['POST'])
@auth_required
def create_dm_conversation_route(current_user):
    """질문하기 버튼 클릭 시 DM 채널 생성"""
    try:
        # 1. 요청 데이터 파싱
        data = request.get_json()
        card_id = data.get('card_id')
        author_name = data.get('author_name')  # 변경: author_id → author_name

        print(
            f"[DEBUG] DM 생성 요청: card_id={card_id}, author_name={author_name}")
        print(
            f"[DEBUG] 질문자: {current_user['name']} (ID: {current_user['id']})")

        # 2. 필수 데이터 검증
        if not card_id or not author_name:
            return jsonify({
                "success": False,
                "message": "카드 ID와 작성자 이름이 필요합니다."
            }), 400

        # 3. 작성자 정보 조회 (변경: find_user_by_id → find_user_by_name)
        author = find_user_by_name(author_name)
        if not author:
            return jsonify({
                "success": False,
                "message": f"작성자 '{author_name}'을 찾을 수 없습니다."
            }), 404

        print(f"[DEBUG] 작성자: {author['name']} (ID: {author['id']})")

        # 4. Slack ID 확인
        questioner_slack_id = current_user.get('slack_user_id')
        author_slack_id = author.get('slack_user_id')

        if not questioner_slack_id or not author_slack_id:
            return jsonify({
                "success": False,
                "message": "Slack 연동이 되지 않은 사용자입니다."
            }), 400

        print(
            f"[DEBUG] Slack IDs - 질문자: {questioner_slack_id}, 작성자: {author_slack_id}")

        # 5. 자기 자신에게 질문하는 경우 방지
        if questioner_slack_id == author_slack_id:
            return jsonify({
                "success": False,
                "message": "자신에게는 질문할 수 없습니다."
            }), 400

        # 6. Slack DM 채널 생성
        dm_result = create_dm_conversation(
            questioner_slack_id, author_slack_id)

        if dm_result['success']:
            return jsonify({
                "success": True,
                "message": "질문방이 생성되었습니다!",
                "channel_id": dm_result.get('channel_id')
            })
        else:
            return jsonify({
                "success": False,
                "message": f"DM 생성 실패: {dm_result['message']}"
            }), 500

    except Exception as e:
        print(f"[ERROR] DM 생성 중 오류: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"서버 오류: {str(e)}"
        }), 500
