function toggleSidebar() {
    document.getElementById('adminSidebar').classList.toggle('open');
}

function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    const isVisible = dropdown.style.display === 'block';
    
    // إغلاق أي قوائم مفتوحة أخرى اختياريًا لتقليل التشتت على الهاتف
    document.querySelectorAll('.sidebar-sub-menu').forEach(menu => menu.style.display = 'none');
    
    dropdown.style.display = isVisible ? 'none' : 'block';
}
