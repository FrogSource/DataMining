import urllib.request

link = "https://api.twitter.com/1.1/search/tweets.json"
query = "?q=Friedrich%20Merz"
request = link+query
print(request)
tweets = urllib.request.urlopen(link+query).read()
print(tweets)