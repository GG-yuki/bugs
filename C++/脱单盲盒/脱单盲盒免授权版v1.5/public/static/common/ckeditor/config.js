/**
 * @license Copyright (c) 2003-2014, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function (config) {
    // Define changes to default configuration here. For example:
    // config.language = 'fr';
    config.uiColor = '#9AB8F3';
    // config.uiColor = '#66AB16';
    config.toolbar = 'Basic';
    config.toolbar_Basic = [
       ['Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
       ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'SpellChecker', 'Scayt'],
       ['RemoveFormat'],
       ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
       ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
       ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
       ['Link', 'Unlink', 'Anchor'],
       ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],        
       ['Styles', 'Format', 'Font', 'FontSize'],
        ['TextColor', 'BGColor','Source']
    ];
    config.toolbar_min = [
     
     ['PasteText', 'PasteFromWord', 'RemoveFormat','Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],   
     ['Link', 'Unlink', 'Anchor'],
     ['Image', 'Table',  'SpecialChar'],
     ['Styles', 'Format', 'Font', 'FontSize'],
     ['TextColor', 'BGColor']
    ];
    
    config.toolbarCanCollapse = true;
    config.smiley_columns = 16; //每行16个
    config.font_names = '宋体/宋体;黑体/黑体;仿宋/仿宋_GB2312;楷体/楷体_GB2312;隶书/隶书;幼圆/幼圆;微软雅黑/微软雅黑;' + config.font_names;
    config.allowedContent = true;
    // config.contentsCss = '/css.css'; 
    //去掉左下角的body和p标签

    // config.removePlugins = 'elementspath';
    config.enterMode = CKEDITOR.ENTER_P;

    //var deskCss = [ 
    //'/html/photonicschina/media/fair_css/fair_desktop/fair_desktop.css' ];

    
  //  config.stylesSet = 'mystyles';
    //config.stylesSet = 'mystyles:/editorstyles/styles.js';
 

    //config.contentsCss = deskCss;

    config.smiley_path = '/images/smiley/CK/';



    //鼠标指上去后显示的提示用config.smiley_descriptions属性指定
    config.smiley_descriptions = ['0', '1', '2', '3', '4', '5'];

    //对P标签自动进行格式化
    config.format_p = { element: 'p', attributes: { class: 'normalPara'} };


    config.extraPlugins='colordialog,tableresize';


    var ckfinderpath = ""; 
    config.filebrowserImageUploadUrl = ckfinderpath +  '/ajax/upload_editor_img'
   
};
