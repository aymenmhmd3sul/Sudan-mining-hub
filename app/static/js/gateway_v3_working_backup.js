const pass = document.getElementById("password");
const eye = document.getElementById("showPass");

if(eye){
 eye.onclick=()=>{
  pass.type = pass.type==="password" ? "text" : "password";
 };
}


const loginBtn=document.querySelector(".primary");

if(loginBtn){

loginBtn.onclick=async()=>{

const email=document.getElementById("email").value;
const password=document.getElementById("password").value;

try{

const r=await fetch("/api/auth/login",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
email,
password
})
});


const data=await r.json();


if(!r.ok){
alert(data.detail || "فشل الدخول");
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


if(data.user.role==="ADMIN"){
location.href="/admin/dashboard";
}

else if(data.user.role==="MERCHANT"){
location.href="/merchant";
}

else if(data.user.role==="BUYER"){
location.href="/buyer";
}

else{
location.href="/";
}


}
catch(e){

alert("تعذر الاتصال بالخادم");

}

};

}



const visitor=document.querySelector(".visitor");

if(visitor){
visitor.onclick=()=>{
location.href="/";
};
}
