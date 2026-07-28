const pass = document.getElementById("password");
const eye = document.getElementById("showPass");

if (eye) {
    eye.onclick = () => {
        if (pass.type === "password") {
            pass.type = "text";
        } else {
            pass.type = "password";
        }
    };
}


const loginBtn = document.querySelector(".login");

if (loginBtn) {
    loginBtn.onclick = async () => {

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {

            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });


            const data = await response.json();


            if (!response.ok) {
                alert(data.detail || "فشل تسجيل الدخول");
                return;
            }


            localStorage.setItem(
                "access_token",
                data.access_token
            );


            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );


            if (data.user.role === "ADMIN") {
                window.location.href = "/admin/dashboard";
            }
            else if (data.user.role === "MERCHANT") {
                window.location.href = "/merchant";
            }
            else if (data.user.role === "BUYER") {
                window.location.href = "/buyer";
            }
            else {
                window.location.href = "/";
            }


        } catch (error) {

            console.error(error);
            alert("تعذر الاتصال بالخادم");

        }

    };
}


window.onload = () => {

    const email = document.getElementById("email");
    const password = document.getElementById("password");

    if (email) email.value = "";
    if (password) password.value = "";

};

// Theme selector
const themeBtn = document.getElementById("themeBtn");
const themeOptions = document.getElementById("themeOptions");

if (themeBtn && themeOptions) {

    themeBtn.onclick = () => {
        themeOptions.classList.toggle("active");
    };

    document.querySelectorAll("[data-theme]").forEach(btn => {

        btn.onclick = () => {
            const theme = btn.dataset.theme;

            document.body.classList.remove(
                "theme-notebook",
                "theme-mobile"
            );

            if (theme === "notebook") {
                document.body.classList.add("theme-notebook");
            }

            if (theme === "mobile") {
                document.body.classList.add("theme-mobile");
            }

            localStorage.setItem(
                "gateway_theme",
                theme
            );

            themeOptions.classList.remove("active");
        };

    });

    const savedTheme = localStorage.getItem("gateway_theme");

    if (savedTheme === "notebook") {
        document.body.classList.add("theme-notebook");
    }

    if (savedTheme === "mobile") {
        document.body.classList.add("theme-mobile");
    }
}
