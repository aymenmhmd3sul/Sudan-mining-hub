const email = document.getElementById("email");
const password = document.getElementById("password");
const loginBtn = document.querySelector(".login");
const eye = document.getElementById("showPass");

eye.onclick = () => {
    password.type = password.type === "password" ? "text" : "password";
};

window.onload = () => {
    email.value = "";
    password.value = "";
};

loginBtn.onclick = async () => {
    const body = new URLSearchParams();
    body.append("username", email.value.trim());
    body.append("password", password.value);

    const response = await fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body
    });

    const data = await response.json();

    if (!response.ok) {
        alert(typeof data.detail === "string" ? data.detail : "فشل تسجيل الدخول");
        return;
    }

    localStorage.setItem("access_token", data.access_token);

    const me = await fetch("/auth/me", {
        headers: {
            "Authorization": `Bearer ${data.access_token}`
        }
    });

    if (!me.ok) {
        alert("تم تسجيل الدخول ولكن تعذر قراءة بيانات المستخدم.");
        return;
    }

    const user = await me.json();

    if ((user.role || "").toUpperCase() === "ADMIN") {
        window.location.href = "/admin/dashboard";
    } else {
        window.location.href = "/explore";
    }
};
