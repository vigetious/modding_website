let panelOpen = 0;
//var firstFeatured = {};
var firstFeatured = undefined;
var firstRandom = undefined;

function showPanel(modID) {
    $('#mod' + panelOpen).css("display", "none");
    panelOpen = modID;

    $('#mod' + modID).css("display", "inline-block");
}


function changeFeatured(modID, avatarURL, modShortDescription, tags, searchURL, modPreviewImage1, modPreviewImage2, modPreviewImage3, modPreviewImage4, modPreviewImage5) {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', afterLoaded);
    } else {
        afterLoaded();
    }

    function afterLoaded() {
        $('#featuredAvatar').attr("src", avatarURL);
        $('#randomModShortDescription').html(modShortDescription).text();
        $('#featuredAvatarLink').attr("href", "/mod/" + modID);
        $('#featuredTags').empty();

        hidePreviewImages();

        for (i = 0; i < tags.length; i++) {
            $('#featuredTags').append("<a class='tag' href='" + searchURL + "?q=&sortBy=newest&tags=" + tags[i] + "&dateBy=0'>" + tags[i] + "</a> ");
        }
        if (modPreviewImage1 !== "null") {
            $('#featuredModBarPreviewImage1').attr("src", modPreviewImage1).attr("style", "display: inline-block");
            $('#randomModPreviewImage1').attr("src", modPreviewImage1);
        } else {
            $('#featuredModBarPreviewImage1').hide();
        }
        if (modPreviewImage2 !== "null") {
            $('#featuredModBarPreviewImage2').attr("src", modPreviewImage2).attr("style", "display: inline-block");
            $('#randomModPreviewImage2').attr("src", modPreviewImage2);
        } else {
            $('#featuredModBarPreviewImage2').hide();
        }
        if (modPreviewImage3 !== "null") {
            $('#featuredModBarPreviewImage3').attr("src", modPreviewImage3).attr("style", "display: inline-block");
            $('#randomModPreviewImage3').attr("src", modPreviewImage3);
        } else {
            $('#featuredModBarPreviewImage3').hide();
        }
        if (modPreviewImage4 !== "null") {
            $('#featuredModBarPreviewImage4').attr("src", modPreviewImage4).attr("style", "display: inline-block");
            $('#randomModPreviewImage4').attr("src", modPreviewImage4);
        } else {
            $('#featuredModBarPreviewImage4').hide();
        }
        if (modPreviewImage5 !== "null") {
            $('#featuredModBarPreviewImage5').attr("src", modPreviewImage5).attr("style", "display: inline-block");
            $('#randomModPreviewImage5').attr("src", modPreviewImage5);
        } else {
            $('#featuredModBarPreviewImage5').hide();
        }
        if (modPreviewImage1 !== "null") {
            $('#randomModPreviewImage1').attr("style", "display: inline-block").attr("class", "mySlides thumb selected");
        } else if (modPreviewImage2 !== "null") {
            $('#randomModPreviewImage2').attr("style", "display: inline-block").attr("class", "mySlides thumb selected");
        } else if (modPreviewImage3 !== "null") {
            $('#randomModPreviewImage3').attr("style", "display: inline-block").attr("class", "mySlides thumb selected");
        } else if (modPreviewImage4 !== "null") {
            $('#randomModPreviewImage4').attr("style", "display: inline-block").attr("class", "mySlides thumb selected");
        } else if (modPreviewImage5 !== "null") {
            $('#randomModPreviewImage5').attr("style", "display: inline-block").attr("class", "mySlides thumb selected");
        }
        $("[id^=featuredMod]").css("background-color", "#3ea7ff");
        $('#featuredMod' + modID).css("background-color", "#259bff");

        //calculateNextImage();
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', afterLoaded);
} else {
    afterLoaded();
}

