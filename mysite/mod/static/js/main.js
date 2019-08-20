function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

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

function deleteComment(reviewid) {
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

function rating(modID, value) {
    console.log("Rating this mod a " + value + "/5.");
    $.ajax({
        url: 'rating/',
        type: 'POST',
        data: {
            modID: modID,
            value: value,
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

function deleteRating() {
    console.log("Deleting rating for " + modID);
    console.log('Deleting rating ' + window.ratingID);
    $.ajax({
        url: 'ratingdelete/',
        type: 'POST',
        data: {
            ratingID: window.ratingID,
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