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
            message.textContent = document.body?.dataset?.loginChecking || "Checking...";
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
                    document.body?.dataset?.loginInvalid ||
                    "Email or password is incorrect";
                }
            }

        } catch(e){

            if(message){
                message.textContent =
                document.body?.dataset?.loginServerError ||
                "Unable to connect to the server";
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
            const prefix = document.body?.dataset?.browseCategory || "Browse";
            requireAuth(`${prefix} ${catName}`);
        }

        function requireAuth(actionName) {
            closeModalDirect('detailModal');
            const body = document.body;
            const loginText = body?.dataset?.loginText || "Login";
            const registerText = body?.dataset?.registerText || "Create Account";
            const prefix = body?.dataset?.authPrefix || "To complete";
            const connector = body?.dataset?.authConnector || "please";
            const suffix = body?.dataset?.authSuffix || "on the platform.";

            document.getElementById('authActionText').innerText =
                `${prefix} (${actionName}), ${connector} ${loginText} or ${registerText} ${suffix}`;
            openModalWithHistory('authModal');
        }

        function toggleLanguage() {
            const currentLang = document.documentElement.lang || "ar";
            window.location.href = currentLang === "ar"
                ? "/language/en"
                : "/language/ar";
        }

/* GLOBAL INTERACTIVE GATEWAY HOOKS */
window.showDetail = showDetail;
window.openCategory = openCategory;
window.requireAuth = requireAuth;
window.toggleLanguage = toggleLanguage;
window.closeModalDirect = closeModalDirect;
/* END GLOBAL INTERACTIVE GATEWAY HOOKS */

/* END ORIGINAL INTERACTIVE GATEWAY ENGINE */

/* INTERACTIVE GATEWAY BEHAVIOR FIX v3 */
(function () {
    "use strict";

    function normalize(value) {
        return String(value || "").trim().toLowerCase();
    }

    function getCards() {
        return Array.from(document.querySelectorAll(".asset-card"));
    }

    function applyGatewayFilters() {
        const searchInput =
            document.querySelector(".search-box input");

        const filters =
            document.querySelectorAll(".filter-select");

        const stateSelect = filters[0] || null;
        const categorySelect = filters[1] || null;

        const search = normalize(
            searchInput ? searchInput.value : ""
        );

        const selectedState = normalize(
            stateSelect ? stateSelect.value : ""
        );

        const selectedCategory = normalize(
            categorySelect ? categorySelect.value : ""
        );

        const allStatesText = normalize(
            stateSelect &&
            stateSelect.options[0]
                ? stateSelect.options[0].textContent
                : ""
        );

        const allCategoriesText = normalize(
            categorySelect &&
            categorySelect.options[0]
                ? categorySelect.options[0].textContent
                : ""
        );

        getCards().forEach(function (card) {
            const text = normalize(card.innerText || "");

            const cardState = normalize(
                card.dataset.state || ""
            );

            const cardCategory = normalize(
                card.dataset.category || ""
            );

            const searchOK =
                !search || text.includes(search);

            const stateOK =
                !selectedState ||
                selectedState === allStatesText ||
                cardState === selectedState;

            const categoryOK =
                !selectedCategory ||
                selectedCategory === allCategoriesText ||
                cardCategory === selectedCategory;

            card.style.display =
                searchOK && stateOK && categoryOK
                    ? ""
                    : "none";
        });
    }

    function bindGatewayFilters() {
        const searchInput =
            document.querySelector(".search-box input");

        const filters =
            document.querySelectorAll(".filter-select");

        if (
            searchInput &&
            searchInput.dataset.gatewayFilterBound !== "1"
        ) {
            searchInput.dataset.gatewayFilterBound = "1";

            searchInput.addEventListener(
                "input",
                applyGatewayFilters
            );
        }

        filters.forEach(function (el) {
            if (el.dataset.gatewayFilterBound === "1") {
                return;
            }

            el.dataset.gatewayFilterBound = "1";

            el.addEventListener(
                "change",
                applyGatewayFilters
            );
        });

        applyGatewayFilters();
    }

    /* closeModalDirect is already defined by the original gateway engine.
       Keep one implementation only. */

    document.addEventListener(
        "DOMContentLoaded",
        bindGatewayFilters
    );

    if (document.readyState !== "loading") {
        bindGatewayFilters();
    }
})();
/* END INTERACTIVE GATEWAY BEHAVIOR FIX v3 */
