import requests

r = requests.post(url="http://upe.42069.fun/jizyr/reset", data={"email": "aqchen@ucla.edu"})
print(r.json())