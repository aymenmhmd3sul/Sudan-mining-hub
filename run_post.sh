curl -X POST "http://127.0.0.1:8080/api/assets/assets" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InVzcl9hZG1pbl8wMDEiLCJzdWIiOiJheW1lbi5taG1kM0BnbWFpbC5jb20iLCJyb2xlIjoic3VwZXJhZG1pbiIsImlzX2FjdGl2ZSI6dHJ1ZSwic3RhdHVzIjoiQUNUSVZFIiwiZXhwIjoxNzgzMDU0NzAxLjk4MDQ1Mn0.L1lvZWhv2Hd5nRXRoPbgDnN7CVXK3e0voaG3MiOpKmY" \
     -H "Content-Type: application/json" \
     -d @test_asset.json
