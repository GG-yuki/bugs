/**
 * 发送AJAX请求
 * @param {type} url
 * @param {type} type
 * @param {type} data
 * @param {type} success
 * @param {type} error
 * @param {type} complete
 * @returns {undefined}
 */
function sendRequest(url,type,data,success,error,complete){
    $.ajax({
        url: url,
        type: type,
        data: data,
        dataType: "json",
        success: function(rst,status,response){
            if(success){
                success(rst,status,response);
            }
        },
        error: function(){
            if(error){
                error();
            }
        },
        complete: function(){
            if(complete){
                complete();
            }
        }
    });
}

//全选操作
function checkALL(checkallItem, checkitem, parentitem) {

    var checkall = $(parentitem).find(checkallItem);
    var checkitem = $(parentitem).find(checkitem);

    checkall.click(function() {
        if ($(this).is(':checked')) {
            checkitem.each(function() {
                $(this).prop("checked", true);
            });
        } else {
            checkitem.each(function() {
                $(this).prop("checked", false);
            });
        }

    });
}
/**
 * 获取省市区数据
 * @param {type} pid 父ID
 * @param {type} callback
 * @returns {undefined}
 */
function getRegion(pid,callback){
    var url = "/api/get_region";
    sendRequest(url,"get",{
        pid : pid
    },callback);
}
/**
 * 用于省市区联动
 * @param {type} s_id
 * @param {type} t_id
 * @param {type} sub_id
 * @returns {undefined}
 */
function LoadAddress(s_id, t_id, sub_id) {
    $(".form-input form-select form-row3 fl_last_address").hide();

    var parentID = $("#" + s_id).val();
    $("#" + t_id + " option:gt(0)").remove();
    if (sub_id.length > 0) {
        $("#" + sub_id + " option:gt(0)").remove();
    }
    getRegion(parentID, function (rst) {
        if (rst.code === 1) {
            $.each(rst.data, function (i, o) {
                var html = '<option value="' + o.id + '">' + o.name_cn + '</option>';
                $("#" + t_id).append(html);
            });
        }
        if ($(".form-input form-select form-row3 fl_last_address  option").length > 1) {
            $(".form-input form-select form-row3 fl_last_address").show();
        }
    });
}
/**
 * 检查是否数字
 * @param {type} str
 * @returns {Boolean}
 */
 function isNumber(str) {
    var reg = /^([0-9]*)$/;
    return reg.test(str);
}

function show_msg(info) {
    layer.msg(info);
}

//序列化表单字段为json对象
$.fn.serializeFormToJson = function() {
    var arr = $(this).serializeArray();//form表单数据 name：value
    var param = {};
    $.each(arr, function (i, obj) { //将form表单数据封装成json对象
        param[obj.name] = obj.value;
    });
    return param;
};