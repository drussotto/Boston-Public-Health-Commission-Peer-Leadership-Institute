$(function() {
    $('textarea.tinymce').tinymce({
	// width: '500px',
        // height: '100px',
        // Location of TinyMCE script
        script_url : "/static/js/tinymce.min.js",

        // General options
        plugins : "emoticons,autoresize,pagebreak,table,save,preview,media,searchreplace,print,contextmenu,paste,directionality,noneditable,visualchars,nonbreaking",
	toolbar : "undo,redo,|,styleselect,|,formats,|,bold,italic,|,alighleft,aligncenter,alignright,alignjustify,|,bullist,numlist,outdent,indent,|,table,|,fontsizeselect,|,emoticons",
        theme_modern_resizing : true,
	autoresize_overflow_padding: 50,
    });
});

function submitEditor() {
    tinyMCE.triggerSave();
    $('#editor-form').submit();
}
