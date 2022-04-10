
(function (a, b, c, d) {
    var e = a(b); a.fn.lazyload = function (c) {
        function i() { var b = 0; f.each(function () { var c = a(this); if (h.skip_invisible && !c.is(":visible")) return; if (!a.abovethetop(this, h) && !a.leftofbegin(this, h)) if (!a.belowthefold(this, h) && !a.rightoffold(this, h)) c.trigger("appear"), b = 0; else if (++b > h.failure_limit) return !1 }) } var f = this, g,
h = { threshold: 0, failure_limit: 0, event: "scroll", effect: "show", container: b, data_attribute: "original", skip_invisible: !0, appear: null, load: null };
        return c && (d !== c.failurelimit && (c.failure_limit = c.failurelimit, delete c.failurelimit), d !== c.effectspeed && (c.effect_speed = c.effectspeed, delete c.effectspeed), a.extend(h, c)), g = h.container === d || h.container === b ? e : a(h.container), 0 === h.event.indexOf("scroll") && g.bind(h.event, function (a) { return i() }), this.each(function () { var b = this, c = a(b); b.loaded = !1, c.one("appear", function () { if (!this.loaded) { if (h.appear) { var d = f.length; h.appear.call(b, d, h) } a("<img />").bind("load", function () { c.hide().attr("src", c.data(h.data_attribute))[h.effect](h.effect_speed), b.loaded = !0; var d = a.grep(f, function (a) { return !a.loaded }); f = a(d); if (h.load) { var e = f.length; h.load.call(b, e, h) } }).attr("src", c.data(h.data_attribute)) } }), 0 !== h.event.indexOf("scroll") && c.bind(h.event, function (a) { b.loaded || c.trigger("appear") }) }), e.bind("resize", function (a) { i() }), /iphone|ipod|ipad.*os 5/gi.test(navigator.appVersion) && e.bind("pageshow", function (b) { b.originalEvent.persisted && f.each(function () { a(this).trigger("appear") }) }), a(b).load(function () { i() }), this
    }, a.belowthefold = function (c, f) { var g; return f.container === d || f.container === b ? g = e.height() + e.scrollTop() : g = a(f.container).offset().top + a(f.container).height(), g <= a(c).offset().top - f.threshold }, a.rightoffold = function (c, f) { var g; return f.container === d || f.container === b ? g = e.width() + e.scrollLeft() : g = a(f.container).offset().left + a(f.container).width(), g <= a(c).offset().left - f.threshold }, a.abovethetop = function (c, f) { var g; return f.container === d || f.container === b ? g = e.scrollTop() : g = a(f.container).offset().top, g >= a(c).offset().top + f.threshold + a(c).height() }, a.leftofbegin = function (c, f) { var g; return f.container === d || f.container === b ? g = e.scrollLeft() : g = a(f.container).offset().left, g >= a(c).offset().left + f.threshold + a(c).width() }, a.inviewport = function (b, c) { return !a.rightoffold(b, c) && !a.leftofbegin(b, c) && !a.belowthefold(b, c) && !a.abovethetop(b, c) }, a.extend(a.expr[":"], { "below-the-fold": function (b) { return a.belowthefold(b, { threshold: 0 }) }, "above-the-top": function (b) { return !a.belowthefold(b, { threshold: 0 }) }, "right-of-screen": function (b) { return a.rightoffold(b, { threshold: 0 }) }, "left-of-screen": function (b) { return !a.rightoffold(b, { threshold: 0 }) }, "in-viewport": function (b) { return a.inviewport(b, { threshold: 0 }) }, "above-the-fold": function (b) { return !a.belowthefold(b, { threshold: 0 }) }, "right-of-fold": function (b) { return a.rightoffold(b, { threshold: 0 }) }, "left-of-fold": function (b) { return !a.rightoffold(b, { threshold: 0 }) } })
})(jQuery, window, document)
//////////////////////////////////////////////////////

var ieVersion = function () {
    var ver = 100,
    ie = (function () {
        var undef,
            v = 3,
            div = document.createElement('div'),
            all = div.getElementsByTagName('i');
        while (
            div.innerHTML = '<!--[if gt IE ' + (++v) + ']><i></i><![endif]-->',
            all[0]
        );
        return v > 4 ? v : undef;
    }());
    if (ie) ver = ie;
    return ver;
}

