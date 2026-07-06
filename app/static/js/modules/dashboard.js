
function init_dashboard() {
    const token = localStorage.getItem("token");
    fetch("/admin/api/dashboard-data", { headers: { "Authorization": "Bearer " + token } })
        .then(res => res.json())
        .then(data => {
            const grid = document.getElementById("dash-stats-grid");
            if(!grid) return;
            
            const stats = data.system_stats;
            grid.innerHTML = `
                <div style="background:#1e1e1e; padding:20px; border-radius:8px; border-top:3px solid #DAA520;">
                    <h3 style="color:#aaa;font-size:13px;margin-bottom:10px;">التجار المحليين</h3>
                    <div style="font-size:26px;font-weight:bold;">${stats.active_traders}</div>
                </div>
                <div style="background:#1e1e1e; padding:20px; border-radius:8px; border-top:3px solid #DAA520;">
                    <h3 style="color:#aaa;font-size:13px;margin-bottom:10px;">طلبات الشراء (LOI)</h3>
                    <div style="font-size:26px;font-weight:bold;color:#ff4444;">${stats.pending_lois}</div>
                </div>
            `;
        })
        .catch(err => console.error("Dashboard Service Error:", err));
}
// تشغيل فوري عند حقن السكريبت لأول مرة
init_dashboard();
