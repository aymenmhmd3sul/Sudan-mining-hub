from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
<!DOCTYPE html>
<html>
<body>

<h1>JS TEST</h1>

<button onclick="alert('WORKING')">
اضغط هنا
</button>

</body>
</html>
"""