window.alert = function (font) {
   layer.open({
        title:'提示'
        ,skin: 'msg'
        ,content: font
        ,btnAlign: 'c' //按钮居中 
        ,shade: 0 //不显示遮罩
        ,btn: '确定'
       //time: 2
   });
   //pub.clearTipStyle(false);
   //layer.msg('玩命提示中');
}

var isIe = (window.ActiveXObject) ? true : false;
//弹出窗

/*弹出登陆窗口*/
var isIE6 = ieVersion() == "6";
(function ($) {
    $.fn.decorateIframe = function (options) {

        if (isIE6) {
            var opts = $.extend({}, $.fn.decorateIframe.defaults, options);
            $(this).each(function () {
                var $myThis = $(this);
                //创建一个IFRAME
                var divIframe = $("<iframe style=\"border:none\" />");
                divIframe.attr("id", opts.iframeId);
                divIframe.css({ "position": "absolute", "display": "block", "z-index": opts.iframeZIndex, "top": 0, "left": 0 });
                if (opts.width == 0) {
                    divIframe.css("width", $myThis.width() + parseInt($myThis.css("padding")) * 2 + "px");
                }
                if (opts.height == 0) {
                    divIframe.css("height", $myThis.height() + parseInt($myThis.css("padding")) * 2 + "px");
                }
                divIframe.css("filter", "mask(color=#fff)");
                $myThis.append(divIframe);
            });
        }
    }
    $.fn.decorateIframe.defaults = {
        iframeId: "decorateIframe1",
        iframeZIndex: -1,
        width: 0,
        height: 0
    }
})(jQuery);

(function ($) {
    $.fn.popwindow = function (cssOptions, data) {
        $("#Overlay").fadeOut().remove();
        var cssOptions = $.extend({}, cssOptions);

        if (this.context) {
            $(this).click(function () {
                open(this);
                return false;
            });
        } else {
            open(null);
        }

        function open(e) {
            html = [];
            html.push();

            var url = "";
            if (typeof (data.href) != "undefined") {
                url = data.href;
            }


            html.push("<div id=\"Overlay\">");
            if (cssOptions.title) {
                html.push("<div class=\"KmainBox\">");
                html.push("<h2 class=\"msgboxhead\">");
                html.push("    <span>" + cssOptions.title + "</span> ");
                html.push("    <a style=\"color: #fff;\" href=\"#\" class=\"close\">关闭</a></h2>");
            }
            if (url.length > 0) {
                html.push("<iframe id=\"LoadedContent\" frameborder=\"0\"></iframe>");
            }
            else {
                html.push("<div id=\"LoadedContent\" frameborder=\"0\"></div>");
            }
            if (cssOptions.title) {
                html.push("</div>");
            }
            html.push("</div>");
            $("body").prepend(html.join(""));

            if (!data.noOverlayClose) {
                $("#Overlay").click(function () { $(this).remove(); });
            }
            $("#Overlay").decorateIframe();
            var $LoadedContent = $("#LoadedContent");

            // url += "&t=" + Math.random();
            if (url.length > 0) {
                $LoadedContent.attr("src", url);
            }
            else {
                $LoadedContent.html(data.html);
            }

            $("#Overlay").children().eq(0).css(cssOptions);
            windowresize();

            $("#Overlay .close").click(function () {
                $("#Overlay").fadeOut().remove();
                return false;
            });
        }
    }

    $.fn.popwindow.close = function () {
        $("#Overlay").fadeOut().remove();

    }

    $.fn.popwindow.resize = function (css) {
        $("#LoadedContent").css(css);
    }


    function windowresize() {
        var $LoadedContent = $("#LoadedContent");

        if ($LoadedContent.length > 0) {
            if (isIE6) {
                $("body").css("position", "static");
                $("#Overlay").css({
                    position: "absolute",
                    width: $(window).width(),
                    height: $(window).height(),
                    top: $(window).scrollTop()
                });
                $(window).scroll(function () {

                    $("#Overlay").css({ top: $(window).scrollTop() });
                });
            } else {
                $("#Overlay").css({ position: "fixed" });
            }
            var position = {
                marginLeft: ($(window).width() - $LoadedContent.width()) / 2, //272
                marginTop: ($(window).height() - $LoadedContent.height()) / 2
            };

            $("#Overlay").children().eq(0).css(position);
        }
    }
    $(window).resize(windowresize);
})(jQuery);


