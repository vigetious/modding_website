function editBioAjax(message) {
    $.ajax({
        url: 'profile/bio/',
        type: 'POST',
        data: {
            message: message,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (json) {
            console.log(json);
            console.log('success');
        }
    })
}