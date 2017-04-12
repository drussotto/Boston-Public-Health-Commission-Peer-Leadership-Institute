$(function() {
    $('textarea.tinymce').tinymce({
	      // width: '500px',
        // height: '100px',
        // Location of TinyMCE script
        script_url : "/static/js/tinymce/tinymce.min.js",
	      // General options
        plugins : "image,emoticons,autoresize,pagebreak,save,preview,media,searchreplace,print,contextmenu,paste,directionality,noneditable,visualchars,nonbreaking,textcolor,colorpicker,advlist,lists",
  			toolbar : "undo,redo,|,styleselect,|,formats,|,bold,italic,|,alighleft,aligncenter,alignright,|,bullist,numlist,outdent,indent,|,fontsizeselect,|,emoticons,|,image,|,preview,|,forecolor,backcolor",
        theme_modern_resizing : true,
	      autoresize_overflow_padding: 50,
    });
});
		
function setupEdit(id) {		
    $.ajax("/uc/manage/getpage",		
	   {		
	       "data":{		
		   "page":id		
	       },		
	       "dataType": "json",		
	       "success": function(data) {		
		   console.log("running")		
		   $('#body').val(data["body"]);		
		   $('#title-box').val(data["title"]);		
		   console.log(data);		
		   $('.rolebox').each(function(idx, ele){		
		       ele.checked = ($.inArray(ele.value, data["required_roles"]) !== -1);		
		   });		
	       } 		
	   });		
}
