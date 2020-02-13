if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', afterLoaded);
} else {
    afterLoaded();
}

function afterLoaded() {

}

function finishEditBio() {
    newBio = document.getElementById('bio').innerText;
    $('#bio').attr('contentEditable', 'false');
    $('#editBio').off('click', finishEditBio).on('click', editBio).attr('value', 'Edit Bio');
    $('#cancelEditBio').off('click', cancelEdit).prop('hidden', true);
    editBioAjax(newBio);
}

function cancelEdit() {
    document.getElementById('bio').innerHTML = originalContent;
    $('#bio').attr('contentEditable', 'false');
    $('#editBio').off('click', finishEditBio).on('click', editBio).attr('value', 'Edit Bio');
    $('#cancelEditBio').off('click', cancelEdit).prop('hidden', true);
}


function showEdit() {
    $('#userLeftSideBarEdit').show(500);
    $('#showEdit').remove();
}

function editBio() {
    originalContent = document.getElementById('bio').innerHTML;
    document.getElementById('bio').contentEditable = "true";
    $('#editBio').off('click', editBio).on('click', finishEditBio).attr('value', 'Finish editing');
    $('#cancelEditBio').on('click', cancelEdit).removeAttr('hidden')
}

function editBioAjax(message) {
    $.ajax({
        url: 'bio',
        type: 'POST',
        data: {
            message: message,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {
            showBioUpdated();
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr + ': ' + xhr.responseText)
        }
    })
}

function showBioUpdated() {
    $('#bioUpdated').show(1000).css("display", "inline-block").delay(2000).hide(1000);
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

        },

        error: function (xhr, errmsg, err) {
            console.log(xhr + ': ' + xhr.responseText)
        }
    })
}

function confirmDeleteRating(ratingID) {
    $('#rating' + ratingID + 'DeleteButton').hide();
    $('#rating' + ratingID + 'Delete > p').text("Are you sure?");
    $('#rating' + ratingID + 'DeleteYes').removeClass("hidden");
    $('#rating' + ratingID + 'DeleteNo').removeClass("hidden");
}

function revertDeleteRating(ratingID) {
    $('#rating' + ratingID + 'DeleteButton').show();
    $('#rating' + ratingID + 'Delete > p').text("");
    $('#rating' + ratingID + 'DeleteYes').addClass("hidden");
    $('#rating' + ratingID + 'DeleteNo').addClass("hidden");
}

function deleteRatingButton(ratingID) {
    $('#rating' + ratingID + 'DeleteButton').off('click');
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
            console.log(xhr + ': ' + xhr.responseText)
        }
    })
}