//div滚动
(function ($) {
    $.fn.slideBox = function (options) {
        var defaults = { duration: 3000, delay: 5000, speed: 500, effect: "fade" };
        var opts = $.extend(defaults, options || {});
        var obj = $(this);
        var currentIndex = 1;
        var isDone = true;
        var myPlayInterval;
        var myPlayTimeOut;
        var start = function () { window.clearInterval(myPlayInterval); myPlayTimeOut = window.setTimeout(goAutoPlayBox, opts.duration); }
        var goAutoPlayBox = function () {
            myPlayInterval = window.setInterval(function () {
                var itemCount = $(".playPages .page", obj).length;
                var nextIndex = currentIndex < itemCount ? currentIndex * 1 + 1 : 1;
                yPlayMove("next", nextIndex);
            }, opts.duration);
        }
        var yPlayMove = function (nextOrPre, nextIndex) {
            if (isDone && currentIndex != nextIndex) {
                window.clearInterval(myPlayInterval);
                window.clearTimeout(myPlayTimeOut);
                isDone = false;
                var item = $(".playPages .page[pageNum='" + currentIndex + "']", obj);
                var width = $(item).width();
                var height = $(item).height();
                var itemLeft = "-" + width + "px";
                var itemTop = "-" + height + "px";
                var nextItemLeft = width + "px";
                var nextItemTop = height + "px";
                if (nextOrPre == "pre") {
                    itemLeft = width + "px";
                    nextItemLeft = "-" + width + "px";
                }

                var nextItem = $(".playPages .page[pageNum='" + nextIndex + "']", obj);
                currentIndex = nextIndex;
                $(".playPageNums .item", obj).removeClass("curr");
                $(".playPageNums .item[pageNum='" + currentIndex + "']", obj).addClass("curr");

                if (opts.effect == "top") {//向下滑动
                    item.animate({ top: itemTop }, opts.speed, function () { item.css({ "top": "0px" }).hide() })
                    nextItem.css({ top: nextItemTop }).show().animate({ top: "0px" }, opts.speed, function () { isDone = true; start(); })
                } else if (opts.effect == "fade") {//fade效果
                    item.fadeOut(opts.speed).css({ "left": "0px" });
                    nextItem.css({ "left": "0px" }).fadeIn(opts.speed, function () { isDone = true; start(); })
                } else {//水平
                    item.animate({ left: itemLeft }, opts.speed, function () { item.css({ "left": "0px" }).hide() })
                    nextItem.css({ left: nextItemLeft }).show().animate({ left: "0px" }, opts.speed, function () { isDone = true; start(); })
                }
            }
        }
        var init = function () {
            $(obj).on("mouseover click", ".playPageNums .item", function () {
                var pageIndex = $(this).attr("pageNum");
                var nextOrPre = pageIndex > currentIndex ? "next" : "pre";
                window.clearInterval(myPlayInterval);
                window.clearTimeout(myPlayTimeOut);
                if (pageIndex != currentIndex) {
                    yPlayMove(nextOrPre, pageIndex);
                }
            })

            var btnnext = $(".btnnext", obj);
            if (btnnext.length > 0) {
                $(".btnnext", obj).click(function () {
                    var itemCount = $(".playPages .page", obj).length; var nextIndex = currentIndex < itemCount ? currentIndex * 1 + 1 : 1; yPlayMove("next", nextIndex);
                    return false;
                });
            }
            var btnprev = $(".btnprev", obj);
            if (btnprev.length > 0) {

                $(".btnprev", obj).click(function () {
                    var itemCount = $(".playPages .page", obj).length; var nextIndex = currentIndex > 1 ? currentIndex * 1 - 1 : itemCount; yPlayMove("pre", nextIndex);

                });
            }
            $(".page", obj).hover(function () {
                window.clearInterval(myPlayInterval); window.clearTimeout(myPlayTimeOut);
            }, function () { start(); })

            if ($(".playPages", obj).length > 0) {
                myPlayTimeOut = window.setTimeout(start, opts.delay);

            }
        }
        $(function () { init(); });

    }

    $.fn.CBDhover = function (options) {
        var defaults = { hoverTime: 200, outTime: 200, hover: function (dom) { $.noop(); }, out: function (dom) { $.noop(); } };
        var sets = $.extend(defaults, options || {});
        var hoverTimer, outTimer;
        return $(this).each(function () {
            $(this).hover(function () {
                clearTimeout(outTimer);
                var current = $(this);
                hoverTimer = setTimeout(function () { sets.hover(current); }, sets.hoverTime);
            },
                 function () {
                     clearTimeout(hoverTimer);
                     var current = $(this);
                     outTimer = setTimeout(function () { sets.out(current); }, sets.outTime);
                 });
        });
    },
    $.fn.imgScroll = function (options) {
        return this.each(function () {

            var e = $.extend({ showItemCount: 5, speed: 300 }, options);
            var itemBox = $(this);
            var ul = $("ul", itemBox);
            var lis = $("li", ul);
            var lisCount = lis.length;
            var isInAnmate = false;
            if (lisCount > 0) {
                //有数据              
                var itemWidth = parseInt($(lis[0]).outerWidth());
                var ULwidth = itemWidth * lis.length;
                ul.css({ width: ULwidth + "px" });
                var displayWidth = e.showItemCount * itemWidth;

                $(".prev", itemBox).click(function () {                   //向左移          
                    if ($(this).hasClass("disable")) {
                        return;
                    }

                    if (isInAnmate)
                        return;

                    var currentLeft = parseInt($(ul).css("left"));
                    currentLeft = isNaN(currentLeft) ? 0 : currentLeft;
                    var left = e.showItemCount * itemWidth;
                    var goLeft = currentLeft + left;

                    if (goLeft <= 0) {
                        isInAnmate = true;
                        ul.animate({ left: goLeft + "px" }, e.speed, function () { checkBtn(); isInAnmate = false; })
                    }

                })

                $(".next", itemBox).click(function () {                    //向左移

                    if ($(this).hasClass("disable")) {
                        return;
                    }
                    if (isInAnmate)
                        return;
                    var currentLeft = parseInt($(ul).css("left"));
                    currentLeft = isNaN(currentLeft) ? 0 : currentLeft;
                    var left = displayWidth;
                    var goLeft = (currentLeft + (left * -1));

                    if (ULwidth > (goLeft * -1)) {


                        isInAnmate = true;
                        ul.animate({ left: goLeft + "px" }, e.speed, function () { checkBtn(); isInAnmate = false; })
                    }

                })

                function checkBtn() {

                    var currentLeft = parseInt($(ul).css("left"));
                    currentLeft = isNaN(currentLeft) ? 0 : currentLeft;

                    if (currentLeft == 0) {
                        $(".prev", itemBox).addClass("disable");

                    }
                    else {
                        $(".prev", itemBox).removeClass("disable");
                    }

                    if (ULwidth - (currentLeft * -1) <= displayWidth) {
                        $(".next", itemBox).addClass("disable");
                    }
                    else {
                        $(".next", itemBox).removeClass("disable");
                    }
                }

                checkBtn();

            }

        })
    }
})(jQuery);


