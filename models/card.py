from datetime import datetime
from bson import ObjectId
from models.database import cards_collection, db
from flask import Blueprint, jsonify, request
from utils.auth_required import auth_required
from utils.bs4_crawler import fetch_thumbnail
from models.user import find_user_by_id
from models.user import find_user_by_name
import validators
import requests

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


@card_bp.route("/validate_url", methods=['POST'])
def validate_url():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({
            "success": False,
            "message": "URL을 입력해주세요"
        }), 400

    if not validators.url(url):
        return jsonify({
            "success": False,
            "message": "유효한 URL 형식을 입력해주세요"
        }), 400

    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 404 or response.status_code == 400:
            return jsonify({
                "success": False,
                "message": "존재하지 않는 URL입니다"
            }), 400
    except requests.RequestException:
        return jsonify({
            "success": False,
            "message": "URL 요청 중 오류가 발생했습니다"
        }), 400

    return jsonify({
        "success": True,
    })


def get_cards(page):
    per_page = 12

    if page == 1:
        # 1. 좋아요 순 상위 4개 카드 가져오기
        top_cards_cursor = cards_collection.find().sort("likes", -1).limit(4)
        top_cards = []
        top_card_ids = set()
        for card in top_cards_cursor:
            top_cards.append({
                "_id": str(card.get("_id")),
                "img": card.get("img", ""),
                "title": card.get("title", ""),
                "author": card.get("author", ""),
                "tag_list": card.get("tag_list", []),
                "date": card.get("date", ""),
                "likes": card.get("likes", 0),
                "url": card.get("url", "")
            })
            top_card_ids.add(card.get("_id"))

        # 2. 이후 카드는 최신순으로 가져오되, top_cards에 포함된 카드는 제외
        remaining_count = per_page - len(top_cards)
        remaining_cards_cursor = cards_collection.find({
            "_id": {"$nin": list(top_card_ids)}
        }).sort("_id", -1).limit(remaining_count)

        remaining_cards = []
        for card in remaining_cards_cursor:
            remaining_cards.append({
                "_id": str(card.get("_id")),
                "img": card.get("img", ""),
                "title": card.get("title", ""),
                "author": card.get("author", ""),
                "tag_list": card.get("tag_list", []),
                "date": card.get("date", ""),
                "likes": card.get("likes", 0),
                "url": card.get("url", "")
            })

        # 3. top_cards + remaining_cards 반환
        return top_cards + remaining_cards

    else:
        # 페이지가 2 이상인 경우
        skip_count = (page - 1) * per_page

        # 페이지 2 이상에서는 항상 베스트 카드 제외
        top_cards_cursor = cards_collection.find().sort("likes", -1).limit(4)
        top_card_ids = [card.get("_id") for card in top_cards_cursor]

        cards_cursor = cards_collection.find({
            "_id": {"$nin": top_card_ids}
        }).sort("_id", -1).skip(skip_count).limit(per_page)

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
        card = cards_collection.find_one({"_id": ObjectId(card_id)})

        if not card:
            return jsonify({"success": False, "message": "카드를 찾을 수 없습니다."}), 404

        if str(card.get("author_id")) == str(current_user['id']):
            return jsonify({"success": False, "message": "본인 글은 추천할 수 없습니다."}), 400

        user_id_str = str(current_user['id'])
        liked_users = card.get("liked_users", [])

        if user_id_str in liked_users:
            return jsonify({"success": False, "message": "이미 좋아요를 누른 카드입니다."}), 400

        result = cards_collection.update_one(
            {"_id": ObjectId(card_id)},
            {
                "$inc": {"likes": 1},
                "$addToSet": {"liked_users": user_id_str}
            }
        )

        if result.matched_count == 0:
            return jsonify({"success": False, "message": "카드를 찾을 수 없습니다."}), 404

        # 업데이트 후 현재 좋아요 수 반환
        updated_card = cards_collection.find_one({"_id": ObjectId(card_id)})

        return jsonify({
            "success": True,
            "message": "좋아요 추가 성공!",
            "likes": updated_card["likes"]
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

        card = cards_collection.find_one({"_id": ObjectId(card_id)})
        if not card:
            return jsonify({
                "success": False,
                "message": "카드를 찾을 수 없습니다."
            }), 404

        print(f"[DEBUG] 카드 제목: {card['title']}")

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
            questioner_slack_id,
            author_slack_id,
            current_user['name'],
            author['name'],
            card['title'],
            card_id
        )

        if dm_result['success']:
            # Q&A 레코드 생성
            from models.qna import create_qna_record
            qna_id = create_qna_record(
                card_id,
                dm_result.get('channel_id'),
                current_user['name'],
                author['name']
            )

            return jsonify({
                "success": True,
                "message": "질문방이 생성되었습니다!",
                "channel_id": dm_result.get('channel_id'),
                "qna_id": qna_id  # Q&A ID 반환
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


@card_bp.route("/collect-conversation", methods=['POST'])
@auth_required
def collect_conversation_route(current_user):
    """대화 수집 및 영구 저장 (역할 자동 감지)"""
    try:
        # 1. 요청 데이터 파싱
        data = request.get_json()
        card_id = data.get('card_id')

        print(f"[DEBUG] 대화 수집 요청: card_id={card_id}")
        print(
            f"[DEBUG] 현재 사용자: {current_user['name']} (ID: {current_user['id']})")

        # 2. 필수 데이터 검증
        if not card_id:
            return jsonify({
                "success": False,
                "message": "카드 ID가 필요합니다."
            }), 400

        # 3. 카드 정보 조회
        from bson import ObjectId
        card = cards_collection.find_one({"_id": ObjectId(card_id)})
        if not card:
            return jsonify({
                "success": False,
                "message": "카드를 찾을 수 없습니다."
            }), 404

        # 4. 작성자 정보 조회
        author_name = card.get('author')
        author = find_user_by_name(author_name)
        if not author:
            return jsonify({
                "success": False,
                "message": f"작성자 '{author_name}'을 찾을 수 없습니다."
            }), 404

        # 5. 🔥 역할 자동 감지: 현재 사용자가 질문자인지 작성자인지 판단
        current_user_slack_id = current_user.get('slack_user_id')
        author_slack_id = author.get('slack_user_id')

        if not current_user_slack_id or not author_slack_id:
            return jsonify({
                "success": False,
                "message": "Slack 연동이 되지 않은 사용자입니다."
            }), 400

        # 6. 🔥 기존 대화 세션에서 실제 질문자/작성자 찾기
        existing_conversation = db.conversations.find_one({
            "card_id": card_id,
            "$or": [
                {"questioner_slack_id": current_user_slack_id},
                {"author_slack_id": current_user_slack_id}
            ]
        })

        if existing_conversation:
            # 기존 대화가 있는 경우 → 실제 질문자/작성자 사용
            questioner_slack_id = existing_conversation["questioner_slack_id"]
            author_slack_id = existing_conversation["author_slack_id"]
            questioner_name = existing_conversation["questioner_name"]
            author_name = existing_conversation["author_name"]

            print(
                f"[DEBUG] 기존 대화 발견 - 질문자: {questioner_name}({questioner_slack_id}), 작성자: {author_name}({author_slack_id})")
        else:
            # 새로운 대화인 경우 → 현재 사용자가 질문자
            if current_user_slack_id == author_slack_id:
                return jsonify({
                    "success": False,
                    "message": "본인이 작성한 포스팅입니다. 질문하기를 먼저 사용해주세요."
                }), 400

            questioner_slack_id = current_user_slack_id
            questioner_name = current_user['name']

            print(
                f"[DEBUG] 새 대화 - 질문자: {questioner_name}({questioner_slack_id}), 작성자: {author_name}({author_slack_id})")

        # 7. DM 채널 찾기
        from utils.slack_helper import find_dm_channel, collect_conversation_history, extract_conversation_by_card, format_conversation_messages

        channel_id = find_dm_channel(questioner_slack_id, author_slack_id)
        if not channel_id:
            return jsonify({
                "success": False,
                "message": "DM 채널을 찾을 수 없습니다. 먼저 질문하기 버튼을 눌러주세요."
            }), 404

        print(f"[DEBUG] DM 채널 ID: {channel_id}")

        # 8. Slack에서 대화 수집
        all_messages = collect_conversation_history(channel_id)
        card_specific_messages = extract_conversation_by_card(
            all_messages, card_id)
        formatted_messages = format_conversation_messages(
            card_specific_messages, questioner_slack_id, author_slack_id
        )

        print(
            f"[DEBUG] 수집 결과 - 전체: {len(all_messages)}, 카드별: {len(card_specific_messages)}, 포맷됨: {len(formatted_messages)}")

        # 9. 🔥 대화 영구 저장 (올바른 질문자/작성자 정보 사용)
        if formatted_messages:
            from models.conversation import save_conversation

            save_result = save_conversation(
                card_id=card_id,
                channel_id=channel_id,
                questioner_slack_id=questioner_slack_id,
                author_slack_id=author_slack_id,
                questioner_name=questioner_name,
                author_name=author_name,
                post_title=card.get('title', '제목 없음'),
                messages=formatted_messages
            )

            # 10. 성공 응답
            return jsonify({
                "success": True,
                "conversation": formatted_messages,
                "storage": {
                    "saved": save_result["success"],
                    "conversation_id": save_result.get("conversation_id"),
                    "action": save_result.get("action"),
                    "version": save_result.get("version"),
                    "message_count": save_result.get("message_count")
                },
                "debug_info": {
                    "total_messages": len(all_messages),
                    "card_specific_messages": len(card_specific_messages),
                    "formatted_message_count": len(formatted_messages),
                    "channel_id": channel_id,
                    "questioner": questioner_name,
                    "author": author_name
                }
            })
        else:
            return jsonify({
                "success": False,
                "message": "해당 카드에 대한 대화를 찾을 수 없습니다.",
                "debug_info": {
                    "total_messages": len(all_messages),
                    "card_specific_messages": len(card_specific_messages),
                    "formatted_message_count": 0,
                    "channel_id": channel_id
                }
            })

    except Exception as e:
        print(f"[ERROR] 대화 수집 중 오류: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"서버 오류: {str(e)}"
        }), 500


@card_bp.route("/conversation/<conversation_id>", methods=['GET'])
@auth_required
def get_conversation_detail(current_user, conversation_id):
    """특정 대화 상세 조회"""
    try:
        from models.conversation import get_conversation_by_id

        conversation = get_conversation_by_id(conversation_id)

        if conversation:
            return jsonify({
                "success": True,
                "conversation": conversation
            })
        else:
            return jsonify({
                "success": False,
                "message": "대화를 찾을 수 없습니다."
            }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"대화 조회 실패: {str(e)}"
        }), 500


@card_bp.route("/conversation/<conversation_id>/publish", methods=['POST'])
@auth_required
def publish_conversation_route(current_user, conversation_id):
    """대화를 Q&A 게시판에 공개"""
    try:
        from models.conversation import publish_conversation

        result = publish_conversation(conversation_id)

        if result["success"]:
            return jsonify({
                "success": True,
                "message": "대화가 Q&A 게시판에 공개되었습니다.",
                "conversation_id": conversation_id
            })
        else:
            return jsonify({
                "success": False,
                "message": result.get("message", "공개 실패")
            }), 500

    except Exception as e:
        print(f"[ERROR] 공개 처리 실패: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"공개 처리 실패: {str(e)}"
        }), 500
