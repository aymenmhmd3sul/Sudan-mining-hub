function toggleSidebar() {
    const sidebar = document.getElementById("adminSidebar");
    if (sidebar) {
        sidebar.classList.toggle("open");
    }
}

function toggleDropdown(id) {
    const menu = document.getElementById(id);
    if (menu) {
        menu.classList.toggle("open");
    }
}
