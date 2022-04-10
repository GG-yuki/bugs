$(function(){

	var codeArray = [];
	$("pre").each(function(i,v){
		codeArray.push($(v).html());
	})
	//复制代码到剪切板
	$(".J-copy").each(function(i){
	    var txt = codeArray[i].replace(/&lt;/g,"<").replace(/&gt;/g,">");
		if(window.clipboardData){
			$(this).html('<img src="../images/icon_copy.gif" style="cursor:pointer" />');
			$(this).click(function(){
				 window.clipboardData.setData("Text",txt);
				 alert("\u4ee3\u7801\u5df2\u88ab\u590d\u5236\u5230\u526a\u5207\u677f\uff01")//代码已被复制到剪切板！
			});
		}else{
			$(this).html('<embed height="15" width="14"  type="application/x-shockwave-flash" allowscriptaccess="never" quality="high" flashvars="clipboard=' + encodeURIComponent(txt) + '" src="../js/clipboard_new.swf" wmode="transparent">');			
			$(this).mouseup(function(){
				alert("\u4ee3\u7801\u5df2\u88ab\u590d\u5236\u5230\u526a\u5207\u677f\uff01")//代码已被复制到剪切板！
			});
		}
	})
	//语法高亮
	SyntaxHighlighter.all({"toolbar":false,"quick-code":false});
})