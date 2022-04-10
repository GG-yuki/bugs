


/**
 * 获取表单数据
 * @param {type} id
 * @returns {unresolved}
 */
function getFormData(form){
    if("object"!==typeof form){
        form = form.indexOf("#")===0 ? $(form) : $("#"+form);
    }
    var postArray = form.serializeArray();
    var postData = {};
    $.each(postArray,function(){
        var name = this.name;
        if(name.indexOf("[]")!==-1){
            name = name.substr(0,name.length-2);
            if(!postData[name]){
                postData[name] = [this.value];
            }else{
                postData[name].push(this.value);
            }
        }else{
            postData[name] = this.value;
        }
    });
    return postData;
}