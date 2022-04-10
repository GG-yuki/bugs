$(function () {
    //导航
    $("#sidebarNav").metisMenu({
        toggle: false
    });
    $("#sidebarScroll").slimscroll({
        height: "100%"
    });
    /*日期时间选择*/
    $(document).on("click", ".js-date", function () {
        WdatePicker();
    });
    $(document).on("click", ".js-datetime", function () {
        var dateFmt = $(this).data("format") || "yyyy-MM-dd HH:mm:ss";
        WdatePicker({
            dateFmt: dateFmt
        });
    });
    //删除图片
    $(".js-deletefile").on("click",function(){
        var _this = this;
        show_confirm("是否确定删除？",function(){
            $(_this).addClass("hidden").siblings(":hidden").val("");
            $img = $(_this).siblings(".js-img");
            $img.attr("src", $img.data("default"));
            show_msg("删除成功");
        });
        return false;
    });
    //取消返回上一页
    $(".js-cancel-btn").on("click",function(){
        window.history.back();
    });
    //列表页搜索
    $("#searchBtn").on("click",function(){
        $(this).closest("form").attr("action","");
    });
    //列表页导出
    $("#exportBtn").on("click",function(){
        var url = $(this).data("url");
        $(this).closest("form").attr("action",url);
    });
});
function show_confirm(info, callback) {
    parent.layer.confirm(info, callback);
}
function show_msg(info) {
    parent.layer.msg(info);
}
function reload(){
    window.location.reload();
}
function is_email(str){
    var reg = /^[\w\+\-]+(\.[\w\+\-]+)*@[a-z\d\-]+(\.[a-z\d\-]+)*\.([a-z]{2,4})$/i;
    return reg.test(str);
}
function is_mobile(str){
    var reg = /^1[3-9]\d{9}$/;
    return reg.test(str);
}
/*tablelist*/
(function ($) {
    var $table = $("#tableList");
    var remove_url = $table.data("remove-url"),
            sort_url = $table.data("sort-url"),
            check_url = $table.data("check-url"),
            status_url = $table.data("status-url");
    var $remove = $("#tableListActions .js-remove-select");
    var $checkBtn = $("#tableListActions .js-check-selected");
    var $btns = $("#tableListActions button");

    function initTableHeight() {
        $table.bootstrapTable('resetView', {
            height: getHeight()
        });
    }
    function getRowID(obj) {
        var index = $(obj).parents('tr[data-index]').eq(0).data("index");
        return $table.bootstrapTable('getData')[index].id;
    }
    function getHeight() {
        return $(window).height() - $('.page-nav-tabs').outerHeight(true) - $(".search-form").outerHeight(true) - 95;
    }
    function getSelectionID() {
        return $.map($table.bootstrapTable("getSelections"), function (row) {
            return row.id;
        });
    }
    function setSort(id, sort) {
        $.ajax({
            type: "POST",
            url: sort_url,
            data: {id: id, sort: sort},
            error: function () {
                show_msg("请求失败，请刷新后再尝试！");
            },
            success: function (rst) {
                if (rst.code === 1) {
                    show_msg("排序更新成功！");
                } else {
                    show_msg(rst.msg);
                }
            }
        });
    }
    function removeItems(ids, callback) {
        if (ids) {
            $.ajax({
                type: "POST",
                url: remove_url,
                data: {ids: ids},
                dataType: 'json',
                error: function () {
                    show_msg("请求失败，请刷新后再尝试！");
                },
                success: function (rst) {
                    if (callback) {
                        callback(rst);
                    } else {
                        if (rst.code === 1) {
                            if($table.hasClass("treetable")){
                                $table.treetable("removeNode",ids);
                            }else{
                                $table.bootstrapTable('remove', {field: "id", values: ids});
                            }
                            show_msg("删除成功！");
                        } else {
                            show_msg(rst.msg);
                        }
                    }
                }
            });
        } else {
            show_msg("参数出错，请刷新后再尝试！");
        }
    }
    function checkItems(ids, command, callback) {
        if (ids && command) {
            $.ajax({
                type: "POST",
                url: check_url,
                data: {ids: ids,command:command},
                dataType: 'json',
                error: function () {
                    show_msg("请求失败，请刷新后再尝试！");
                },
                success: function (rst) {
                    if (callback) {
                        callback(rst);
                    } else {
                        if (rst.code === 1) {
                            window.location.reload();
                            show_msg("删除完成");
                        } else {
                            show_msg(rst.msg);
                        }
                    }
                }
            });
        } else {
            show_msg("参数出错，请刷新后再尝试！");
        }
    }
    function getStatusClassName(status){
        var className = "";
        switch(status){
            case 1:
                className = "fa fa-check";
                break;
            case 0:
                className = "fa fa-times";
                break;
        }
        return className;
    }
    function initStatus(){
        $table.find(".status").each(function(i,o){
            var status = $(this).data("value"), 
                className = getStatusClassName(status);
            $(this).find("i").addClass(className);
        });
    }
    function setStatus(obj){
        var id = getRowID(obj), field = $(obj).data("field"), value = $(obj).data("value");
        if(!id || !field){
            return;
        }
        $.ajax({
            type: "POST",
            url: status_url,
            data: {id: id, field: field, value: value},
            dataType: "json",
            error: function () {
                show_msg("请求失败，请刷新后再尝试！");
            },
            success: function (rst) {
                if (rst.code === 1) {
                    var className = getStatusClassName(rst.data.value);
                    $(obj).data("value",rst.data.value).find("i").removeClass().addClass(className);
                    show_msg("状态更新成功！");
                } else {
                    show_msg(rst.msg);
                }
            }
        });
    }
    function initPageJump() {
        var $pageNum = $("#pageNum");
        var nowpage = parseInt($pageNum.val()) || 1;
        $pageNum.data("nowpage", nowpage);
        $("#pageJumpBtn").on("click", function () {
            var p = parseInt($pageNum.val()) || 1;
            var nowPage = $pageNum.data("nowpage");
            if (p !== nowPage) {
                var href = window.location.href;
                if(window.location.search===""){
                    window.location.href += '?page=' + p;
                    return;
                }
                var reg = new RegExp("(\\?|&)(page=)([^&]*)","i");
                window.location.href = href.replace(reg,"$1$2"+p);
            } else {
                show_msg("已经在当前页");
            }
        });
    }
    $(function () {
        initTableHeight();
        $(window).resize(function () {
            initTableHeight();
        });
        /*排序*/
        $table.on("change", ".js-sort", function () {
            var id = getRowID(this) || 0, sort = parseInt(this.value) || 0;
            setSort(id, sort);
        });
        /*行删除*/
        $table.on("click", ".js-remove", function () {
            var _this = this;
            show_confirm("确定要删除吗？", function () {
                var id = getRowID(_this);
                var ids = id ? [id] : 0;
                removeItems(ids);
                window.parent.layer.closeAll('dialog');
            });
        });
        /*设置状态*/
        initStatus();
        $table.on("click", ".js-status", function(){
            setStatus(this);
        });
        /*批量删除*/
        $table.on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table', function () {
            $btns.prop('disabled', !$table.bootstrapTable('getSelections').length);
        });
        $remove.on("click", function () {
            show_confirm("确定要批量删除吗？", function () {
                var ids = getSelectionID();
                removeItems(ids, function (rst) {
                    window.parent.layer.closeAll('dialog');
                    if (rst.code === 1) {
                        if($table.hasClass("treetable")){
                            $table.treetable("removeNode",ids);
                        }else{
                            $table.bootstrapTable('remove', {field: "id", values: ids});
                        }
                        $remove.prop('disabled', true);
                        show_msg("删除成功！");
                    } else {
                        show_msg(rst.msg);
                    }
                });
            });
        });
        $checkBtn.on("click", function () {
            var _self = this;
            var msg = "确定"+$.trim($(this).text())+"吗？";
            show_confirm(msg, function () {
                var ids = getSelectionID();
                var command = $(_self).data("command");
                checkItems(ids, command, function (rst) {
                    if (rst.code === 1) {
                        window.location.reload();
                        show_msg("操作完成");
                    } else {
                        show_msg(rst.msg);
                    }
                });
            });
        });
        initPageJump();
    });
})(jQuery);
/*treetable*/
(function ($) {
    var $table = $("#tableList.treetable");
    $(function () {
        if(!$table){
            return;
        }
        var column = $table.data("treecolumn") || 3;
        $table.treetable({
            column: column,
            expandable: true,
            initialState: 'expanded',
            onNodeCollapse: function(){
                if($table.data("toggle")==="table"){
                    $table.bootstrapTable("resetView");
                }
            },
            onNodeExpand: function(){
                if($table.data("toggle")==="table"){
                    $table.bootstrapTable("resetView");
                }
            }
        });
        $(".js-tt-expand").on("click", function () {
            $table.treetable("expandAll");
        });
        $(".js-tt-collapse").on("click", function () {
            $table.treetable("collapseAll");
        });
    });
})(jQuery);

