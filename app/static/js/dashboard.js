
function logToDev(msg) {
    const log = document.getElementById('dev-log');
    if(log) log.innerHTML += '<div>> ' + new Date().toLocaleTimeString() + ' : ' + msg + '</div>';
    console.log(msg);
}

async function testConnection() {
    const output = document.getElementById('test-output');
    const devPanel = document.getElementById('dev-panel');
    devPanel.style.display = 'block';
    output.style.display = 'block';
    
    logToDev("جاري الاتصال بـ /opportunity-center/explore ...");
    
    try {
        const start = performance.now();
        const response = await fetch('/opportunity-center/explore');
        const end = performance.now();
        
        logToDev('Status: ' + response.status);
        logToDev('Time: ' + (end - start).toFixed(2) + 'ms');
        
        const data = await response.json();
        output.innerText = JSON.stringify(data, null, 2);
        logToDev('Records: ' + (data.data ? data.data.length : 0));
        
    } catch (error) {
        logToDev('Error: ' + error.message);
    }
}