//  $("#scrollDiv").TxtScroll({ line: 1, speed: 500, timer: 3000, up: "", down: "" });
(function ($) {
    $.fn.extend({
        TxtScroll: function (opt, callback) {
            //参数初始化
            if (!opt) var opt = {};
            var _btnUp = $("#" + opt.up); //Shawphy:向上按钮
            var _btnDown = $("#" + opt.down); //Shawphy:向下按钮
            var timerID;
            var _this = this.eq(0).find("ul:first");
            var lineH = _this.find("li:first").height(), //获取行高
                        line = opt.line ? parseInt(opt.line, 10) : parseInt(this.height() / lineH, 10), //每次滚动的行数，默认为一屏，即父容器高度
                        speed = opt.speed ? parseInt(opt.speed, 10) : 500; //卷动速度，数值越大，速度越慢（毫秒）
            timer = opt.timer //?parseInt(opt.timer,10):3000; //滚动的时间间隔（毫秒）
            if (line == 0) line = 1;
            var upHeight = 0 - line * lineH;
            //滚动函数
            var scrollUp = function () {
                _btnUp.unbind("click", scrollUp); //Shawphy:取消向上按钮的函数绑定
                _this.animate({
                    marginTop: upHeight
                }, speed, function () {
                    for (i = 1; i <= line; i++) {
                        _this.find("li:first").appendTo(_this);
                    }
                    _this.css({ marginTop: 0 });
                    _btnUp.bind("click", scrollUp); //Shawphy:绑定向上按钮的点击事件
                });

            }
            //Shawphy:向下翻页函数
            var scrollDown = function () {
                _btnDown.unbind("click", scrollDown);
                for (i = 1; i <= line; i++) {
                    _this.find("li:last").show().prependTo(_this);
                }
                _this.css({ marginTop: upHeight });
                _this.animate({
                    marginTop: 0
                }, speed, function () {
                    _btnDown.bind("click", scrollDown);
                });
            }
            //Shawphy:自动播放
            var autoPlay = function () {
                if (timer) timerID = window.setInterval(scrollUp, timer);
            };
            var autoStop = function () {
                if (timer) window.clearInterval(timerID);
            };
            //鼠标事件绑定
            _this.hover(autoStop, autoPlay).mouseout();
            _btnUp.css("cursor", "pointer").click(scrollUp).hover(autoStop, autoPlay); //Shawphy:向上向下鼠标事件绑定
            _btnDown.css("cursor", "pointer").click(scrollDown).hover(autoStop, autoPlay);

        }
    })
})(jQuery);
function ClosePop() {

    $("#Overlay,#dailog").fadeOut().remove();


}


