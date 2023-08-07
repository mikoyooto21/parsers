import coins_ids as ids
import requests
import json
import csv
import time

def process_links(links):
    updated_links = {}
    for key, value in links.items():
        if key == 'twitter_screen_name':
            updated_links['twitter'] = f"twitter.com/{value}"
        elif key == 'facebook_username':
            updated_links['facebook'] = f"facebook.com/{value}"
        else:
            updated_links[key] = value
    return updated_links

def get_last_id():
    try:
        with open('last_id.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_last_id(last_id):
    with open('last_id.txt', 'w') as file:
        file.write(last_id)

def coin_get_data():
    ids_data = ids.get_ids()
    print("Found " + str(len(ids_data)) + " coins")

    last_id = get_last_id()
    if last_id is not None:
        last_id_index = ids_data.index(last_id)
        ids_data = ids_data[last_id_index + 1:]

    try:
        with open('coingecko_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow([
                "id", "symbol", "name", "asset_platform_id", "platforms", "detail_platforms",
                "block_time_in_minutes", "hashing_algorithm", "categories", "public_notice",
                "additional_notices", "description", "links", "image", "country_origin",
                "genesis_date", "sentiment_votes_up_percentage", "sentiment_votes_down_percentage",
                "watchlist_portfolio_users", "market_cap_rank", "coingecko_rank", "coingecko_score",
                "developer_score", "community_score", "liquidity_score", "public_interest_score",
                "community_data", "public_interest_stats", "status_updates", "last_updated"
            ])
            
            for id in ids_data:
                url = f"https://api.coingecko.com/api/v3/coins/{id}?localization=false&tickers=false&market_data=false&community_data=true&developer_data=false"
                response = requests.get(url)
                
                if response.status_code == 429:
                    print("Rate limit exceeded. Waiting for 60 seconds.")
                    time.sleep(60)
                    response = requests.get(url)
                
                if response.status_code == 200:
                    print('Data received')
                    data = json.loads(response.text)
                    data['links'] = json.dumps(process_links(data['links']))  # Зберегти значення links як рядок JSON
                    writer.writerow(list(data.values()))
                    csvfile.flush()
                    save_last_id(id)
                 
            print("Writing data completed.")
    except Exception as exception:
        print(exception)

coin_get_data()
