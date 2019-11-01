function showSupportListDropDown(x) {
    if ($('#' + x).css('display') == 'none') {
        $('#' + x).show(200)
    } else {
        $('#' + x).hide(200)
    }
}