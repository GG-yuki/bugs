<?php
//接口路由
Route::get('links', 'api/links/click');

Route::group("api",function(){
    Route::get("get_region","api/country/region");


});


