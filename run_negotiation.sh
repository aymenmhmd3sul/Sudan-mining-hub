BUYER_TOKEN=$(cat buyer_token.txt)

curl -X POST "http://127.0.0.1:8080/api/negotiation/rooms" \
     -H "Authorization: Bearer $BUYER_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"asset_id": 1}'
