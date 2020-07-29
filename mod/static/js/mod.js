if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', afterLoaded);
} else {
    afterLoaded();
}

function afterLoaded() {
    var reviewCommentForm = $('#reviewCommentForm > textarea, #reviewSubmitButton');
    reviewCommentForm.click(function () {
        if (!isAuth) {
            reviewCommentForm.attr("disabled", "disabled");
            $('#reviewCommentForm > textarea').text("You must be logged in to review mods!");
        }
    });

    $("#screenshotVideoContent").on("click", function () {
        if ($(this).hasClass("fullscreen-mode")) {
            $(this).removeClass("fullscreen-mode");
            $(".screenshotVideoContent").css("height", "");
            $(".screenshotVideoContentFullscreen").remove()
        } else {
            $(this).addClass("fullscreen-mode");
            $(".screenshotVideo").prepend("<div class='screenshotVideoContentFullscreen'><p>Fullscreen mode</p></div>");
            $(".screenshotVideoContent").css("height", "100%");
        }
    });
}

function upvote_post(id, modID) {
    $.ajax({
        url: 'reviewupvote/',
        type: 'POST',
        data: {id : id, modID : modID, csrfmiddlewaretoken : csrftoken},

        success : function (json) {

        },

        error : function (xhr, errmsg, err) {

        }
    })
}

function remove_vote(reviewid, modID) {

    $.ajax({
        url: 'reviewremovevote/',
        type: 'POST',
        data: {id: reviewid, modID: modID, csrfmiddlewaretoken: csrftoken},

        success: function (json) {

        },

        error: function (xhr, errmsg, err) {

        }
    })
}
// could optimise all of this code
function downvote_post(reviewid, modID) {
    $.ajax({
        url: 'reviewdownvote/',
        type: 'POST',
        data: {
            id: reviewid,
            modid: modID,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {

        },

        error: function (xhr, errmsg, err) {

        }
    })
}

function deleteCommentAjax(reviewid) {
    $.ajax({
        url: 'reviewdelete/',
        type: 'POST',
        data: {
            id: reviewid,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json){

        },

        error: function (xhr, errmsg, err) {

        }
    })
}

function rating(modID) {
    var radios = document.getElementsByName("rating");
    var radioValue;

    if (document.getElementById("rating").hidden) {
        radioValue = "N/A"
    } else {
        for (var i = 0, len=radios.length; i<len; i++) {
            if (radios[i].checked) {
                radioValue = radios[i].value;
            }
        }
    }

    var choice = document.getElementById("choice");
    var selectedChoice = choice.options[choice.selectedIndex].value;

    ratingSubmit(modID, radioValue, selectedChoice);
    document.getElementById("ratingSubmit").value = "Update";
}

function reminder() {
    $('#reminder').text("Don't forget to hit Submit/Update!").css("color", "red");
}

function registerReminder() {
    $('#reminder').text("You must be logged in to rate mods!").css("color", "red");
    $('#ratingSubmit, #choice, #rating').attr("disabled", "disabled");
}

function followReminder() {
    $('#followReminder').text("You must be logged in to follow mods!").css("color", "red");
    $('.modNotifications > input').attr("disabled", "disabled");
}

function ratingSubmit(modID, radioValue, selectedChoice) {

    $.ajax({
        url: 'rating/',
        type: 'POST',
        data: {
            modID: modID,
            radioValue: radioValue,
            selectedChoice: selectedChoice,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {
            var obj = JSON.parse(json['data'].slice(1, -1));
            window.ratingID = obj['pk'];
            window.ratingModID = obj['fields']['ratingModID'];
            window.ratingAuthorID = obj['fields']['ratingAuthorID'];
            window.ratingValue = obj['fields']['ratingValue'];
        },

        error: function (xhr, errmsg, err) {

        }
    })
}

function deleteRatingButton(ratingID) {
    $('#rating' + ratingID + 'Delete').off('click');
    deleteRating(ratingID);
    $('#rating' + ratingID).remove()
}



function deleteRating(ratingID) {
    $.ajax({
        url: 'ratingdelete/',
        type: 'POST',
        data: {
            ratingID: ratingID,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {

        },

        error: function (xhr, errmsg, err) {

        }
    })
}

function submitNews(news_text, news_mod_id) {
    $.ajax({
        url: 'news/',
        type: 'POST',
        data: {
            news_text: news_text,
            news_mod_id: news_mod_id,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {

        },

        error: function (xhr, errmsg, err) {

        }
    })
}

function followYes(modID) {
    $.ajax({
        url: 'notifications/',
        type: 'POST',
        data: {
            modID: modID,
            follow: 'add',
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {

            $('#notifications-no').attr({
                "id": "notifications-yes",
                "class": "notifications-yes",
                "value": "Following",
                "onclick": "followNo(" + modID + ")"
            });
        },

        error: function (xhr, errmsg, err) {

        }
    })
}

function followNo(modID) {
    $.ajax({
        url: 'notifications/',
        type: 'POST',
        data: {
            modID: modID,
            follow: 'remove',
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {

            $('#notifications-yes').attr({
                "id": "notifications-no",
                "class": "notifications-no",
                "value": "Follow",
                "onclick": "followYes(" + modID + ")"
            });
        },

        error: function (xhr, errmsg, err) {

        }
    })
}

function showNews() {
    $('#newsForm').show(500);
    $('#showNews').remove();
}

function deleteComment(reviewID) {
    //event.preventDefault();
    if (confirm('Are you sure you want to delete the review?')) {
        console.log("Deleting comment " + reviewID);
        deleteCommentAjax(reviewID);
        $(`#review${reviewID}`).remove();
    }
}

function editCommentAjax(reviewid) {
    $.ajax({
        url: 'reviewedit/',
        type: 'POST',
        data: {
            id: reviewid,
            comment: $(`#reviewComment${reviewid}`).val(),
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json){
            $('#savedNotification' + reviewid).show(1000).css("display", "inline-block").delay(2000).hide(1000);
            $(`#reviewComment${reviewid}`).val("This review is awaiting verification from moderators. If you have written the review and it has not been approved within 7 days, please contact us.").attr("disabled", "disabled");
            $(`#editReview${reviewid}`).remove();
        },

        error: function (xhr, errmsg, err) {
        }
    })
}

function editCommentAjaxEdit(reviewid) {
    if (confirm("You already have an edit being approved for this comment! You will overwrite your old edit if you submit this edit. Do you want to continue?")) {
        $.ajax({
            url: 'reviewedit/',
            type: 'POST',
            data: {
                id: reviewid,
                comment: $(`#reviewComment${reviewid}`).val(),
                csrfmiddlewaretoken: csrftoken
            },

            success: function (json){
                $('#savedNotification' + reviewid).show(1000).css("display", "inline-block").delay(2000).hide(1000);
                $(`#reviewComment${reviewid}`).val("This review is awaiting verification from moderators. If you have written the review and it has not been approved within 7 days, please contact us.").attr("disabled", "disabled");
                $(`#editReview${reviewid}`).remove();
            },

            error: function (xhr, errmsg, err) {
            }
        })
    }
}