
const pass=document.getElementById("password");
const eye=document.getElementById("showPass");

eye.onclick=()=>{

if(pass.type==="password"){
pass.type="text";
}else{
pass.type="password";
}

};


window.onload=()=>{

document.getElementById("email").value="";
document.getElementById("password").value="";

};

