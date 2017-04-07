// Handles login (modal) form submission on any page (via layout.html)

$loginForm = $("#login-modal form");
$loginForm.attr("action", $loginForm.attr("action") + "?next=" + window.location);

$loginForm.submit(function(e) {
    e.preventDefault();
    $(".login-alert, #submit-login-btn").hide();
    $("#login-invalid-alert").html("");
    $("#login-loading-msg").show();
    $.ajax({
      url: $loginForm.attr("action"),
      type: "POST",
      dataType: "JSON",
      data: { 
        email: $("#email").val(),
        password: $("#password").val()
      },
      statusCode: {
        200: function() {
          window.location.replace($loginForm.attr("action").split("?next=")[1]);
        },
        403: function() {
          $("#login-failed-alert").show();
        },
        400: function(errors) {
          $invalidAlert = $("#login-invalid-alert").show();
          errors = $.parseJSON(errors.responseText);
          if (errors["email"]) {
            $invalidAlert.append("<p>Email is required.</p>");
          }
          if (errors["password"]) {
            $invalidAlert.append("<p>Password is required.</p>");
          }
        }
      },
      complete: function() {
        $("#login-loading-msg").hide();
        $("#submit-login-btn").show();
      }
    });
});