function initImageWebUploader(obj,opt){
    var $obj = $(obj);
    var server = $obj.data("server") || "",
        path = $obj.data("path") || "",
        multiple = $obj.data("multiple") || false;
    var display = $obj.data("display") || "imageDisplay";
    var $display = $("#"+display);
    var config = {
        auto: true,
        // swf文件路径
        swf: "/static/admin/js/webuploader/Uploader.swf",
        // 文件接收服务端。
        server: server,
        // 选择文件的按钮。可选。
        pick: {
            id: obj,
            multiple: multiple
        },
        // 不压缩image, 默认如果是jpeg，文件上传前会压缩一把再上传！
        fileVal: 'file',
        formData: {
            filetype: "image",
            path: path
        },
        compress: false,
        // 只允许选择图片文件。
        accept: {
            title: '请选择图片文件',
            extensions: 'gif,jpg,jpeg,bmp,png',
            mimeTypes: 'image/*'
        }
    };
    config = $.extend(config, opt);
    var uploader = WebUploader.create(config);
    uploader.on( 'uploadError', function( file ) {

    });
    uploader.on( 'uploadSuccess', function( file , response) {
        if(response.code===1){
            $display.find(".js-file-input").val(response.savename);
            $display.find(".js-asset-input").val(response.id);
            $display.find(".js-img").attr("src", response.savename);
            $display.find(".js-deletefile").removeClass("hidden");
        }else{
            show_msg(response.msg);
        }
    });
    uploader.on( 'uploadFinished', function( file ) {
        uploader.reset();
    });
}
function initFileWebUploader(obj,opt,callback){
    var $obj = $(obj);
    var server = $obj.data("server") || "",
        path = $obj.data("path") || "",
        multiple = $obj.data("multiple") || false;
    var display = $obj.data("display") || "fileDisplay";
    var $display = $("#"+display);
    var config = {
        auto: true,
        // swf文件路径
        swf: "/static/admin/js/webuploader/Uploader.swf",
        // 文件接收服务端。
        server: server,
        // 选择文件的按钮。可选。
        pick: {
            id: obj,
            multiple: multiple
        },
        // 不压缩image, 默认如果是jpeg，文件上传前会压缩一把再上传！
        fileVal: 'file',
        formData: {
            filetype: "file",
            path: path
        },
        compress: false
    };
    config = $.extend(config, opt);
    var uploader = WebUploader.create(config);
    uploader.on( 'uploadError', function( file ) {
        show_msg("上传控件出错");
    });
    uploader.on( 'uploadSuccess', function( file , response) {
        if(response.code===1){
            $display.find(".js-file-input").val(response.file);
            $display.find(".js-ext-input").val(response.ext);
            $display.find(".js-asset-input").val(response.id);
            if(callback){
                callback(response);
            }
        }else{
            show_msg(response.msg);
        }
    });
    uploader.on( 'uploadFinished', function( file ) {
        uploader.reset();
    });
}