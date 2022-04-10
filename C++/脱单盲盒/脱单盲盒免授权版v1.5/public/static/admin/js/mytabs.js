(function ($) {
    function prev() {
        var width = $(menuTabs).width();
        var scroll_left = $(menuTabs).scrollLeft() - width;
        scroll_left = scroll_left < 0 ? 0 : scroll_left;
        $(menuTabs).animate({
            scrollLeft: scroll_left
        }, 500);
    }
    function next() {
        var width = $(menuTabs).width();
        var scroll_left = $(menuTabs).scrollLeft() + width;
        $(menuTabs).animate({
            scrollLeft: scroll_left
        }, 500);
    }
    function adjustPosition(obj){
        //调整位置
        var scroll_left = $(menuTabs).scrollLeft(),
                offset = $(obj).offset().left - $(menuTabs).offset().left;
        if(offset<0){
            scroll_left = scroll_left + offset;
        }else if(offset > 0){
            var visual_offset = $(menuTabs).width() - $(obj).parent().width();
            if(offset > visual_offset){
                scroll_left = scroll_left + (offset - visual_offset);
            }
        }
        $(menuTabs).animate({
            scrollLeft: scroll_left
        }, 500);
    }
    function openTab() {
        var url = $(this).attr("href"), iftid = $(this).data(iftID), text = $(this).data('title') || $.trim($(this).text()), k = true;
        if (url == undefined || $.trim(url).length == 0) {
            return false;
        }
        $(menuTab).each(function () {
            if ($(this).data("id") == iftid) {
                $(menuTab).removeClass(active);
                $(this).addClass(active);
                var $iframe = findIframeByID(iftid);
                if($iframe){
                    $iframe.attr("src", url);
                    $iframe.show().siblings(iframeClass).hide();
                }
                adjustPosition(this);
                k = false;
                return false;
            }
        });
        if (k) {
            var li = '<li><a href="javascript:;" class="' + active + ' ' + menuTabName + '" data-id="' + iftid + '">' + text + ' <i class="fa fa-times-circle"></i></a></li>';
            $(menuTab).removeClass(active);
            $(menuTabs).append(li);
            var n = '<iframe class="'+iframeName+'" id="iframe_'+iftid+'" name="iframe_' + iftid + '" width="100%" height="100%" src="' + url + '" frameborder="0" data-id="' + iftid + '" seamless></iframe>';
            $(iframeClass).hide();
            $("#iframeWrapper").append(n);
            next();
        }
        return false;
    }
    function findIframeByID(id){
        var $obj = false;
        $(iframeClass).each(function () {
            if ($(this).data("id") == id) {
                $obj = $(this);
                return false;
            }
        });
        return $obj;
    }
    function removeTab() {
        var $menuTab = $(this).parent(), $menuTabWrap = $menuTab.parent();
        var myID = $menuTab.data("id");
        if ($menuTab.hasClass(active)) {
            var $nextMenuTabWrap = $menuTabWrap.next();
            if($nextMenuTabWrap.length){
                var $nextMenuTab = $nextMenuTabWrap.find("a");
                var nextID = $nextMenuTab.data("id");
                $nextMenuTab.addClass(active);
                var $nextIframe = findIframeByID(nextID);
                if($nextIframe){
                    $nextIframe.show().siblings(iframeClass).hide();
                }
            }else{
                var $prevMenuTabWrap = $menuTabWrap.prev();
                var $prevMenuTab = $prevMenuTabWrap.find("a");
                var prevID = $prevMenuTab.data("id");
                $prevMenuTab.addClass(active);
                var $prevIframe = findIframeByID(prevID);
                if($prevIframe){
                    $prevIframe.show().siblings(iframeClass).hide();
                }
            }
        }
        $menuTabWrap.remove();
        var $m = findIframeByID(myID);
        if($m){
            $m.remove();
        }
        return false;
    }
    function switchTab() {
        if (!$(this).hasClass(active)) {
            var id = $(this).data("id");
            var $iframe = findIframeByID(id);
            if($iframe){
                $iframe.show().siblings(iframeClass).hide();
            }
            $(menuTab).removeClass(active);
            $(this).addClass(active);
            //调整位置
            adjustPosition(this);
            return false;
        }
        return false;
    }
    function reload(){
        var id = $(menuTab+'.'+active).data("id");
        document.getElementById("iframe_"+id).contentWindow.location.reload(true);
    }
    var iftID = "iftid",
        menuItem = ".ift-menu-item",
        menuTabPrev = "#iftPrev",
        menuTabNext = "#iftNext",
        reloadBtn = "#iftReload",
        menuTabName = "ift-menu-tab", 
        menuTab = "." + menuTabName,
        active = "active",
        iframeName = "ift-iframe", 
        iframeClass = "." + iframeName,
        menuTabs = "#menuTabs";
        
    $(function () {
        $(menuItem).each(function (i) {
            if (!$(this).data(iftID)){
                $(this).data(iftID, i);
            }
        });
        $(menuItem).on("click", openTab);
        //标签里面的链接加上勾子，第一个加上active
        $(menuTabs).find("a").addClass(menuTabName).removeClass(active).eq(0).addClass(active);
        $(menuTabs).on("click", menuTab + " i", removeTab);
        $(menuTabs).on("click", menuTab, switchTab);
        $(menuTabPrev).on("click", prev);
        $(menuTabNext).on("click", next);
        $(reloadBtn).on("click", reload);
    });
})(jQuery);