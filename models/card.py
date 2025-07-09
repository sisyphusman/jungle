from models.database import cards_collection


def get_cards():
    return cards_collection.find()
