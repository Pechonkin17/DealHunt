from db.mongo_client import get_games_collection
from services.steam_parser import SteamParser

def main():
    collection = get_games_collection()
    parser = SteamParser(collection)
    games = parser.fetch_discounts()
    print(f"[INFO] Parsed and saved {len(games)} games to MongoDB")

if __name__ == '__main__':
    main()
