
CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
        
        //文本格式过滤
        config.allowedContent = {
            $1: {
                elements: CKEDITOR.dtd,
                attributes: true,
                styles: true,
                classes: true
            }
        };
        config.disallowedContent = 'script; iframe; img{width,height}';
        //允许空标签i,span
        config.protectedSource.push(/<i[^>]*><\/i>/g);
        config.protectedSource.push(/<span[^>]*><\/span>/g);
        
	config.language = 'zh-cn';

        config.toolbarGroups = [
            { name: 'document', groups: [ 'mode' ] },
            { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
            { name: 'insert', groups: [ 'insert' ] },
            { name: 'links', groups: [ 'links' ] },
            { name: 'tools', groups: [ 'tools' ] },
            '/',
            { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
            { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
            '/',
            { name: 'styles', groups: [ 'styles' ] },
            { name: 'colors', groups: [ 'colors' ] },
            { name: 'tables', groups: ['tablerow', 'tablecolumn', 'tablecell', 'tablecellmergesplit']}
            
        ];
        config.removeButtons = "Preview,Styles,Format";
        
        config.width = 800;
        config.height = 600;
    //视频接口
    config.extraPlugins = 'html5video';
    config.uploadUrl = 'https://api.net/api/ECategoryDetail/UploadImg';
	//恢复右键菜单
        config.extraPlugins = 'tableresizerowandcolumn,quicktable,tabletoolstoolbar,lineheight,uploadimage,html5video';
        config.removePlugins= '';
        
	//删除某个对话框
	config.removeDialogTabs = 'image:advanced;link:advanced';
	//粘贴为纯文本
	config.forcePasteAsPlainText = true;

	//禁止显示 所见即所得编辑器 的提示
        //图片上传接口
        config.filebrowserUploadMethod = 'form';
        config.filebrowserUploadUrl  = "/admin/Editor/uploadimage";
        //粘贴图片上传接口
        config.imageUploadUrl  = "/admin/Editor/uploadimagebypaste";
        
        config.fontSize_sizes = "12/12px;13/13px;14/14px;16/16px;18/18px;20/20px;22/22px;24/24px;26/26px;28/28px;30/30px";
        //定制行间距
        config.line_height = "1;1.5;2;2.5;3;3.5;4;4.5;5";
        
        config.font_names = config.font_names + ";Miscrosoft Yahei;";
        
        config.ignoreEmptyParagraph = false;
};
