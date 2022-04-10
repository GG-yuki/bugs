
CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
        
        config.customConfig = 'content.js';
        
//	config.language = 'zh-cn';
//
//	//恢复右键菜单
//        config.extraPlugins = 'sourcedialog,tableresizerowandcolumn,quicktable,tabletoolstoolbar,lineheight,uploadimage';
//        config.removePlugins= 'sourcearea';
//        
//	//删除某个对话框
//	config.removeDialogTabs = 'image:advanced;link:advanced';
//	//粘贴为纯文本
//	config.forcePasteAsPlainText = true;
//        
//	//禁止显示 所见即所得编辑器 的提示
////	config.title = false;	
//        //图片上传接口
//        config.filebrowserUploadMethod = 'form';
//        config.filebrowserUploadUrl  = "/admin.php/Editor/uploadimage";
//        //粘贴图片上传接口
//        config.imageUploadUrl  = "/admin.php/Editor/uploadimagebypaste";
//        //文本格式过滤
//        config.allowedContent = true;
//        config.fontSize_sizes = "12/12px;13/13px;14/14px;16/16px;18/18px;20/20px;22/22px;24/24px;26/26px;28/28px;30/30px";
//        //定制行间距
//        config.line_height = "1;1.5;2;2.5;3;3.5;4;4.5;5";
};
