import json

tweets_data_path = '/Users/xinan/Desktop/big_data/data.json'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

print("Total tweets:" )
print(len(tweets_data))