var CBDtools = {
    //**************************************************************************************************cookies操作
    //value:Cookie的值，expiresMM：有效时间（过期时间--分钟）,name:名称（必填）,key:键 可以不输入或为空
    //encodeURI==>Server.URLEncode
    setCookie: function (value, expiresMM, name, key) {

        var exp = new Date();
        exp.setTime(exp.getTime() + expiresMM * 60 * 1000);
        if (key == null || key == "") {
            document.cookie = name + "=" + encodeURI(value) + ";expires=" + exp.toGMTString() + ";path=/";
        }
        else {
            var nameValue = this.getCookie(name);
            if (nameValue == "") {
                document.cookie = name + "=" + key + "=" + encodeURI(value) + ";expires=" + exp.toGMTString() + ";path=/";
            }
            else {
                var keyValue = this.getCookie(name, key);

                if (keyValue != "") {
                    nameValue = nameValue.replace(key + "=" + keyValue, key + "=" + encodeURI(value));
                    document.cookie = name + "=" + nameValue + ";expires=" + exp.toGMTString() + ";path=/";
                }
                else {
                    document.cookie = name + "=" + nameValue + "&" + key + "=" + encodeURI(value) + ";expires=" + exp.toGMTString() + ";path=/";
                }
            }
        }
    },
    //读取cookies
    getCookie: function (name, key) {
        var nameValue = "";
        var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
        if (arr = document.cookie.match(reg)) {
            nameValue = decodeURI(arr[2]);
        }
        if (key != null && key != "") {
            reg = new RegExp("(^| |&)" + key + "=([^(;|&|=)]*)(&|$)");
            if (arr = nameValue.match(reg)) {

                return decodeURI(arr[2]);

            }
            else return "";
        }
        else {
            return nameValue;
        }
    },
    //删除cookies
    delCookie: function (name) {
        var exp = new Date();
        exp.setTime(exp.getTime() - 1);
        var cval = this.getCookie(name);
        if (cval != null) document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
    },
    //**************************************************************************************************cookies操作
    //URL参数
    getParam: function (paras) {
        var url = location.href;
        var paraString = url.substring(url.indexOf("?") + 1, url.length).split("&");
        var paraObj = {}
        for (i = 0; j = paraString[i]; i++) {
            paraObj[j.substring(0, j.indexOf("=")).toLowerCase()] = j.substring(j.indexOf("=") + 1, j.length);
        }
        var returnValue = paraObj[paras.toLowerCase()];
        if (typeof (returnValue) == "undefined") {
            return "";
        } else {
            return returnValue;
        }
    },
    //加载JS文件
    loadScript: function (script_filename) {
        document.write('<' + 'script');
        document.write(' language="javascript"');
        document.write(' type="text/javascript"');
        document.write(' src="' + script_filename + '">');
        document.write('</' + 'script' + '>');
    },
    //等比缩小图片
    DrawImage: function (ImgD, FitWidth, FitHeight) {
        var image = new Image();
        image.src = ImgD.src;
        if (image.width > 0 && image.height > 0) {
            if (image.width / image.height >= FitWidth / FitHeight) {
                if (image.width > FitWidth) {
                    ImgD.width = FitWidth;
                    ImgD.height = (image.height * FitWidth) / image.width;
                } else {
                    ImgD.width = image.width;
                    ImgD.height = image.height;
                }
            }
            else {
                if (image.height > FitHeight) {
                    ImgD.height = FitHeight;
                    ImgD.width = (image.width * FitHeight) / image.height;
                } else {
                    ImgD.width = image.width;
                    ImgD.height = image.height;
                }
            }
        }
    },

    OpenWindow: function (_href, _width, _height, _title, _noOverlayBoxClose, _html) {

        $.fn.popwindow({ width: _width, height: _height, title: _title }, { href: _href, noOverlayClose: _noOverlayBoxClose, html: _html });
    },
    CloseWindow: function () {

        $.fn.popwindow.close();
    },
    isLogin: function (callBack, c) {

        var d = "/ajax/IsLogined.aspx";
        var b = [];
        if (c != null && c.length > 0) { b.push("skuID=" + c) }
        if (b.length > 0) { d = d + "?" + b.join("&") }
        $.getScript(d, callBack)
    },
    showLoginPop: function (callBack) {

        CBDtools.OpenWindow("/Ajax/Pop/Login.aspx?callBack=" + callBack + "&r=" + Math.random(), 600, 500, "登录/注册", true, "");

    },
    showLoginTipPop: function (callBack) {



        CBDtools.OpenWindow("/Ajax/Pop/LoginTip.aspx?callBack=" + callBack + "&r=" + Math.random(), 665, 230, "登录/注册", true, "");

    }

}




