from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Test UI</title>

<style>
body {
    font-family: Arial;
    background:#0b1220;
    color:white;
    text-align:center;
}

.card {
    margin:20px auto;
    padding:20px;
    width:200px;
    background:#1f2937;
    cursor:pointer;
    border-radius:10px;
}

#modal {
    display:none;
    position:fixed;
    top:0;left:0;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.8);
}

.box {
    background:#111827;
    margin:20% auto;
    padding:20px;
    width:80%;
    border-radius:10px;
}
</style>
</head>

<body>

<h2>Dashboard Test</h2>

<div class="card" onclick="openModal()">
اضغط هنا
</div>

<div id="modal">
    <div class="box">
        <h3>Modal Works</h3>
        <button onclick="closeModal()">Close</button>
    </div>
</div>

<script>
function openModal() {
    document.getElementById("modal").style.display = "block";
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}
</script>

</body>
</html>
"""
