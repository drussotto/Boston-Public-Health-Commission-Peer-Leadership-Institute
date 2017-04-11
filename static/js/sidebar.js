var originalPageContentHeight;
var navHeight = $("#nav").height();
$("#menu-toggle").click(function(e) {
  e.preventDefault();
  var $wrapper = $("#wrapper");
  $wrapper.toggleClass("toggled");
  if ($wrapper.hasClass("toggled")) {
    $("body").scrollTop(0);
    originalPageContentHeight = $pageContent.height();
    $("#page-content, #content-column").height(window.innerHeight - navHeight);
    $("#sidebar-wrapper, #page-content-mask").height(window.innerHeight);
    $("#footer").hide();
  } else {
    $("#page-content").height(originalPageContentHeight);
    $("#footer").show();
    $("#content-column").css("height", "initial");
  }
});

$("#page-content-mask").click(function() {
  $("#menu-toggle").click();
});