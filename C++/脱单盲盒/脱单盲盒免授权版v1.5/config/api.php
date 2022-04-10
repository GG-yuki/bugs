<?php

$domain = env("domain");
return [
    //静态资源主机
    "img_host" => env("img_host"),
    //令牌盐值
    "token_salt" => env('token_salt'),
];