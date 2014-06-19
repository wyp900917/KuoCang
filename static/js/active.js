/**
 * Created by ping on 14-5-29.
 */
function active(){
    document.getElementById("trace_tip").innerHTML="12位";
    document.getElementById("result").innerHTML="";
    if (document.getElementById("trace_codes").value.length==0){
        document.getElementById("trace_tip").innerHTML="追溯码不能为空！";
    }else{
        var xmlhttp;
        if (window.XMLHttpRequest){
            xmlhttp=new XMLHttpRequest();
        }else {
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange=function() {
            if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
                document.getElementById("result").innerHTML=xmlhttp.responseText;
                document.getElementById("trace_codes").value="";
            }
        };
        var _xsrf = getCookie("_xsrf");
        xmlhttp.open("POST","/sale/active",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.send("_xsrf="+_xsrf+"&trace_codes="+document.getElementById("trace_codes").value);
    }
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}