function closeWindowBase(windowId) {
    $("#" + windowId).remove();
}
function closeWindow() {
    closeWindowBase("mesWindow")
}







function CBDtogglePop(Trigger, Parent, ParentToggleClass, Target) {
    $(document).delegate(Trigger, "mouseenter", function () { var h = $(this), g = h.parents(Parent), f = g.siblings(), e = g.find(Target); clearTimeout(g[0].timer); g[0].timer = null; clearTimeout(h[0].atimer); h[0].atimer = null; h[0].atimer = setTimeout(function () { f.removeClass(ParentToggleClass); g.addClass(ParentToggleClass); e.show() }, 200) });
    $(document).delegate(Target, "mouseenter", function () { var e = $(this), g = e.parents(Parent), f = g.siblings(); clearTimeout(g[0].timer); g[0].timer = null; f.removeClass(ParentToggleClass); g.addClass(ParentToggleClass); });
    $(document).delegate(Target, "mousemove", function () { var e = $(this), g = e.parents(Parent), f = g.siblings(); clearTimeout(g[0].timer); g[0].timer = null; f.removeClass(ParentToggleClass); g.addClass(ParentToggleClass); });
    $(document).delegate(Trigger, "mouseleave", function () { var g = $(this), f = g.parents(Parent), e = f.find(Target); clearTimeout(g[0].atimer); g[0].atimer = null; clearTimeout(f[0].timer); f[0].timer = null; f[0].timer = setTimeout(function () { e.hide(); f.removeClass(ParentToggleClass) }, 100) });
    $(document).delegate(Target, "mouseleave", function () { var e = $(this), f = e.parents(Parent); clearTimeout(f[0].timer); f[0].timer = null; f[0].timer = setTimeout(function () { e.hide(); f.removeClass(ParentToggleClass) }, 100) })
}



