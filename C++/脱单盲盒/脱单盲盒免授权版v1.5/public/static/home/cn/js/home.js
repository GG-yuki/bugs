$(function () {
    // 展开更多内容
    $(".btn-slide").click(function () {
        $("#showhide").slideToggle();
        $(".btn-slide").slideToggle();
    });

    layui.use(['form','layer'], function () {
        var form=layui.form;
        var layer=layui.layer;

        $("#invitation").click(function () {
            layer.prompt({title:'请输入你的微信号'},function(val){
                window.location.href = '../invitation?wechat='+val;
            });
        });

        form.verify({
            age: function(value) {
                if (value!='' && value< 18) {
                    return '未成年不允许参加哦~';
                }
            },
            wechat: [
                /^[a-zA-Z0-9_]([-_a-zA-Z0-9]{5,19})+$/,'微信号不符合规则！'
            ]
        });

        // 监听二级联动下拉框
        form.on('select(province)',function(data){
            layer.load();
            $.ajax({
                url: '/api/get_region',
                type: 'get',
                data: {pid:data.value},
                dataType: "json",
                success: function(rst){
                    $("select[name='city']").html("");
                    $("select[name='city']").append("<option value='' selected>请选择</option>");
                    $.each(rst.data, function (i, o) {
                        $("select[name='city']").append("<option value='" + o.id + "'>" + o.name_cn + "</option>");
                    });
                    form.render();
                    layer.closeAll('loading');
                }
            });
        });

        // 监听提交按钮
        form.on('submit(formDemo)', function(data){
            layer.load();
            $.ajax({
                url:"/stay/save",
                async: false,
                type:"POST",
                dataType: "json",
                data:data.field,
                success: function(data){
                    if(data.code==0){
                        layer.msg(data.msg);
                        layer.closeAll('loading');
                    }
                    if(data.code==1){
                        if(data.data.url){
                            var content = "您的订单号为【"+data.data.order_sn+"】请截图保存，便于后期查询您的订单。";
                            layer.ready(function(){
                                layer.confirm(content,{'closeBtn':0,title: "重要提示",btn: ['微信支付']}, function(){
                                    window.location.href = data.data.url;
                                });
                            });
                        }else{
                            //询问框
                            layer.confirm(data.msg, {
                                btn: ['在留一个','去抽一个']
                            }, function(){
                                window.location.href = '../stay';
                            },function (){
                                window.location.href = '../take';
                            });
                            layer.closeAll('loading');
                        }
                    }
                }
            });
            return false;
        });
    });
});


$(document).ready(function(){
    $("#funnyNewsTicker1").funnyNewsTicker({width:"100%",timer:3000,titlecolor:"#FFF",itembgcolor:"#f792ac",infobgcolor:"#5a9dbd",buttonstyle:"white"});
});