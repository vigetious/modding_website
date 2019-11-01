$(document).ready(function () {
    $(document).on("click", 'upvote_review', function (e) {
        $(this).toggleClass("clicked-button");
        var reviewID = $(this).attr('data-reviewID');
        var vote_total = $('.vote_total[data-reviewID=' + reviewID + ']');
        var downvote_button = $('.downvote_website[data-reviewID=' + reviewID + ']');

        if (downvote_button.hasClass("clicked-button")){
            downvote_button.toggleClass("clicked-button");
        }

        $.ajax({
            type: "POST",
            url: '/upvote_review/',
            data: {'reviewID': reviewID},
            dataType: "json",

            success: function (response) {
                vote_total.html(response + '&nbsp;');
            },

            error: function (response) {
                window.location.href = '/accounts/login/';
            }
        });
    })

    $(document).on("click", '.downvote_review', function (e) {
        $(this).toggleClass("clicked-button");
        var reviewID = $(this).attr('data-reviewID');
        var vote_total = $('.vote_total[data-reviewID=' + reviewID + ']');
        var upvote_button = $('.upvote_review[data-reviewID=' + reviewID + ']');

        if (upvote_button.hasClass("clicked-button")){
            upvote_button.toggleClass("clicked-button");
        }

        $.ajax({
            type: "POST",
            url: '/downvote_review/',
            data: {'reviewID': reviewID},
            dataType: "json",
            
            success: function (response) {
                vote_total.html(response + '&nbsp;');
            },
            
            error: function (response) {
                window.location.href = '/accounts/login/';
            }
        });
    })
})