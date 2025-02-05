import http.client

conn = http.client.HTTPSConnection("dev-om80m547hwxipo72.us.auth0.com")

payload = "{\"client_id\":\"4psv5F2kPSqNsZE91bGj74iVMP3d123q\",\"client_secret\":\"LN5ZK-z9Sf2zdU9OqhBbZoQYmH3k7ig2fXF4w6rodK9uRuPs37Y4u-B1NKhRDwOB\",\"audience\":\"fsnd\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))