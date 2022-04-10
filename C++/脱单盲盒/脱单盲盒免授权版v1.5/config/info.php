<?php

/* 
 * 用于存放网站的一些预设数据
 * 
 */

return [
    "device" => "pc",
    //万能验证码
    "smscode" => "734862",
    //中间件名称
    "middleware" => [
        '1' => "IpBlacklist", //IP黑名单
        '2' => "IsWeixin", //禁止PC端
    ]

];