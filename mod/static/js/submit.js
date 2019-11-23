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