function scrollToObject(obj) {

    var target = $(obj);
    if (target.length == 0) {
        return;
    }
    var top = target.offset().top - 80;
    $("html, body").animate({ scrollTop: top + "px" }, { duration: 200, easing: "swing" });

    var row = target.parents(".booth-form-row, .media_reg tr");
    if (row.length > 0) {

        for (var i = 0; i < 4; i++) {

            window.setTimeout(function () {
                if (row.hasClass("row-error-style")) {
                    row.removeClass("row-error-style")

                }
                else {
                    
                    row.addClass("row-error-style")
                }
            }, (i + 1) * 500);
        }


    }

}





$(function () {
    $(".media_reg .btn_submit").html("提交").removeAttr("disabled")
})
$(document).on("click", ".media_reg .btn_submit", function () {

    var btn = $(this);
    var form = $(this).parents(".media_reg");

    var languange = "cn";
    var txtMedia_name = form.find("#txtMedia_name").val();
    var txtName = form.find("#txtName").val();
    var txtPosition = form.find("#txtPosition").val();
    var txtPhone = form.find("#txtPhone").val();
    var txtMobile = form.find("#txtMobile").val();
    var txtEmail = form.find("#txtEmail").val();
    var txtAddress = form.find("#txtAddress").val();
    var media_nature = "";
    form.find("input[name='media_nature']:checked").each(function (index, item) {
        var val = $(item).val();
        media_nature += (media_nature.length > 0 ? "," : "") + val;
    });
    var sections_other = form.find("input[name='sections_other']").val();

    var media_nature_other = form.find("#media_nature_other").val();
    var txtRemark = form.find("#txtRemark").val();

    $(this).attr("disabled", "disabled").html("正在提交...");

    var postData = {
        "languange": languange,
        "txtMedia_name": txtMedia_name,
        "txtName": txtName,
        "txtPosition": txtPosition,
        "txtPhone": txtPhone,
        "txtMobile": txtMobile,
        "txtEmail": txtEmail,
        "txtAddress": txtAddress,
        "media_nature": media_nature,
        "media_nature_other": media_nature_other, "txtRemark": txtRemark
    };



    $.ajax({
        url: "/ajax/index.aspx?action=submitMediaReg",
        type: "post",
        data: postData,
        dataType: "json",
        success: function (data) {
            btn.removeAttr("disabled").html("提交");
            if (data.msgType == 1) {
                //alert(data.msg);

                form.find("#txtMedia_name").val("");
                form.find("#txtName").val("");
                form.find("#txtPosition").val("");
                form.find("#txtPhone").val("");
                form.find("#txtMobile").val("");
                form.find("#txtEmail").val("");
                form.find("#txtAddress").val("");

                form.find("input[name='media_nature']").prop("checked", false);

                window.location.href = "/media/media_registration_success/";
                // $('.title2-row,.media_reg').hide();
                // $('.content2-row').removeClass('content2-row')
                // $('.succeed-row').show();
            }
            else {
                //alert(data.msg);
                layer.msg(data.msg);
                scrollToObject(data.data);
            }
         
        }
    })
})

// function scrollToObject(obj) {
 
//     var target = $(obj);
//     if (target.length == 0)
//     {
//         return;
//      }
//     var top = target.offset().top - 20;
//     $("html, body").animate({ scrollTop: top + "px" }, { duration: 200, easing: "swing" });

//     var row = target.parents(".form-row");
//     if (row.length > 0)
//     {
   
//         for (var i = 0; i <4; i++)
//         {
            
//             window.setTimeout(function () {
//                 if (row.hasClass("row-error-style"))
//                 {
//                     row.removeClass("row-error-style")
//                 }
//                 else {
              
//                     row.addClass("row-error-style")
//                 }
//             }, (i+1)* 500);
//         }
        

//     }

// }