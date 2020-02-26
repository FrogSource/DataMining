import urllib.request

key = "EWKjFPCPyXju9YmsMAtHVu5Nj"
secret = "pX2Y22ZDzgxVn2NhVApZQQYAM0fcjh5C4v9cQH8sHLb3qMPZsr"
access_token = "65090235-vTZHttfDUWh17HgJQyTqMq7JxIYbDvpJyuLqR3LQb"
access_token_secret = "R7vhHiDDMPl3GJv5mvMD7OennabXmuTarZw0ap06nE8xd"
link = "https://api.twitter.com/1.1/tweets/search/30day/tweets.json"
query = "?q=Friedrich%20Merz"
request = link+query
print(request)
tweets = urllib.request.urlopen(link+query).read()
print(tweets)