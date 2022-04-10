<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK IT ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006-2016 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: yunwuxin <448901948@qq.com>
// +----------------------------------------------------------------------

return [
    'connector' => env('queue_connector'),
    'expire'    => env('queue_expire'),
    'default'   => env('queue_default'),

    //数据库驱动的配置
    'table'   => env('queue_table'),

    //Redis驱动的配置
    'host'       => env('queue_redis_host'),	// redis 主机ip
    'port'       => env('queue_redis_port'),		// redis 端口
    'password'   => env('queue_redis_password'),		// redis 密码
    'select'     => env('queue_redis_select'),		// 使用哪一个 db，默认为 db0
    'timeout'    => env('queue_redis_timeout'),		// redis连接的超时时间
    'persistent' => env('queue_redis_persistent'),		// 是否是长连接
];