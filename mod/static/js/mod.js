function upvote_post(id, modID) {
    console.log('can upvote post ' + id);
    $.ajax({
        url: 'reviewupvote/',
        type: 'POST',
        data: {id : id, modID : modID, csrfmiddlewaretoken : csrftoken},

        success : function (json) {
            console.log(json);
            console.log("success");
        },

        error : function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    })
}

function remove_vote(reviewid, modID) {
    console.log('can remove vote from post ' + reviewid);
    $.ajax({
        url: 'reviewremovevote/',
        type: 'POST',
        data: {id: reviewid, modID: modID, csrfmiddlewaretoken: csrftoken},

        success: function (json) {
            console.log(json);
            console.log('success');
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    })
}
// could optimise all of this code
function downvote_post(reviewid, modID) {
    console.log('can downvote post ' + reviewid);
    $.ajax({
        url: 'reviewdownvote/',
        type: 'POST',
        data: {
            id: reviewid,
            modid: modID,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {
            console.log(json);
            console.log('success');
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText)
        }
    })
}

function deleteCommentAjax(reviewid) {
    console.log("Deleteing review " + reviewid);
    $.ajax({
        url: 'reviewdelete/',
        type: 'POST',
        data: {
            id: reviewid,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json){
            console.log(json);
            console.log('success');
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText)
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

function ratingSubmit(modID, radioValue, selectedChoice) {
    console.log("Rating this mod a " + radioValue + "/5.");

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
            console.log(json['result']);
            var obj = JSON.parse(json['data'].slice(1, -1));
            window.ratingID = obj['pk'];
            window.ratingModID = obj['fields']['ratingModID'];
            window.ratingAuthorID = obj['fields']['ratingAuthorID'];
            window.ratingValue = obj['fields']['ratingValue'];
            console.log('Created rating ' + ratingID);
            console.log('success')
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ': ' + xhr.responseText)
        }
    })
}

function deleteRatingButton(ratingID) {
    $('#rating' + ratingID + 'Delete').off('click');
    deleteRating(ratingID);
    $('#rating' + ratingID).remove()
}



function deleteRating(ratingID) {
    console.log('Deleting rating ' + ratingID);
    $.ajax({
        url: 'ratingdelete/',
        type: 'POST',
        data: {
            ratingID: ratingID,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {
            console.log(json);
            console.log('success');
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr + ': ' + xhr.responseText)
        }
    })
}

function submitNews(news_text, news_mod_id) {
    console.log("Submitting news for " + news_mod_id);
    $.ajax({
        url: 'news/',
        type: 'POST',
        data: {
            news_text: news_text,
            news_mod_id: news_mod_id,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {
            console.log(json);
            console.log('success');
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr + ': ' + xhr.responseText)
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
            console.log(json);
            console.log('success');
            $('#notifications-no').attr({
                "id": "notifications-yes",
                "class": "notifications-yes",
                "value": "Following",
                "onclick": "followNo(" + modID + ")"
            });
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr + ': ' + xhr.responseText)
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
            console.log(json);
            console.log('success');
            $('#notifications-yes').attr({
                "id": "notifications-no",
                "class": "notifications-no",
                "value": "Follow",
                "onclick": "followYes(" + modID + ")"
            });
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr + ': ' + xhr.responseText)
        }
    })
}

function showNews() {
    $('#newsForm').show(500);
    $('#showNews').remove();
}