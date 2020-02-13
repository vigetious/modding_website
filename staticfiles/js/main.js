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

function submitNews(news_text, news_mod_id) {
    console.log("Submitting news for " + news_mod_id)
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


function finishEditBio() {
    console.log('Finished editing, saving...');
    newBio = document.getElementById('bio').innerText;
    $('#bio').attr('contentEditable', 'false');
    $('#editBio').off('click', finishEditBio).on('click', editBio).attr('value', 'Edit Bio');
    $('#cancelEditBio').off('click', cancelEdit).prop('hidden', true);
    editBioAjax(newBio);
}

function cancelEdit() {
    console.log('Canceled editing.');
    document.getElementById('bio').innerHTML = originalContent;
    $('#bio').attr('contentEditable', 'false');
    $('#editBio').off('click', finishEditBio).on('click', editBio).attr('value', 'Edit Bio');
    $('#cancelEditBio').off('click', cancelEdit).prop('hidden', true);
}

function openMod(evt, mod) {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', afterLoaded);
    } else {
        afterLoaded();
    }

    function afterLoaded() {
        var i, tabcontent, tablinks

        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }

        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }

        document.getElementById(mod).style.display = "block";
        evt.currentTarget.className += " active";
    }
}

function currentDiv(n) {
    showDivs(slideIndex = n);
}

function showDivs(n) {
    var i;
    var x = document.getElementsByClassName("mySlides");
    if (n > x.length) {slideIndex = 1}
    if (n < 1) {slideIndex = x.length}
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    x[slideIndex-1].style.display = "block";
}

function notLoggedIn() {
    window.alert("You must be logged in to do this!")
}

function showUpload() {
    document.getElementById('uploadProgressP').removeAttribute('hidden');
    document.getElementById('progressBar').removeAttribute('hidden');
}

// MOD PAGE SPECIFIC

function showNews() {
    $('#newsForm').show(500);
    $('#showNews').remove();
}

// PROFILE SPECIFIC

function showEdit() {
    $('#userLeftSideBarEdit').show(500);
    $('#showEdit').remove();
}

function editBio() {
    console.log('Editing bio.');
    originalContent = document.getElementById('bio').innerHTML;
    document.getElementById('bio').contentEditable = "true";
    $('#editBio').off('click', editBio).on('click', finishEditBio).attr('value', 'Finish editing');
    $('#cancelEditBio').on('click', cancelEdit).removeAttr('hidden')
}

function editBioAjax(message) {
    console.log(message);
    $.ajax({
        url: 'bio',
        type: 'POST',
        data: {
            message: message,
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

function editNoteAjax(note, ratingID) {
    $.ajax({
        url: 'note',
        type: 'POST',
        data: {
            note: note,
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

// SUBMIT SPECIFIC
function showNext(id, remove) {
    $('#hiddenNextImage' + id).show(200);
    $('#showNextButton' + remove).remove();
}

function previewMouseOver(id) {
    document.getElementById('previewImage' + id).setAttribute('style', 'width: 100%; height: 100%');
}

function previewMouseLeave(id) {
    document.getElementById('previewImage' + id).setAttribute('style', 'width:25%; height:25%');
}

$(document).ready(function () {
    $('#myForm').validate( {
        rules: {
            modName: {
                required: true
            },
            modUploadURL: {
                required: true,
                url: true
            },
            modPlayTimeMinutes: {
                range: [0, 59]
            }
        }
    })
});