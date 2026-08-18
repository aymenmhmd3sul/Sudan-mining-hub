const showPass = document.getElementById("showPass");
const password = document.getElementById("password");

if (showPass && password) {
    showPass.onclick = () => {
        if (password.type === "password") {
            password.type = "text";
            showPass.textContent = "🙈";
        } else {
            password.type = "password";
            showPass.textContent = "👁";
        }
    };
}


// Language
const langBtn = document.getElementById("langBtn");
const langMenu = document.getElementById("langMenu");

if (langBtn && langMenu) {
    langBtn.onclick = () => {
        langMenu.style.display =
            langMenu.style.display === "block"
            ? "none"
            : "block";
    };
}


// Login
const loginBtn = document.getElementById("loginBtn");
const message = document.getElementById("message");

if (loginBtn) {
    loginBtn.onclick = async () => {

        const email = document.getElementById("email").value;
        const pass = document.getElementById("password").value;

        const form = new FormData();
        form.append("username", email);
        form.append("password", pass);

        if(message){
            message.textContent = "جاري التحقق...";
        }

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                body: form
            });

            const data = await response.json();

            if(response.ok){

                if(message){
                    message.textContent = data.message;
                }

                setTimeout(()=>{
                    window.location.href = data.redirect;
                },800);

            } else {

                if(message){
                    message.textContent =
                    "البريد الإلكتروني أو كلمة المرور غير صحيحة";
                }
            }

        } catch(e){

            if(message){
                message.textContent =
                "تعذر الاتصال بالخادم";
            }
        }
    };
}


// Visitor
const visitor = document.querySelector(".links a:last-child");

if(visitor){
    visitor.onclick = ()=>{
        window.location.href="/";
    };
}

const arBtn = document.querySelector("#langMenu .ar");
const enBtn = document.querySelector("#langMenu .en");

if (arBtn) {
    arBtn.onclick = (event) => {
        if (event) event.preventDefault();
        window.location.href = "/language/ar";
    };
}

if (enBtn) {
    enBtn.onclick = (event) => {
        if (event) event.preventDefault();
        window.location.href = "/language/en";
    };
}

const serverLanguage =
    document.body.dataset.serverLanguage === "en" ? "en" : "ar";

document.documentElement.lang = serverLanguage;
document.documentElement.dir =
    serverLanguage === "ar" ? "rtl" : "ltr";

/* ORIGINAL INTERACTIVE GATEWAY ENGINE — restored from 3d81c60 */
// Smartphone Back Button Handling (History API)
        function openModalWithHistory(modalId) {
            document.getElementById(modalId).style.display = 'flex';
            window.history.pushState({ modalOpen: modalId }, "");
        }

        function closeModalDirect(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        window.onpopstate = function(event) {
            document.getElementById('detailModal').style.display = 'none';
            document.getElementById('authModal').style.display = 'none';
        };

        // View Item Details Before Auth
        function showDetail(title, price, location, desc, imgSrc) {
            document.getElementById('detailTitle').innerText = title;
            document.getElementById('detailPrice').innerText = price;
            document.getElementById('detailLoc').innerText = location;
            document.getElementById('detailDesc').innerText = desc;
            document.getElementById('detailImg').src = imgSrc;
            openModalWithHistory('detailModal');
        }

        function openCategory(catName) {
            requireAuth('تصفح فئة ' + catName);
        }

        function requireAuth(actionName) {
            closeModalDirect('detailModal');
            const body = document.body;
            const loginText = body?.dataset?.loginText || "تسجيل الدخول";
            const registerText = body?.dataset?.registerText || "التسجيل";
            document.getElementById('authActionText').innerText =
                `لإكمال (${actionName})، يرجى ${loginText} أو ${registerText} على المنصة.`;
            openModalWithHistory('authModal');
        }

        function toggleLanguage() {
            const currentLang = document.documentElement.lang || "ar";
            window.location.href = currentLang === "ar"
                ? "/language/en"
                : "/language/ar";
        }
/* END ORIGINAL INTERACTIVE GATEWAY ENGINE */
