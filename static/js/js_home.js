
$(document).ready(function() {

    // FUNCTION AREA: WELCOME
    // define height of home image main window
    const window_height = window.innerHeight * 0.6; // define the front div with image and welcome as 60% of the screen
    const welcome_height = parseInt($('#welcome_div').css("height")) / 2; // get the height of welcome div
    //const welcome_div_half = (window_height - welcome_height);
    const home_back_img = $('#home_back_img');
    home_back_img.css('height',(window_height-welcome_height));
    (home_back_img.parent()).css('height',(window_height));

    // FUNCTION AREA: WELCOME
    // define top position of welcome city search div
    //const welcome_div = $('#welcome_div');
    //const div_height = welcome_div.height();
    //const div_css_top = (window_height / 2) - (div_height/2);
    //welcome_div.css("position","absolute")
    //    .css("top",div_css_top);

    // FUNCTION AREA: WELCOME
    // define left position of welcome city search div
    //const window_width = $(window).width();
    //const div_width = welcome_div.width();
    //if (window_width > 599) {
    //    const div_css_mleft = (window_width - div_width) / 6;
    //    welcome_div.css("margin-left",div_css_mleft);
    //}
    //welcome_div.css("display","block");

    // FUNCTION AREA: ALL_CITIES LIST
    //div_allCities - cities name list, this makes a word bold, the other not
    let counter = 1;
    $('#allCities_block .allCities_city').each(function () {
        if (counter === 1) {
            $(this)
                .css("font-family", "WorkSans-ExtraBold");
            counter = 0;
        } else {
            $(this).css("font-family", "WorkSans-Medium");
            counter = 1;
        }
    });

    // FUNCTION AREA: BOATS_VIEW
    // div_boats_view - boats view with review, the caroulse is created without active, this will add it
    $('.carousel-inner').each(function () {
        $(this).children(".carousel-item").first().addClass('active');
    });

    // FUNCTION AREA: BOATS_VIEW
    // div_boats_view - truncate boats review text
    $('.carousel-item p').each(function() {
        const full_text = $(this).html();
        const span_tag = "<span onclick='CarouselLoadFullText(this)' fulltext='"+full_text+"' class='linkHover'><strong>[...]</strong></span>";
        if (full_text.length > 200) {
            const new_text = full_text.substring(0, 200);
            $(this).html(new_text+span_tag);
        }
    });

    if (parseInt(window.outerWidth) < 800) {
        $('#home_filter_city').attr("placeholder", "Cidade");
        $('#top_filter_city').attr("placeholder", "Cidade");
    }
//$('#user_added').val()

    // FUNTION AREA: TOP BAR LOGO AT HOME
    //$('#top_bar_logo').attr("src", "/media/admin/logo_lightgray.png");
}); // -------------------------------------------------------    END OF $(document).ready function()


// FUNCTION AREA: BOATS_VIEW
// Loads full review text, if the three dots are clicked
function CarouselLoadFullText(obj) {
    const span_text = $(obj);
    const full_text = span_text.attr('fulltext');
    span_text.parent().html(full_text);
}

// FUNCTION AREA: BOATS_VIEW
// function to open boat page
//function OpenBoatPage(boat_id) {
//    console.log(boat_id);
//}