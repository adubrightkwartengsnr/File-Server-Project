 // JavaScript/jQuery code to filter files based on category
$(document).ready(function () {
    $("label[for='checkbox1']").click(function () {
        var category = "photos";
        $(".file-library").hide();
        $(".file-library[data-category='" + category + "']").show();
    });

    $("label[for='checkbox2']").click(function () {
        var category = "videos";
        $(".file-library").hide();
        $(".file-library[data-category='" + category + "']").show();
    });

    $("label[for='checkbox3']").click(function () {
        var category = "audio";
        $(".file-library").hide();
        $(".file-library[data-category='" + category + "']").show();
    });

    $("label[for='checkbox4']").click(function () {
        var category = "pdfs";
        $(".file-library").hide();
        $(".file-library[data-category='" + category + "']").show();
    });
});