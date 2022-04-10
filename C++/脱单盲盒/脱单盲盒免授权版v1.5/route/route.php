<?php
// 找不到静态资源，返回404
Route::get('static', function(\think\Response $response){
    return $response->code(404);
});
Route::get('UploadFiles', function(\think\Response $response){
    return $response->code(404);
});
Route::get('uploads', function(\think\Response $response){
    return $response->code(404);
});

// ajax接口
Route::rule("ajax/:action","home/ajax/:action");

//主站相关
$homeRoute = function(){
    // 首页
    Route::get('', 'home/Index/index');
    Route::get('about', 'home/Index/about');
    Route::get('clause', 'home/Index/clause');
    Route::get('order', 'home/Index/order');
    Route::post('order_sava', 'home/Index/order_sava');
    Route::get('invitation', 'home/Index/invitation');


    // 微信官方支付
    Route::group("wxpay",function (){
        Route::get('pay', 'home/Wxpay/wx_pay');
        Route::rule('notify', 'home/Wxpay/wx_notify');
    });

    // 讯虎支付
    Route::group("xunhu",function (){
        Route::rule('notify', 'home/Wxpay/xunhu_notify');
    });

    // XORPAY
    Route::group("xorpay",function (){
        Route::get('pay', 'home/Wxpay/xor_pay');
        Route::rule('notify', 'home/Wxpay/xor_notify');
    });

    // 彩虹易支付
    Route::group("caihong",function (){
        Route::get('pay', 'home/Wxpay/caihong_pay');
        Route::rule('notify', 'home/Wxpay/caihong_notify');
    });

    // 留
    Route::group("stay",function (){
        Route::get('', 'home/Stay/index');
        Route::post('save', 'home/Stay/save');
    });

    // 取
    Route::group("take",function (){
        Route::get('', 'home/Take/index');
        Route::post('save', 'home/Take/save');
    });

    // 新闻
    Route::group("news",function (){
        Route::get('', 'home/News/list');
        Route::get('<id>', 'home/News/info')->pattern(['id'=>'\d+']);
    });

    //默认路由
    Route::miss('home/smart/handle');
};

//注册多语言路由
$lang_list = config("allow_lang_list");
foreach($lang_list as $key => $lang){
    if($key === config("default_lang")){
        $homeRoute();
    }else{
        Route::group($lang, $homeRoute)->append(["lang"=>$lang]);
        Route::get($lang."/", 'home/index/index')->append(["lang"=>$lang]);
    }
}

//后台
Route::rule('admin/:c/:a', "admin/:c/:a");
Route::rule('admin', "admin/index/index");