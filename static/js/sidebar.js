$("#menu-toggle").click(function(e) {
  e.preventDefault();
  var $wrapper = $("#wrapper");
  $wrapper.toggleClass("toggled");
  if ($wrapper.hasClass("toggled")) {
    $("body").scrollTop(0);
  }
});

var pageHeight = $("#page-content").height() 
                + $("#footer").height()
                + $("#nav").height()
                + 50;
$("#page-content-mask").click(function() {
  $("#menu-toggle").click();
}).height(pageHeight);