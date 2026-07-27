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
            const response = await fetch("/api/web/login", {
                method: "POST",
                body: form
            });

            const data = await response.json();

            if(response.ok){

                localStorage.setItem(
                    "access_token",
                    data.access_token
                );

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

if(arBtn){
    arBtn.onclick = () => {
        document.documentElement.lang = "ar";
        document.documentElement.dir = "rtl";
        langMenu.style.display = "none";
    };
}

if(enBtn){
    enBtn.onclick = () => {
        document.documentElement.lang = "en";
        document.documentElement.dir = "ltr";
        langMenu.style.display = "none";
    };
}


function applyLanguage(lang){

    const data = {
        ar:{
            title:"منصة السودان للتعدين",
            subtitle:"بوابة إدارة قطاع التعدين الذكية",
            login:"بوابة الدخول",
            email:"البريد الإلكتروني",
            password:"كلمة المرور",
            loginBtn:"🔐 تسجيل الدخول الآمن",
            register:"التسجيل لأول مرة",
            visitor:"دخول كزائر"
        },
        en:{
            title:"Sudan Mining Hub",
            subtitle:"Smart Mining Sector Management Gateway",
            login:"Login Gateway",
            email:"Email Address",
            password:"Password",
            loginBtn:"🔐 Secure Login",
            register:"Register First Time",
            visitor:"Visitor Access"
        }
    };

    const t=data[lang];

    document.querySelector(".brand strong").textContent=t.title;
    document.querySelector(".brand span").textContent=t.subtitle;
    document.querySelector(".main-card h1").textContent=t.login;

    document.getElementById("email").placeholder=t.email;
    document.getElementById("password").placeholder=t.password;
    document.getElementById("loginBtn").textContent=t.loginBtn;

    const links=document.querySelectorAll(".links a");
    if(links.length>=2){
        links[0].textContent=t.register;
        links[1].textContent=t.visitor;
    }

    const ads=document.querySelectorAll(".gold-scroll span");

    if(lang==="en" && ads.length>=4){
        ads[0].textContent="🟡 Live Gold Market | Ounce: $3420 | 24K Global Price";
        ads[1].textContent="🌍 International investors seeking mining opportunities in Sudan";
        ads[2].textContent="⛏ Mining equipment and projects for sale and purchase";
        ads[3].textContent="🚚 Mining transport and logistics services available";
    }

    if(lang==="ar" && ads.length>=4){
        ads[0].textContent="🟡 بورصة الذهب مباشرة | الأونصة: $3420 | عيار 24: سعر عالمي";
        ads[1].textContent="🌍 مستثمرون دوليون يبحثون عن فرص التعدين في السودان";
        ads[2].textContent="⛏ معدات تعدين ومشاريع للبيع والشراء عبر المنصة";
        ads[3].textContent="🚚 خدمات النقل واللوجستيات التعدينية متاحة الآن";
    }

    localStorage.setItem("language",lang);
}

if(enBtn){
    enBtn.onclick=()=>{
        applyLanguage("en");
        document.documentElement.lang="en";
        document.documentElement.dir="ltr";
        langMenu.style.display="none";
    };
}

if(arBtn){
    arBtn.onclick=()=>{
        applyLanguage("ar");
        document.documentElement.lang="ar";
        document.documentElement.dir="rtl";
        langMenu.style.display="none";
    };
}

const savedLanguage=localStorage.getItem("language");
if(savedLanguage){
    applyLanguage(savedLanguage);
}

