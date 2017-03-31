var curPage = 0;
var totalPages = 0;

function makePostContainer(page, ctnr) {
    console.log(page);
    var $div = $("<div></div>").addClass("section");
    var $postTitle = $("<h1></h1>").addClass("section-heading");
    var $img = $("<img class='section-bubbles' src='/static/images/bubbles.png'>").text(page["title"]);
    $postTitle.append($img);
    
    var $postBody = $("<div></div>");

    $postTitle.html(page["title"]);
    $postBody.html(page["body"]);
    $div.append($postTitle);
    $div.append($postBody);
    
    ctnr.append($div);

    $div.click(function () {
	window.location = "/uc/show?page="+page["_id"];
    });
}

function getPage(num) {
    console.log("Getting page");
    $.ajax('/uc/manage/pageofpages', {
	dataType: "json",
	data: {
	    skip: num,
	    number: 10
	},
	success: function(data) {
	    
	    console.log("Got ", data);
	    var $ctnr = $("#post_container");
	    $ctnr.html("");

	    for (var i = 0; i < data.length; i++) {
		makePostContainer(data[i], $ctnr);
	    }
	}
    });
}



function makeButtons() {
    var myPage = curPage;
    // while (myPage < curPage + 5) {
	
    // }
}

// $.ajax('/uc/manage/count', {
//     dataType: "json",
//     success: function(data) {
// 	totalPages = data;
// 	makeButtons();
//     }
// });

getPage(0);
