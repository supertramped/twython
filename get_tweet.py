from twython import Twython
import json
import sys

CONSUMER_KEY =  "0YFRlmpYynzylhNKwPGPJxPxd"
CONSUMER_SECRET = "jNFJKNJDN1nGGI4yvq8xLj5PhWmRwqm5rqh1KTvTP4eJulCT8b"
OAUTH_TOKEN = "4560634274-HFuBXpb4DO7BIjs3tfc8oGbP1k1ATnSdxXlaCsY"
OAUTH_TOKEN_SECRET = "zIbwvTkDIKuGhintB2cskWWwU94Vzm6NJv53cWkCfZYKN"


twitter = Twython(
    CONSUMER_KEY, CONSUMER_SECRET,
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

tweets = open("tweets.json", "a")
tweet_chain = []

if len(sys.argv) > 1:
    origin_id = sys.argv[1]
else:
    origin_id = "796316042247012352"

curr_id = origin_id

def getTweet(curr_id):
    tweet_chain.append(curr_id)
    tweet = twitter.show_status(id=curr_id)
    json.dump(tweet,tweets)
            
    reply_to = tweet['in_reply_to_status_id_str']
    if reply_to is not None:
        getTweet(reply_to)
        

getTweet(curr_id)    
print tweet_chain
tweets.close()            

with open("chains.txt", "a") as fp:
    fp.write(json.dumps(tweet_chain) + "\n")
fp.close()
