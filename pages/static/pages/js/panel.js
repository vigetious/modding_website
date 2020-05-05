function changePanel(modID, modName, avatarURL, modShortDescription, modAuthor, modDate, modPlayTimeHours, modStatus, modRating, tags, searchURL, modPreviewImage1, modPreviewImage2, modPreviewImage3, modPreviewImage4, modPreviewImage5, modRedditAccount) {
    $('#modAvatar').attr("src", avatarURL);
    $('#modAvatarLink').attr("href", "/mod/" + modID);
    $('#modShortDescription').html(modShortDescription).text();
    if (modAuthor !== "vigetious") {
        $('#modAuthor').attr("href", "/accounts/" + modAuthor + "/profile").html(modAuthor).text();
    } else if (modRedditAccount !== null) {
        $('#modAuthor').attr("href", "https://www.reddit.com/user/" + modRedditAccount + "/").text("u/" + modRedditAccount);
    } else {
        $('#modAuthor').attr("href", "/support/claim").text("Claim this mod as your own!");
    }
    $('#modName').html(modName).attr("href", "/mod/" + modID).text();
    $('#modDate').text(modDate);
    $('#modPlayTimeHours').text(modPlayTimeHours);
    $('#modStatus').text(modStatus);
    $('#modRating').text(modRating);
    $('#tags').empty();
    for (i = 0; i < tags.length; i++) {
        $('#tags').append("<a class='tag' href='" + searchURL + "?q=&sortBy=newest&tags=" + tags[i] + "&dateBy=0'>" + tags[i] + "</a> ");
    }
    if (modPreviewImage1 !== "null") {
        $('#modPreviewImage1').attr("src", modPreviewImage1).attr("style", "display: inline-block");
    } else {
        $('#modPreviewImage1').hide();
    }
    if (modPreviewImage2 !== "null") {
        $('#modPreviewImage2').attr("src", modPreviewImage2).attr("style", "display: inline-block");
    } else {
        $('#modPreviewImage2').hide();
    }
    if (modPreviewImage3 !== "null") {
        $('#modPreviewImage3').attr("src", modPreviewImage3).attr("style", "display: inline-block");
    } else {
        $('#modPreviewImage3').hide();
    }
    if (modPreviewImage4 !== "null") {
        $('#modPreviewImage4').attr("src", modPreviewImage4).attr("style", "display: inline-block");
    } else {
        $('#modPreviewImage4').hide();
    }
    if (modPreviewImage5 !== "null") {
        $('#modPreviewImage5').attr("src", modPreviewImage5).attr("style", "display: inline-block");
    } else {
        $('#modPreviewImage5').hide();
    }
}