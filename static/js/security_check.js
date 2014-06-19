/**
 * Created by ping on 14-5-29.
 */
function security_check(){
    document.getElementById("trace").innerHTML="12位";
    document.getElementById("security").innerHTML="6位";
    document.getElementById("result").innerHTML="";
    if (document.getElementById("trace_code").value.length==0){
        document.getElementById("trace").innerHTML="追溯码不能为空！";
        if (document.getElementById("security_code").value.length==0){
            document.getElementById("security").innerHTML="防伪码不能为空！";
        }
    }else if(document.getElementById("security_code").value.length==0){
        document.getElementById("security").innerHTML="防伪码不能为空！";
    } else{
        var xmlhttp;
        if (window.XMLHttpRequest){
            xmlhttp=new XMLHttpRequest();
        }else {
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange=function() {
            if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
                document.getElementById("result").innerHTML=xmlhttp.responseText;
            }
        };
        var _xsrf = getCookie("_xsrf");
        xmlhttp.open("POST","/security_check",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.send("_xsrf="+_xsrf+"&trace_code="+document.getElementById("trace_code").value+"&security_code="+document.getElementById("security_code").value);
    }
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

/*
function cls(obj,v){
    if(obj.value == v){
        obj.value="";
        obj.style.color='#aaa'
    }
}
function res(obj, v){
    if(obj.value==""){
        obj.value=v;
        obj.style.color='#ccc'
    }
}*/
