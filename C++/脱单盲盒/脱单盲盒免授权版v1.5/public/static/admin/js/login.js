$(function(){
    var Jinp = $(".J-input");
    Jinp.focus(function(){
        $(this).next().addClass("curr");
    });
    Jinp.blur(function(){
        if(!$(this).val()){
            $(this).next().removeClass("curr");
        }
    });
    Jinp.change(function(){
        $(this).next().addClass("curr");
    });
});
