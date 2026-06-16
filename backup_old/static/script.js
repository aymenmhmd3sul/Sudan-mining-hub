function showToast(message, isError) {
    var toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.display = 'block';
    toast.style.borderColor = isError ? '#ef4444' : '#22c55e';
    setTimeout(function() {
        toast.style.display = 'none';
    }, 3000);
}

function refreshData() {
    var btn = document.getElementById('refreshDataBtn');
    btn.disabled = true;
    btn.innerHTML = '⏳ جاري التحديث... <span class="spinner"></span>';

    fetch('/api/gold')
        .then(function(response) {
            if (!response.ok) throw new Error('فشل جلب البيانات');
            return response.json();
        })
        .then(function(data) {
            if (data.gold !== undefined) {
                document.getElementById('goldPrice').innerHTML = '💰 USD ' + data.gold.toFixed(2) + ' <span>| PAXG</span>';
                document.getElementById('lastUpdate').textContent = new Date().toLocaleString('ar-EG');

                // تحديث الأرقام الوهمية
                document.getElementById('orders').textContent = Math.floor(1200 + Math.random() * 200);
                document.getElementById('traders').textContent = Math.floor(320 + Math.random() * 50);
                document.getElementById('mining').textContent = Math.floor(50 + Math.random() * 15);
                document.getElementById('ads').textContent = Math.floor(80 + Math.random() * 20);
                document.getElementById('subscriptions').textContent = Math.floor(220 + Math.random() * 50);

                showToast('✅ تم تحديث البيانات بنجاح!', false);
            }
        })
        .catch(function(error) {
            showToast('❌ فشل تحديث البيانات: ' + error.message, true);
        })
        .finally(function() {
            btn.disabled = false;
            btn.innerHTML = '🔄 تحديث البيانات';
        });
}
