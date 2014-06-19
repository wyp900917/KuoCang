/**
 * Created by ping on 14-6-18.
 */
function report_up(){
    var options = document.getElementsByName("checkbox_1");
    var pids = new Array();
    for(var i=0; i<options.length; i++){
        if(options[i].checked){
            pids.push(options[i].value);
        }
    }
    //document.getElementById("response").innerHTML="";
    if (pids.length == 0){
        alert("请选择需要上报的箱号...");
    }else{
        var xmlhttp;
        if (window.XMLHttpRequest){
            xmlhttp=new XMLHttpRequest();
        }else {
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange=function() {
            if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
                alert("上报成功！");
                location.replace(document.referrer);
            }else if(xmlhttp.status != 200 && xmlhttp.status != 0) {
                alert("上报失败！");
            }
        };
        var _xsrf = getCookie("_xsrf");
        xmlhttp.open("POST","/manage/report_box",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.send("_xsrf="+_xsrf+"&pids="+pids);
    }
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}