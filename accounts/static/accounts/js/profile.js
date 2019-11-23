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
