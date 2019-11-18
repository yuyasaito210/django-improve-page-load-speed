
$(document).ready(function() {

    $('.top_header_menu i, a, span').css("color", "dimgray");

});

function OpenFilterModal(filter_type) {

    let modal_window = $('#modal_filter');
    let modal_filter_Type_id = Object;
    $('.rsmodal_filter_div').each(function () {
       $(this).addClass("hideOnly");
    });

    switch (filter_type) {
        case "Date":
            modal_filter_Type_id = $('#rsmodal_filter_date');
            break;
        case "Capacity":
            modal_filter_Type_id = $('#rsmodal_filter_capacity');
            break;
        case "Category":
            modal_filter_Type_id = $('#rsmodal_filter_category');
            break;
        case "MoreFilters":
            modal_filter_Type_id = $('#rsmodal_filter_morefilter');
            break;
    }

    modal_filter_Type_id.removeClass("hideOnly");
    modal_window.modal('show');

}



//$('#filter_date_from, #filter_date_to').on("click", function () {

$('#modal_filter').on('hidden.bs.modal', function (e) {
    pureJSCalendar.close();
});

function BoatsRes_Option_Click(objId, destId, boat_type){
    let div = $('#'+objId);
    let currDest_val = $('#'+destId).val();

    if (boat_type !== "all") {
        if (div.hasClass('boat_reg_btn_cliked')) {
            div.removeClass('boat_reg_btn_cliked');
            currDest_val = currDest_val.replace(boat_type+";","");
        } else {
            div.addClass('boat_reg_btn_cliked');
            currDest_val += boat_type+";";
        }
    } else {
        let div_parent = div.parent();
        currDest_val = "";
        $('#rsmodal_filter_category .valid_opt').each(function () {
           $(this).addClass('boat_reg_btn_cliked');
           currDest_val += (($(this).attr("id")).split("_"))[3] + ";"
        });
    }

    $('#'+destId).val(currDest_val);
}

$('.slider-range').on("mouseup", "span", function () {
    //$('#search_form').submit();
});

$('#price_day').on("change", function () {
    //$('#search_form').submit();
});

