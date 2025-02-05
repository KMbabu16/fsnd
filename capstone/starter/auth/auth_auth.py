import http.client

conn = http.client.HTTPSConnection("dev-om80m547hwxipo72.us.auth0.com")

payload = "{\"client_id\":\"ChUol8i9qIb9NQ9oZQENsvkBmRFQV7qe\",\"client_secret\":\"iQ8_FygYs_uvuDBE0vQhJq-LSSKdFnWoKYNmAJSv7M6JFKPjKi63gwnq1IUFksQW\",\"audience\":\"CoffeeShop\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))