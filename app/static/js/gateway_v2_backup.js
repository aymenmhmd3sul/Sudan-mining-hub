async function loginUser() {
    const username = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("يرجى إدخال البريد وكلمة المرور");
        return;
    }

    try {
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

        if (data.redirect) {
            window.location.href = data.redirect;
        } else {
            window.location.href = "/explore";
        }

    } catch (error) {
        alert("تعذر الاتصال بالخادم");
        console.error(error);
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
