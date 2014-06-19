/**
 * Created by ping on 14-6-11.
 */
function check(form){
    document.getElementById("validate_1").innerHTML="";
    document.getElementById("validate_2").innerHTML="";
    if (form["text_1"].value==""){
        document.getElementById("validate_1").innerHTML="此项为必填，不能为空！";
        if (form["text_2"].value==""){
            document.getElementById("validate_2").innerHTML="此项为必填，不能为空！";
        }
        return false;
    }
    if (form["text_2"].value==""){
        document.getElementById("validate_2").innerHTML="此项为必填，不能为空！";
        return false;
    }
    return true;
}