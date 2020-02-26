import json
credentials = {}
credentials['CONSUMER_KEY'] = "EWKjFPCPyXju9YmsMAtHVu5Nj"
credentials['CONSUMER_SECRET'] = "pX2Y22ZDzgxVn2NhVApZQQYAM0fcjh5C4v9cQH8sHLb3qMPZsr"
credentials['ACCESS_TOKEN'] = "65090235-vTZHttfDUWh17HgJQyTqMq7JxIYbDvpJyuLqR3LQb"
credentials['ACESS_SECRET'] = "R7vhHiDDMPl3GJv5mvMD7OennabXmuTarZw0ap06nE8xd"

with open("twitter_credentials.json","w") as file:
    json.dump(credentials,file)

print(file)