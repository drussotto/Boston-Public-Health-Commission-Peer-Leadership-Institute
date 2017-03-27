$(function() {
    $('textarea.tinymce').tinymce({
	width: '500px',
        height: '100px',
        // Location of TinyMCE script
        script_url : "/static/js/tinymce.min.js",
	content_css : "/static/css/layout.css",

        // General options
        theme : "modern",
        plugins : "autoresize,pagebreak,table,save,preview,media,searchreplace,print,contextmenu,paste,directionality,noneditable,visualchars,nonbreaking",
        theme_modern_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,styleselect,formatselect,fontselect,fontsizeselect",
        theme_modern_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
        theme_modern_buttons3 : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl",
        theme_modern_buttons4 : "insertlayer,moveforward,movebackward,absolute,|,styleprops,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,nonbreaking,pagebreak",
        theme_modern_resizing : true,
	autoresize_overflow_padding: 50,
    });
});
