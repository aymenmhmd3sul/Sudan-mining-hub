async function loginUser() {
    const username = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);

    const response = await fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: form
    });

    const data = await response.json();

    if (!response.ok) {
        alert("بيانات الدخول غير صحيحة");
        return;
    }

    localStorage.setItem("access_token", data.access_token);

    const profile = await fetch("/auth/me", {
        headers: {
            "Authorization": `Bearer ${data.access_token}`
        }
    });

    const user = await profile.json();

    if (user.role && user.role.toUpperCase() === "ADMIN") {
        window.location.href = "/admin/dashboard";
    } else {
        window.location.href = "/explore";
    }
}


document.addEventListener("DOMContentLoaded", () => {

    const btn = document.querySelector(".login");

    if (btn) {
        btn.addEventListener("click", loginUser);
    }

    const pass = document.getElementById("password");
    const eye = document.getElementById("showPass");

    if (eye && pass) {
        eye.onclick = () => {
            pass.type = pass.type === "password"
                ? "text"
                : "password";
        };
    }

});
