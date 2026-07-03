BUYER_TOKEN=$(cat buyer_token.txt)

curl -X POST "http://127.0.0.1:8080/api/negotiation/rooms/1/messages" \
     -H "Authorization: Bearer $BUYER_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"message": "أنا جاد في الشراء وجاهز للتنفيذ الفوري، وهذا عرضي المالي الأول.", "offer_price": 120000.0}'
