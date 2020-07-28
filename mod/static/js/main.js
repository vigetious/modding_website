if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', afterLoaded);
} else {
    afterLoaded();
}

function afterLoaded() {
    $('input:submit').click(function () {

    });

    $('#baseSearch').focusin(function () {
        $('#baseSearch').animate({
            width: "30%"
        });
    }).focusout(function () {
        $('#baseSearch').animate({
            width: "100px"
        });
    })
}

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

$(function(){
    if (typeof freezeBg === 'undefined') {
        var x = 0;
        var y = 0;
        setInterval(function(){
            x-=1;
            y-=1;
            $('body').css('background-position', x + 'px ' + y + 'px');
        }, 30);
    } else {
        // stop moving the background
    }
});

function nsfw_check(tags, modName) {
    index = tags.indexOf("nsfw");
    if (index !== -1) {
        console.log("nsfw");
        $('#modName').css("color", "red");
        $('#modName').text("[NSFW] " + modName);
        $('#modUploadURL').click(function(){return confirm("You must be over 18 to download this mod. Please confirm that you are over the age of 18, and are allowed to download this mod.")});
    }
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

        document.getElementById(mod).style.display = "inline-block";
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