(function(e) {
    $.fn.funnyNewsTicker = function(e) {
        var t = {
            width: "100%",
            modulid: "funnyNewsTicker",
            autoplay: true,
            timer: 3e3,
            titlecolor: "#333",
            titlefontsize: "16px",
            itembgcolor: "#FFF",
            contentlinkcolor: "#099",
            infobgcolor: "#f2f2f2",
            bordercolor: "#DDD",
            itemheight: 130,
            infobarvisible: true,
            btnfacebook: true,
            btntwitter: true,
            btngoogleplus: true,
            btnlinkbutton: true,
            btnlinktarget: "_blank",
            pagecountvisible: true,
            buttonstyle: "black",
            pagenavi: true,
            pagenavistyle: "black",
            feed: false,
            feedcount: 100
        };
        var e = $.extend(t, e);
        return this.each(function() {
            function o() {
                function o() {
                    $(e.modulid + ">div").css({
                        left: ($(e.modulid).width() - 30) / 2
                    })
                }

                function u() {
                    $(e.modulid + " ul li").eq(r[0]).addClass("fnt-top0");
                    $(e.modulid + " ul li").eq(r[1]).addClass("fnt-top1");
                    $(e.modulid + " ul li").eq(r[2]).addClass("fnt-top2");
                    $(e.modulid + " ul li").eq(r[3]).addClass("fnt-active");
                    $(e.modulid + " ul li").eq(r[4]).addClass("fnt-bottom2");
                    $(e.modulid + " ul li").eq(r[5]).addClass("fnt-bottom1");
                    $(e.modulid + " ul li").eq(r[6]).addClass("fnt-bottom0")
                }

                function a() {
                    t--;
                    if (t < 0) t = n;
                    l()
                }

                function f() {
                    t++;
                    if (t == n + 1) t = 0;
                    l()
                }

                function l() {
                    $(e.modulid + " ul li").attr("class", "");
                    if (t == 0) {
                        r[0] = n - 2;
                        r[1] = n - 1;
                        r[2] = n;
                        r[3] = t;
                        r[4] = t + 1;
                        r[5] = t + 2;
                        r[6] = t + 3
                    } else if (t == 1) {
                        r[0] = n - 1;
                        r[1] = n;
                        r[2] = t - 1;
                        r[3] = t;
                        r[4] = t + 1;
                        r[5] = t + 2;
                        r[6] = t + 3
                    } else if (t == 2) {
                        r[0] = n;
                        r[1] = t - 2;
                        r[2] = t - 1;
                        r[3] = t;
                        r[4] = t + 1;
                        r[5] = t + 2;
                        r[6] = t + 3
                    } else if (t == n) {
                        r[0] = n - 3;
                        r[1] = n - 2;
                        r[2] = n - 1;
                        r[3] = t;
                        r[4] = 0;
                        r[5] = 1;
                        r[6] = 2
                    } else if (t == n - 1) {
                        r[0] = n - 4;
                        r[1] = n - 3;
                        r[2] = n - 2;
                        r[3] = t;
                        r[4] = t + 1;
                        r[5] = 0;
                        r[6] = 1
                    } else if (t == n - 2) {
                        r[0] = n - 5;
                        r[1] = n - 4;
                        r[2] = n - 3;
                        r[3] = t;
                        r[4] = t + 1;
                        r[5] = t + 2;
                        r[6] = 0
                    } else {
                        r[0] = t - 3;
                        r[1] = t - 2;
                        r[2] = t - 1;
                        r[3] = t;
                        r[4] = t + 1;
                        r[5] = t + 2;
                        r[6] = t + 3
                    }
                    u()
                }
                $(e.modulid + " ul li").css({
                    height: e.itemheight,
                    background: e.itembgcolor,
                    color: e.titlecolor,
                    "font-size": e.titlefontsize
                });
                $(e.modulid + " ul li").each(function(t, r) {
                    if (e.infobarvisible) {
                        i = '<div class="fnt-info" style="background:' + e.infobgcolor + "; border-color:" + e.bordercolor + ';">';
                        if (e.btnfacebook) i = i + '<a data-type="facebook" data-url="' + $(this).find(".fnt-content").attr("data-link") + '" data-text="' + $(this).find(".fnt-content").text() + '" class="fnt-easing2 fnt-facebook-' + e.buttonstyle + '"></a>';
                        if (e.btntwitter) i = i + '<a data-type="twitter" data-url="' + $(this).find(".fnt-content").attr("data-link") + '" data-text="' + $(this).find(".fnt-content").text() + '" class="fnt-easing2 fnt-twitter-' + e.buttonstyle + '"></a>';
                        if (e.btngoogleplus) i = i + '<a data-type="google" data-url="' + $(this).find(".fnt-content").attr("data-link") + '" data-text="' + $(this).find(".fnt-content").text() + '" class="fnt-easing2 fnt-google-' + e.buttonstyle + '"></a>';
                        if (e.pagecountvisible) i = i + "<span>" + ($(this).index() + 1) + " / " + (n + 1) + "</span>";
                        if (e.btnlinkbutton) i = i + '<a href="' + $(this).find(".fnt-content").attr("data-link") + '" class="fnt-easing2 fnt-link-' + e.buttonstyle + '" target="' + e.btnlinktarget + '"></a>';
                        i = i + "</div>"
                    }
                    $(this).append(i)
                });
                $(e.modulid + " ul li .fnt-content").find("a").css({
                    color: e.contentlinkcolor
                });
                $(e.modulid + " ul li").click(function(e) {
                    t = $(this).index();
                    l()
                });
                o();
                $(window).resize(function(e) {
                    o()
                });
                u();
                if (e.autoplay) {
                    s = setInterval(function() {
                        f()
                    }, e.timer);
                    $(e.modulid).hover(function() {
                        clearInterval(s)
                    }, function() {
                        s = setInterval(function() {
                            f()
                        }, e.timer)
                    })
                }
            }
            e.modulid = "#" + $(this).attr("id");
            var t = 0;
            var n = $(e.modulid + " ul li").length - 1;
            var r = [n - 2, n - 1, n, t, t + 1, t + 2, t + 3];
            var i = "";
            var s = e.modulid;
            if (e.feed != false) {
                $(e.modulid + " ul").html("");
                $(e.modulid + " ul").append('<li class="fnt-active"><div class="fnt-content">Rss Feed Loading...</div></li>');
                u()
            } else {
                o()
            }
        })
    }
})(jQuery)