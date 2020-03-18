function hideBlur(modID) {
    //$("#homeRightMenu" + modID).css("filter", "url(#no-blur)");
    document.getElementById("homeRightMenu" + modID).style.webkitAnimationName = "fadein";
    document.getElementById("homeRightMenu" + modID).style.webkitAnimationDuration = "2.5s";
    document.getElementById("homeRightMenu" + modID).style.webkitFilter = "blur(0px)";
    $(".overlay" + modID + " > p").hide(1000);
    setTimeout(function () {
        $(".overlay" + modID).remove();
    }, 1000);
}

function loadFirst(modID) {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', afterLoaded);
    } else {
        afterLoaded();
    }

    function afterLoaded() {
        console.log("mySlides" + modID);
        for (var x in $(".mySlides" + modID)) {
            if ($(".mySlides" + modID)[x].src) {
                var id = $(".mySlides" + modID)[x].id;
                $("#" + id).attr("style", "display: inline-block");
                break;
            }
        }

        moveSayori();
    }
}


function moveSayori() {
    var x = 0;
    var y = 0;
    setInterval(function(){
        x-=1;
        y-=1;
        $('.category').css('background-position', x + 'px ' + y + 'px');
    }, 30);
}

function calculateNextImage(modID) {
    var prev = $(".selected" + modID).prev().attr("src");
    console.log("prev: " + prev);
    var next = $(".selected" + modID).next().attr("src");
    console.log("next: " + next);
    switch (next) {
        case undefined:
        case "":
            console.log("mod id: " + modID);
            document.getElementById('rightButton' + modID).classList.remove("shown");
            document.getElementById('rightButton' + modID).classList.add("tempHidden");
            break;
        default:
            document.getElementById('rightButton' + modID).classList.remove("tempHidden");
            document.getElementById('rightButton' + modID).classList.add("shown");
    }
    switch (prev) {
        case undefined:
        case "":
            document.getElementById('leftButton' + modID).classList.remove("shown");
            document.getElementById('leftButton' + modID).classList.add("tempHidden");
            break;
        default:
            document.getElementById('leftButton' + modID).classList.remove("tempHidden");
            document.getElementById('leftButton' + modID).classList.add("shown");
    }
}

function hideArrowButtons(modID) {
    $('.rightButton' + modID).addClass("tempHidden").removeClass("shown");
    $('.rightButton1' + modID).addClass("tempHidden").removeClass("shown");
    $('.leftButton' + modID).addClass("tempHidden").removeClass("shown");
    $('.leftButton1' + modID).addClass("tempHidden").removeClass("shown");
}

function leftButton(modID) {
    var prev = $(".selected" + modID).prev();
    var img = prev.attr('src');
    if (img) {
        $(".mySlides" + modID).removeClass('selected' + modID).hide();
        prev.attr("style", "display: inline-block");
        prev.addClass('selected' + modID);
    }
    calculateNextImage(modID);
}

function rightButton(modID) {
    var next = $(".selected" + modID).next();
    var img = next.attr('src');
    if (img) {
        $(".mySlides" + modID).removeClass('selected' + modID).hide();
        next.attr("style", "display: inline-block");
        next.addClass('selected' + modID);
    }
    calculateNextImage(modID);
}

