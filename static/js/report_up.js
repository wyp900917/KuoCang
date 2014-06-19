/**
 * Created by ping on 14-6-5.
 */
function report_up(){
    var options = document.getElementsByName("checkbox_1");
    var company_id = document.getElementById("company_id").value;
    var reporter = document.getElementById("reporter").value;
    var trace_codes = new Array();
    for(var i=0; i<options.length; i++){
        if(options[i].checked){
            trace_codes.push(options[i].value);
        }
    }
    //document.getElementById("response").innerHTML="";
    if (trace_codes.length == 0){
        alert("请选择需要上报的追溯码...");
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
        xmlhttp.open("POST","/manage/report",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.send("_xsrf="+_xsrf+"&trace_codes="+trace_codes+"&company_id="+company_id+"&reporter="+reporter);
    }
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}