function afterLoaded() {
    $('.screenshotVideoContent').click(function () {
        $(document).keydown(function(e) {
            switch (e.key) {
                case "ArrowLeft":
                    leftButton();
                    break;
                case "ArrowRight":
                    rightButton();
                    break;
                default: return
            }
            e.preventDefault();
        });
    });

    $('.search').click(function () {
        $(document).off('keydown');
    });

    $('.screenshotVideoContent').hover(function() {
        calculateNextImage();
    }, function () {
        $('.rightButton').addClass("tempHidden").removeClass("shown");
        $('.rightButton1').addClass("tempHidden").removeClass("shown");
        $('.leftButton').addClass("tempHidden").removeClass("shown");
        $('.leftButton1').addClass("tempHidden").removeClass("shown");
    });

    $('.leftButton').hover(function () {
        var prev = $(".selected").prev().attr("src");
        switch (prev) {
            case undefined:
            case "":
                $('.leftButton').addClass("tempHidden").removeClass("shown");
                break;
            default:
                $('.leftButton1').addClass("shown").removeClass("tempHidden");
        }
    });
    $('.rightButton').hover(function () {
        var next = $(".selected").next().attr("src");
        switch (next) {
            case undefined:
            case "":
                $('.leftButton').addClass("tempHidden").removeClass("shown");
                break;
            default:
                $('.leftButton1').addClass("shown").removeClass("tempHidden");
        }
    });

    for (var x in $(".mySlides")) {
        if ($(".mySlides")[x].src) {
            var id = $(".mySlides")[x].id;
            $("#" + id).attr("style", "display: inline-block");
            break;
        }
    }

    $('.leftButton').click(function () {
        leftButton()
    });
    $('.rightButton').click(function () {
        rightButton();
    }); //idk why this isnt working

    function leftButton() {
        var prev = $(".selected").prev();
        var img = prev.attr('src');
        if (img) {
            $(".mySlides").removeClass('selected').hide();
            prev.attr("style", "display: inline-block");
            prev.addClass('selected');
        }
        calculateNextImage();
    }

    function rightButton() {
        var next = $(".selected").next();
        var img = next.attr('src');
        if (img) {
            $(".mySlides").removeClass('selected').hide();
            next.attr("style", "display: inline-block");
            next.addClass('selected');
        }
        calculateNextImage();
    }
}

function hidePreviewImages() {
    $('#randomModPreviewImage1').hide().attr("src", "").attr("class", "mySlides thumb");
    $('#randomModPreviewImage2').hide().attr("src", "").attr("class", "mySlides thumb");
    $('#randomModPreviewImage3').hide().attr("src", "").attr("class", "mySlides thumb");
    $('#randomModPreviewImage4').hide().attr("src", "").attr("class", "mySlides thumb");
    $('#randomModPreviewImage5').hide().attr("src", "").attr("class", "mySlides thumb");
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
    x[slideIndex-2].style.display = "block";
}

function calculateFirstFeatured(BarOrVideo, modNumber) {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', afterLoaded);
    } else {
        afterLoaded();
    }

    function afterLoaded() {
        if (BarOrVideo === true && firstFeatured === undefined) {
            firstFeatured = modNumber;
            $('#randomModPreviewImage' + modNumber).attr("style", "display: inline-block");
        } else if (BarOrVideo === false) {
            $('#featuredModBarPreviewImage' + modNumber).attr("style", "display: inline-block");
        }
    }
}

function calculateNextImage() {
    var prev = $(".selected").prev().attr("src");
    var next = $(".selected").next().attr("src");
    switch (next) {
        case undefined:
        case "":
            $('.rightButton').addClass("tempHidden").removeClass("shown");
            break;
        default:
            $('.rightButton').removeClass("tempHidden").addClass("shown");
    }
    switch (prev) {
        case undefined:
        case "":
            $('.leftButton').addClass("tempHidden").removeClass("shown");
            break;
        default:
            $('.leftButton').removeClass("tempHidden").addClass("shown");
    }
}

function showHideBestOf(year) {
    if (year == 2019) {
        $('#bestOf2019Arrow').toggleClass("down").toggleClass("up");
        $('#best-of-2019').toggle(1000);
    } else {
        $('#bestOf2018Arrow').toggleClass("down").toggleClass("up");
        $('#best-of-2018').toggle(1000);
    }
}