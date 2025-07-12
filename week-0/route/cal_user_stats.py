from models.database import users_collection
from models.database import cards_collection
from bson import ObjectId

def sum_all_users(user_id):
    user_id = ObjectId(user_id)
    users = list(cards_collection.find({"author_id": user_id}))

    total_posts = users

    total_likes = sum(user.get("likes", 0) for user in total_posts)

    active_date_set = set(card["date"] for card in users if card.get("date"))

    return {
        "total_posts": total_posts,
        "total_likes": total_likes,
        "total_active_days": len(active_date_set)
    }