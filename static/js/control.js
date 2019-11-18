
// after html and dom
$(document).ready(function() {

    if (window.location.href.indexOf("pesca/loja-de-pesca") > -1) {
        $('#id_fishing_client').removeClass("hideOnly").attr("required", "required");
        $('#modal_login_btn').trigger("click");
    }

    // FUNCTION AREA - MENU
    // enable mobile version menu
    if (window.innerWidth < 1000) {
        $('#menu_nav').addClass('bg-light');
    }

    // FUNCTION AREA - SIGN IN and SIGN UP
    // if there is a message in the sign in or sign up, opens the login modal to show it
    if ($('#modal_alert').html() !== "  ") {
            $('#modal_login').modal('show');
    }

    //$('#top_bar_search').addClass('hideOnly');

    if ($('#id_license_type_5').length) {
        if($('#id_license_type_5').is(':checked')) {
            $('#ua_profile_form #professional_skipper').removeClass('hideOnly');
            $('#modal_captain_signup_part2 #professional_skipper').removeClass('hideOnly');
        }
    }


    if ($('#modal_captain_signup_part4 #id_extra_activities').length) {
        extra_activities_add('modal_captain_signup_part4');
    }
    if ($('#ua_profile_form #id_extra_activities').length) {
        extra_activities_add('ua_profile_form');
    }

    $('.results_div_owner_review').each(function () {
        let score = parseFloat($(this).attr('score').replace(",","."));
        let score_count = $(this).attr('score-count');
        let appendHtml = "";
        let i = 5;
        while (i > 0){
            if (score >= 1) {
                appendHtml += "<i class='fas fa-star'></i>";
            } else if (score >= 0.5) {
                appendHtml += "<i class='fas fa-star-half-alt'></i>";
            } else {
                appendHtml += "<i class='far fa-star'></i>";
            }
            score -= 1;
            i -= 1;
        }
        if (score_count != "") {
            $(this).append(appendHtml+" ("+score_count+")");
        } else {
            $(this).append(appendHtml);
        }
    });
    //DisableCalendarDays();

    if ($('#user_added').val() === "true") {
        $('#modal_login').modal('show');
        $('#modal_login_content').addClass('hideOnly');
        $('#modal_register_content').addClass('hideOnly');
        $('#modal_register_mobile').removeClass('hideOnly');
        SignUp_SendSms();
    }



}); // -------------------------------------------------------    END OF $(document).ready function()

function LoadFullCalendars() {
    if ($('#availability_calendar_left').length) {
        let cal_date = new Date();
        let month = parseInt(cal_date.getMonth()) + 1;
        let year = cal_date.getFullYear();
        $('#availability_calendar_left, #availability_calendar_right').html("");
        BuildOwnCalendar(month, year, 'availability_calendar_left');
        if (month === 12) {
            year += 1;
            month = 1;
        } else {
            month += 1;
        }
        BuildOwnCalendar(month, year, 'availability_calendar_right');
    }
}

function BuildOwnCalendar(month, year, cal_div_id) {

    let cal_date;
    let cal_div = $('#'+cal_div_id);
    if (year === "" || month === "") {
        cal_date = new Date();
        month = parseInt(cal_date.getMonth())+1;
        year = cal_date.getFullYear();
    }

    let no_weeks = GetNumberOfWeeksInMonth(month,year) + 2;

    //let cal_div = $('#availability_calendar');
    cal_div.html("");
    let cal_div_height = parseInt(cal_div.height());
    let cal_div_row_height = (cal_div_height / no_weeks);
    cal_date = new Date(year+"/"+month+"/01 00:00:00");
    let weekday_start = cal_date.getDay() + 1;
    let month_lastday = new Date(year, month, 0).getDate();
    let month_name = getMonthName(parseInt(cal_date.getMonth())+1);

    // GET BOOKED DATES
    let booked_dates = ($('#booked_dates').val()).split(";");
    let booked_date_arr, booked_from_date = [], booked_to_date = [], current_date, b = 0, is_booked = false;

    for (let i = 0; i < booked_dates.length; i++) {
        booked_date_arr = booked_dates[i].split("_");
        if (booked_date_arr.length > 1) {
            booked_from_date[b] = new Date(booked_date_arr[0].replace(/-/g,"/")+" 00:00:00");
            booked_to_date[b] = new Date(booked_date_arr[1].replace(/-/g,"/")+" 00:00:00");
        }
        b++;
    }

    // ------------------ TITLE
    let month_row = "<div class='cal_row_title w-100 cal_row d-flex' style='height: "+cal_div_row_height+"px;'>";
    let left_arrow = "<div class='left_arrow d-flex align-items-center justify-content-center flex-fill' onclick='Calendar_Move("+'"prev"'+",this)'><i class='fas fa-arrow-left'></i></div>";
    let right_arrow = "<div class='right_arrow d-flex align-items-center justify-content-center flex-fill' onclick='Calendar_Move("+'"next"'+",this)'><i class='fas fa-arrow-right'></i></div>";
    month_row += left_arrow;
    month_row += "<div class='cal_month d-flex align-items-center justify-content-center flex-fill' data-month='"+month+"' data-year='"+year+"'>"+month_name.toUpperCase()+" "+year+"</div>";
    month_row += right_arrow;
    month_row += "</div>";
    cal_div.append(month_row);

    // ------------------- WEEKDAY NAMES
    let week_days = "<div class='cal_days_row w-100 d-flex bd-highlight cal_row f-bold' style='height: "+cal_div_row_height+"px;'>";
    week_days += "<div class='p-0 flex-sm-fill bd-highlight cal_weekd d-flex align-items-center justify-content-center'>D</div>";
    week_days += "<div class='p-0 flex-sm-fill bd-highlight cal_weekd d-flex align-items-center justify-content-center'>S</div>";
    week_days += "<div class='p-0 flex-sm-fill bd-highlight cal_weekd d-flex align-items-center justify-content-center'>T</div>";
    week_days += "<div class='p-0 flex-sm-fill bd-highlight cal_weekd d-flex align-items-center justify-content-center'>Q</div>";
    week_days += "<div class='p-0 flex-sm-fill bd-highlight cal_weekd d-flex align-items-center justify-content-center'>Q</div>";
    week_days += "<div class='p-0 flex-sm-fill bd-highlight cal_weekd d-flex align-items-center justify-content-center'>S</div>";
    week_days += "<div class='p-0 flex-sm-fill bd-highlight cal_weekd d-flex align-items-center justify-content-center'>S</div>";
    week_days += "</div>";
    cal_div.append(week_days);


    // -------------------- DAYS
    let cal_cel = 1;
    let week_rows;
    let cel_day = 1, day = 1, curr_date, cel_date, blocked = "";
    for (let cal_row = 1; cal_row <= (no_weeks-2); cal_row++) {
        // DAYS ROW
        week_rows = "<div class='cal_days_row w-100 d-flex bd-highlight cal_row' style='height: "+cal_div_row_height+"px;'>";
        for (cal_cel = 1; cal_cel <= 7; cal_cel++) {
            curr_date = new Date();
            cel_date = new Date(year+"/"+month+"/"+day+" 00:00:00");
            // BLOCK PAST DATES
            if (curr_date >= cel_date) {
                blocked = "cal_day_blocked";
            } else {
                blocked = "";
            }
            // BLOCK BOAT BOOKED DATES
            for (let j = 0; j < booked_from_date.length; j++) {
                if (cel_date >= booked_from_date[j] && cel_date <= booked_to_date[j]) {
                    blocked = "cal_day_blocked";
                }
            }
            // DAY CELL
            week_rows += "<div class='p-0 pointer flex-sm-fill bd-highlight cal_weekd b-right d-flex align-items-center justify-content-center "+blocked+"'>";
            if ((cel_day === weekday_start || day > 1) && day <= month_lastday) {
                week_rows += day;
                day++;
            }
            week_rows += "</div>";
            cel_day++;
        }
        week_rows += "</div>";
        cal_div.append(week_rows);

        $('.cal_day_blocked').each(function () {
           if ($(this).html() === "") {
               $(this).removeClass("cal_day_blocked");
           }
        });
    }

}

/**
 * @return {number}
 */
function GetNumberOfWeeksInMonth(month, year) {
    let cal_date = new Date(year+"/"+month+"/01 00:00:00");
    let weekday_start = cal_date.getDay() + 1;
    let no_days_month = new Date(year, month, 0).getDate();
    let no_weeks = 0;

    no_days_month -= (7-(weekday_start-1));
    no_weeks = 1;
    no_weeks += parseInt(no_days_month/7);

    if (parseFloat(no_days_month/7) - parseInt(no_days_month/7) !== 0) {
        no_weeks += 1;
    }

    return no_weeks;
}

function Calendar_Move(direction, this_obj) {
    let calendar = $('#availability_calendar_left'); $(this_obj).parent().parent();
    let curr_year = parseInt(calendar.find('.cal_month').attr('data-year'));
    let curr_month = parseInt(calendar.find('.cal_month').attr('data-month'));

    if (direction === "next") {
        if (curr_month === 12) {
            curr_year += 1;
            curr_month = 1;
        } else {
            curr_month += 1;
        }
    } else if (direction === "prev") {
        if (curr_month === 1) {
            curr_year -= 1;
            curr_month = 12;
        } else {
            curr_month -= 1;
        }
    }
    BuildOwnCalendar(curr_month, curr_year, "availability_calendar_left");

    if (curr_month === 12) {
        curr_year += 1;
        curr_month = 1;
    } else {
        curr_month += 1;
    }

    BuildOwnCalendar(curr_month, curr_year, "availability_calendar_right");
}

function getMonthName(month) {
    let str_month;
    switch (month) {
        case 1:
            str_month = "Janeiro";
            break;
        case 2:
            str_month = "Fevereiro";
            break;
        case 3:
            str_month = "Março";
            break;
        case 4:
            str_month = "Abril";
            break;
        case 5:
            str_month = "Maio";
            break;
        case 6:
            str_month = "Junho";
            break;
        case 7:
            str_month = "Julho";
            break;
        case 8:
            str_month = "Agosto";
            break;
        case 9:
            str_month = "Setembro";
            break;
        case 10:
            str_month = "Outubro";
            break;
        case 11:
            str_month = "Novembro";
            break;
        case 12:
            str_month = "Dezembro";
            break;
    }
    return str_month;
}

function extra_activities_add(parentObj) {
    let lastRow = ($('#'+parentObj+' #id_extra_activities > li').last());
    let lastRowId = parseInt(((lastRow.find("input").attr("id")).split('_'))[3]);
    let lastRowVal = parseInt(lastRow.find("input").attr("value"));
    let li_item = "<li><label for='id_extra_activities_"+(lastRowId+1)+"'>";
    li_item += "<input type='checkbox' name='extra_activities' value='"+(lastRowVal+1)+"' class='radio_inp' ";
    li_item += "style='width:15px;height:15px;float:left;' id='id_extra_activities_"+(lastRowId+1)+"'>";
    li_item += "<input placeholder='Outros' type='text' data-parent='"+parentObj+"' class='form-control extra-acts-add'";
    li_item += "style='border-bottom: 1px solid #537b89 !important;' value=''></label></li>";
    $('#'+parentObj+' #id_extra_activities').append(li_item);
}

$('#ua_profile_form, #modal_captain_signup_part4 #id_extra_activities').on('focusout', '.extra-acts-add', function () {
    let obj_id = $(this).attr("data-parent");
    let lastRow = ($('#'+obj_id+' #id_extra_activities > li').last());
    let lastRowId = parseInt(((lastRow.find("input").attr("id")).split('_'))[3]);
    let thisRow = parseInt((($(this).parent().find("input").attr("id")).split('_'))[3]);
    if (thisRow === lastRowId) {
        extra_activities_add(obj_id);
    }
});

// FUNCTION AREA - MENU
// function to open the menu on mobile
function OpenMobileMenu(is_authenticated) {
    if (is_authenticated === "True") {
        event.preventDefault();
        event.stopPropagation();
        openUserMenu();
    } else {
        $('#welcome_div').css('position','static');
    }
}

// FUNCTION AREA - MENU
// on mobile, after the menu is closed, the welcome div should move to the original position
$('#menu_nav').on('hide.bs.collapse', function () {
    $('#welcome_div').css('position','absolute');
});

// FUNCTION AREA - MENU
// Opens menu
function openUserMenu() {
    document.getElementById("right_user_menu_open").style.width = "250px";
}

// FUNCTION AREA - MENU
// Closes menu
function closeNav() {
    document.getElementById("right_user_menu_open").style.width = "0";
}

// FUNCTION AREA - SIGN IN
//Sign up functionality
function modalSignUp(person) {
    $('#modal_login_content').addClass('hideOnly');
    $('#modal_register_content').removeClass('hideOnly');
    $('#modal_register_mobile').addClass('hideOnly');
    $('#modal_alert').addClass('hideOnly');
    $('#modal_alert_cap').addClass('hideOnly');
    if ( person.toLowerCase() === "owner") {
        $('#signup_register').css('display','none');
        $('#add_boat').val('true');
        $('#add_boat_signin').val('true');
    } else {
        $('#signup_register').css('display','flex');
        $('#add_boat').val('');
        $('#add_boat_signin').val('');
    }
}

//Sign up functionality
function modalCaptainProfile() {
    if ($('#add_boat').val() === "Add_CapProf") {
        $('#modal_captain_signup').modal({
            backdrop: 'static',
            keyboard: false
        });
        $('#modal_captain_signup').modal('show');
    } else {
        $('#modal_boat_reg').modal({
            backdrop: 'static',
            keyboard: false
        });
        $('#modal_boat_reg').modal('show');
        let price;
        $('.price_inp').each(function () {
           price = parseInt($(this).val());
           if (!isNaN(price)) {
                $(this).val(price);
                PriceChange($(this).attr("id"));
           }
        });

    }
}

// FUNCTION AREA - SIGN IN
//Sign in functionality
function modalSignIn() {
    $('#modal_login_content').removeClass('hideOnly');
    $('#modal_register_content').addClass('hideOnly');
    $('#modal_register_mobile').addClass('hideOnly');
    $('#modal_alert').addClass('hideOnly');
    $('#modal_alert_cap').addClass('hideOnly');
}

// FUNCTION AREA - SIGN UP and SIGN IN
// function used to switch between login and registration
function ModalToggleLoginRegister() {
    $('#modal_login_content').toggleClass('hideOnly');
    $('#modal_register_content').toggleClass('hideOnly');
    $('#modal_alert').addClass('hideOnly');
    $('#modal_alert_cap').addClass('hideOnly');
}

// FUNCTION AREA - SIGN UP
// only allow numbers in all objects with class onlyNumbers inside the registration modal
$('body').on('keydown', '.onlyNumbers', function(e){
   const ignore_key_codes = [0,8,9,17,46,48,49,50,51,52,53,54,55,56,57,86,96,97,98,99,100,101,102,103,104,105,187,188];
   if ($.inArray(e.keyCode, ignore_key_codes) <= 0){
      e.preventDefault();
   }
});

// FUNCTION AREA - SIGN UP
// function to send registration code to modile by SMS
let unique_id;
function SignUp_SendSms(){

    //event.preventDefault();

    //if (!document.getElementById('SignUpForm').checkValidity()) {
    //    $('#register_btn').trigger('click');
    //    return;
    //}

    unique_id = Math.random().toString(36).substr(2, 5);
    // call function(unique_id) to send SMS

    const mobile_country = "+" + parseInt($('#id_mobile_country').val());
    const mobile_area = $('#id_mobile_area').val();
    const mobile_no = $('#id_mobile_number').val();
    const title_obj = $('#mobile_confirm_title');
    const title = title_obj.html();

    title_obj.html(title.replace("[mobileNo]",mobile_country+" "+mobile_area+" "+mobile_no));
    $('#modal_register_content').addClass('hideOnly');
    $('#modal_register_mobile').removeClass('hideOnly');

}

// FUNCTION AREA - SIGN UP
// function to check if the entered code is correct and submit registration
function SignUp_SmsConfirm() {

    event.preventDefault();

    const mobile_code_input = $('#mobile_code');
    const sms_code = mobile_code_input.val();
    const successMsg = mobile_code_input.attr('successmsg');
    const errorMsg = mobile_code_input.attr('errormsg');

    if (unique_id === sms_code) {
        $('#modal_alert_sms')
            .removeClass("hideOnly")
            .removeClass("alert-danger")
            .addClass("alert-success")
            .html(successMsg);
        $('#sms_confirm').val('confirmed');
        setTimeout(function submitForm() {$('#SMSConfirmForm').submit();}, 2000);
    } else {
        $('#modal_alert_sms')
            .removeClass("hideOnly")
            .removeClass("alert-success")
            .addClass("alert-danger")
            .html(errorMsg);
        $('#sms_confirm').val('invalid');
    }
}

// FUNCTION AREA - AUTOCOMPLETE
// autocomplete code block
function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus, val_a, val_b;
  var listWidth = inp.offsetWidth;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function() {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      a.setAttribute("style", "width: "+listWidth+"px");
      inp.setAttribute("style","border-bottom-left-radius: 0 !important;");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        val_a = arr[i].substr(0, val.length).toUpperCase().replace("Ã","A").replace("Á","A").replace("Ú","U");
        val_a = val_a.replace("Ç","C").replace("Ó","O");
        val_b = val.toUpperCase().replace("Ã","A").replace("Á","A").replace("Ú","U");
        val_b = val_b.replace("Ç","C").replace("Ó","O");
        if (val_a === val_b) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          //b.innerHTML = "<i class='fas fa-map-marker-alt' style='font-size: 18px;position: absolute;left: 0;padding: 4px 12px 8px 15px;color: lightslategray;'></i>";
          b.innerHTML = "<strong style='color: dodgerblue;'>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function() {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });

          if ($('.autocomplete-items > div').length === 4) {
            return;
          }
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode === 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus constiable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode === 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus constiable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode === 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt !== x[i] && elmnt !== inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
    $(".home_filter_city").css("border-bottom-left-radius","");
    });
}

// FUNCTION AREA - HOME CITY SEARCH
// Define all cities list to be uploaded in the city autocomplete search
let str_all_cities = $('#all_cities').val().split("'").join("").replace("[","").replace("]","").split(",").join(";");
let arr_all_cities = str_all_cities.split("_").join(",").split("; ");
$('.home_filter_city').on('keydown', function() {
    autocomplete(document.getElementById(this.id), arr_all_cities);
});

function CapitainSignUpForm_Next(id_hide, id_show) {
        $('#modal_captain_signup_part'+id_hide).addClass('hideOnly');
        $('#modal_captain_signup_part'+id_show).removeClass('hideOnly');
}

function CheckSkipperLicense() {

    if($('#ua_profile_form #id_license_type_5').is(':checked')) {
        $('#ua_profile_form #professional_skipper').removeClass('hideOnly');
    } else {
        $('#ua_profile_form #professional_skipper').addClass('hideOnly');
    }
    if($('#modal_captain_signup_part2 #id_license_type_5').is(':checked')) {
        $('#modal_captain_signup_part2 #professional_skipper').removeClass('hideOnly');
    } else {
        $('#modal_captain_signup_part2 #professional_skipper').addClass('hideOnly');
    }

}

function AddToFavorite(obj_id, is_authenticated) {
    event.preventDefault();
    event.stopPropagation();

    if (is_authenticated === "False") {
        $('#SignUpBtn').trigger("click");
        return;
    }

    let icon = $('#'+obj_id);
    let boat_id = obj_id.split('_')[1];

    $.ajax({
       url: '../../adicionar-favorito',
       data: {
           'boat_id': boat_id
       },
        dataType: 'json',
        complete: function (data) {
        },
        error: function (error_msg) {
        }
    });

    icon.removeClass("far");
    icon.addClass("fas");
    icon.addClass("added");
}

function create_extra_activity(form_id) {

    if (event != undefined) {
        event.preventDefault();
    }

    $('#loaderIcon').removeClass("hideOnly");
    $('#ua_submit').attr("disabled", "disabled");

    $('#CaptainSetupMsg').removeClass("hideOnly");

    let new_values = "";

    $('.extra-acts-add').each(function () {
        new_values += $(this).val()+",";
    });

    $.ajax({
        url: 'create_extra_activity',
        data: {
            'new_values': new_values
        },
        dataType: 'json',
        complete: function (data) {
            setTimeout(function() {
                $('#CaptainSetupMsg').addClass("hideOnly");
                $('#'+form_id).find('.inp_sub').trigger("click");
            }, 1000);
        }
    });
}

function UpdateSearchField(obj_id) {
    let city = (($('#'+obj_id).val()).split(" - "))[0];

    $('#'+obj_id).parent().find('.search_city_name').val(city);

}

/**
 * @return {boolean}
 */
function ValidateCity(obj_id) {

    let submit_btn = $('#'+obj_id);
    let input_city = submit_btn.parent().find('.home_filter_city');
    let city = input_city.val();
    let city_found = false;
    let customized_city;

    if (city === "") {
        submit_btn.parent().find('.search_city_name').val("brasil");
        //input_city.val("0");
        return;
    }

    // change array of cities to all lower case
    let lcase_city_array = [];
    for (let i = 0; i < arr_all_cities.length; i++) {
        customized_city = arr_all_cities[i]
            .toLowerCase()
            .replace(/-/g, "")
            .replace(/,/g, "")
            .replace(/ {2}/g, " ")
            .replace(/ /g, ".*")
            .replace(/ã/g, "a")
            .replace(/õ/g, "o")
            .replace(/ç/g, "c")
            .replace(/á/g, "a")
            .replace(/é/g, "e")
            .replace(/í/g, "i")
            .replace(/ó/g, "o")
            .replace(/ú/g, "u");
        lcase_city_array.push(customized_city);
    }

    // create regex of searched city and convert to lowercase
    let current_city = city.toLowerCase()
        .replace(/-/g, "")
        .replace(/,/g, "")
        .replace(/ {2}/g, " ")
        .replace(/ /g, ".*")
        .replace(/ã/g, "a")
        .replace(/õ/g, "o")
        .replace(/ç/g, "c")
        .replace(/á/g, "a")
        .replace(/é/g, "e")
        .replace(/í/g, "i")
        .replace(/ó/g, "o")
        .replace(/ú/g, "u");
    let city_regex = new RegExp(current_city);

    // find the regex city in the array of cities
    lcase_city_array.filter(function(word,index){
        if(word.match(city_regex)){
            console.log(index);
            city = arr_all_cities[index];
            submit_btn.parent().find('.search_city_name').val(city);
            input_city.val(city);
            UpdateSearchField(input_city.attr('id'));
            city_found = true;
            return true;
        }
    });

    if (city_found === false) {
        alert("Infelizmente a entrada "+city+" não foi reconhecida como uma cidade válida ou não temos barco nela. Tente novamente");
        event.preventDefault();
        return false;
    } else {
        return true;
    }

}

function SearchPageValidateCity(obj_id) {
    event.preventDefault();

    let found_city = ValidateCity(obj_id);

    if (found_city === true) {
        $('#filter_city').val($('#search_city_name').val());
        $('#search_form').submit();
    }
}

//  -----------------------------------------   CALENDAR  -------------------------------------------------------------


//private calendar controller IIFE
var pureJSCalendar = (function () {
    let wrap, label, calYear, calMonth, calDateFormat, firstDay, isIE11;

    isIE11 = !!window.MSInputMethodContext && !!document.documentMode;

    //check global variables for calendar widget and set default localizatioSubmitMsgn values
    if (window.months === undefined) {
        window.months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto',
            'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    }

    if (window.shortDays === undefined) {
        window.shortDays = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM'];
    }

    //first day of week combinations array
    const firstDayCombinations = [
        [0, 1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6, 0],
        [2, 3, 4, 5, 6, 0, 1],
        [3, 4, 5, 6, 0, 1, 2],
        [4, 5, 6, 0, 1, 2, 3],
        [5, 6, 0, 1, 2, 3, 4],
        [6, 0, 1, 2, 3, 4, 5]
    ]

    //DOM strings helper
    const DOMstrings = {
        divCal: 'cal',
        divCalQ: '#cal',
        monthLabel: 'label',
        btnPrev: 'prev',
        btnNext: 'next',
        sunLabel: 'eformSun',
        monLabel: 'eformMon',
        tueLabel: 'eformTue',
        wedLabel: 'eformWed',
        thuLabel: 'eformThu',
        friLabel: 'eformFri',
        satLabel: 'eformSat',
        tdDay: '.eformDay'
    }

    //open function
    function open(dateFormat, x, y, firstDayOfWeek, minDate, maxDate, element, zindex) {
        //prevent to open more than one calendar
        if (document.getElementById('cal')) {
            return false;
        }

        //init def props
        eFormMinimalDate = DateParse(minDate);
        eFormMaximalDate = DateParse(maxDate);
        eFormCalendarElement = element;
        firstDay = firstDayOfWeek;

        //set default first date of week
        if (firstDayOfWeek === undefined) {
            firstDayOfWeek = 6;
        } else {
            firstDayOfWeek -= 1;
        }

        //create html and push it into DOM
        const newHtml = '<div id="cal" style="top:' + y + 'px;left:' + x + 'px;z-index:' + zindex + ';"><div class="header"><span class="left button" id="prev"> &lang; </span><span class="left hook"></span><span class="month-year" id="label"> June 20&0 </span><span class="right hook"></span><span class="right button" id="next"> &rang; </span></div ><table id="days"><tr><td id="eformSun">sun</td><td id="eformMon">mon</td><td id="eformTue">tue</td><td id="eformWed">wed</td><td id="eformThu">thu</td><td id="eformFri">fri</td><td id="eformSat">sat</td></tr></table><div id="cal-frame"><table class="curr"><tbody></tbody></table></div></div >'
        document.getElementsByTagName('body')[0].insertAdjacentHTML('beforeend', newHtml);

        calDateFormat = dateFormat;
        wrap = document.getElementById(DOMstrings.divCal);
        label = document.getElementById(DOMstrings.monthLabel);

        //register events
        document.getElementById(DOMstrings.btnPrev).addEventListener('click', function () { switchMonth(false); });
        document.getElementById(DOMstrings.btnNext).addEventListener('click', function () { switchMonth(true); });
        label.addEventListener('click', function () { switchMonth(null, new Date().getMonth(), new Date().getFullYear()); });

        //shorter day version labels
        const dayCombination = firstDayCombinations[firstDayOfWeek];

        document.getElementById(DOMstrings.sunLabel).textContent = window.shortDays[dayCombination[0]];
        document.getElementById(DOMstrings.monLabel).textContent = window.shortDays[dayCombination[1]];
        document.getElementById(DOMstrings.tueLabel).textContent = window.shortDays[dayCombination[2]];
        document.getElementById(DOMstrings.wedLabel).textContent = window.shortDays[dayCombination[3]];
        document.getElementById(DOMstrings.thuLabel).textContent = window.shortDays[dayCombination[4]];
        document.getElementById(DOMstrings.friLabel).textContent = window.shortDays[dayCombination[5]];
        document.getElementById(DOMstrings.satLabel).textContent = window.shortDays[dayCombination[6]];

        //fire inicialization event trigger
        label.click();
    }

    //switches current month
    function switchMonth(next, month, year) {
        var curr = label.textContent.trim().split(' '), calendar, tempYear = parseInt(curr[1], 10);
        if (month === undefined) {
            month = ((next) ? ((curr[0] === window.months[11]) ? 0 : months.indexOf(curr[0]) + 1) : ((curr[0] === window.months[0]) ? 11 : months.indexOf(curr[0]) - 1));
        }

        if (!year) {
            if (next && month === 0) {
                year = tempYear + 1;
            } else if (!next && month === 11) {
                year = tempYear - 1;
            } else {
                year = tempYear;
            }
        }

        //set month and year for widget scope
        calMonth = month + 1;
        calYear = year;

        calendar = createCal(year, month);

        var curr = document.querySelector('.curr')
        curr.innerHTML = '';
        curr.appendChild(calendar.calendar());

        //disable days below minimal date
       /* if (eFormMinimalDate !== undefined) {
            if (year < eFormMinimalDate.year || year <= eFormMinimalDate.year && month <= eFormMinimalDate.month - 1) {
                const emptyCount = document.querySelector('.curr table').rows[0].querySelectorAll('td:empty').length;
                const tdDisabled = document.querySelectorAll('.eformDay');
                for (var i = 0; i < tdDisabled.length; ++i) {
                    if (i - emptyCount + 1 < eFormMinimalDate.day && month < eFormMinimalDate.month - 1 && year < eFormMinimalDate.year) {
                        tdDisabled[i].classList.add('eformDayDisabled');
                        tdDisabled[i].onclick = function () {
                            return false;
                        }
                    }
                }
            }
        }

        //disable days above maximal date
        if (eFormMaximalDate !== undefined) {
            if (year > eFormMinimalDate.year || year >= eFormMaximalDate.year && month >= eFormMaximalDate.month - 1) {
                const emptyCount = document.querySelector('.curr table').rows[0].querySelectorAll('td:empty').length;
                const tdDisabled = document.querySelectorAll('.eformDay');
                for (var i = 0; i < tdDisabled.length; ++i) {
                    if (year >= eFormMaximalDate.year) {
                        if (month >= eFormMaximalDate.month) {
                            if (i - emptyCount + 1 > eFormMaximalDate.day) {
                                tdDisabled[i].classList.add('eformDayDisabled');
                                tdDisabled[i].onclick = function () {
                                    return false;
                                }
                            }
                        }
                    }
                }
            }
        }*/

        label.textContent = calendar.label;
        //DisableCalendarDays();
    }

    //main calendar function. Creates calendar itself and stores into cache
    function createCal(year, month) {
        var day = 1, i, j, haveDays = true,
            startDay = new Date(year, month, day).getDay(),
            daysInMonths = [31, (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0)) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
            calendar = [];

        startDay -= firstDay;
        if (startDay < 0) {
            startDay = 7 + startDay;
        }

        if (createCal.cache[year] && !isIE11) {
            if (createCal.cache[year][month]) {
                return createCal.cache[year][month];
            }
        } else {
            createCal.cache[year] = {};
        }

        i = 0;
        while (haveDays) {
            calendar[i] = [];
            for (j = 0; j < 7; j++) {
                if (i === 0) {
                    if (j === startDay) {
                        calendar[i][j] = day++;
                        startDay++;
                    }
                } else if (day <= daysInMonths[month]) {
                    calendar[i][j] = day++;
                } else {
                    calendar[i][j] = '';
                    haveDays = false;
                }
                if (day > daysInMonths[month]) {
                    haveDays = false;
                }
            }
            i++;
        }

        ////6th week of month fix IF NEEDED
        //if (calendar[5]) {
        //    for (i = 0; i < calendar[5].length; i++) {
        //        if (calendar[5][i] !== '') {
        //            calendar[4][i] = '<span>' + calendar[4][i] + '</span><span>' + calendar[5][i] + '</span>';
        //        }
        //    }
        //    calendar = calendar.slice(0, 5);
        //}

        for (i = 0; i < calendar.length; i++) {
            calendar[i] = '<tr><td class="eformDay month_holder" data-month="'+(parseInt(month)+1)+'" onclick="pureJSCalendar.dayClick(this)">' + calendar[i].join('</td><td class="eformDay" onclick="pureJSCalendar.dayClick(this)">') + '</td></tr>';
        }

        const calendarInnerHtml = calendar.join('');
        calendar = document.createElement('table', { class: 'curr' });
        calendar.innerHTML = calendarInnerHtml;
        const tdEmty = calendar.querySelectorAll('td:empty');
        for (var i = 0; i < tdEmty.length; ++i) {
            tdEmty[i].classList.add('nil');
        }
        if (month === new Date().getMonth()) {
            const calTd = calendar.querySelectorAll('td');
            const calTdArray = Array.prototype.slice.call(calTd);
            calTdArray.forEach(function (current, index, array) {
                if (current.innerHTML === new Date().getDate().toString()) {
                    current.classList.add('today');
                }
            });
        }

        createCal.cache[year][month] = { calendar: function () { return calendar }, label: months[month] + ' ' + year };//calendar.clone()

        //DisableCalendarDays();
        return createCal.cache[year][month];
    }
    //DisableCalendarDays();
    createCal.cache = {};

    //day click event function => than close
    const dayClick = function (element) {
        const dateResult = DateToString(new Date(calYear, calMonth-1, parseInt(element.innerHTML)), calDateFormat);

        document.getElementById(eFormCalendarElement).value = dateResult;
        close();
    }

    // join
    function joinObj(obj, seperator) {
        var out = [];
        for (k in obj) {
            out.push(k);
        }
        return out.join(seperator);
    }

    //returns string in desired format
    function DateToString(inDate, formatString) {
        var dateObject = {
            M: inDate.getMonth() + 1,
            d: inDate.getDate(),
            D: inDate.getDate(),
            h: inDate.getHours(),
            m: inDate.getMinutes(),
            s: inDate.getSeconds(),
            y: inDate.getFullYear(),
            Y: inDate.getFullYear()
        };
        // Build Regex Dynamically based on the list above.
        // Should end up with something like this "/([Yy]+|M+|[Dd]+|h+|m+|s+)/g"
        var dateMatchRegex = joinObj(dateObject, "+|") + "+";
        var regEx = new RegExp(dateMatchRegex, "g");
        formatString = formatString.replace(regEx, function (formatToken) {
            var datePartValue = dateObject[formatToken.slice(-1)];
            var tokenLength = formatToken.length;

            if (formatToken === 'MMMM') {
                return window.months[dateObject.M - 1];
            }

            // A conflict exists between specifying 'd' for no zero pad -> expand to '10' and specifying yy for just two year digits '01' instead of '2001'.  One expands, the other contracts.
            // so Constrict Years but Expand All Else
            if (formatToken.indexOf('y') < 0 && formatToken.indexOf('Y') < 0) {
                // Expand single digit format token 'd' to multi digit value '10' when needed
                var tokenLength = Math.max(formatToken.length, datePartValue.toString().length);
            }
            var zeroPad;
            try {
                zeroPad = (datePartValue.toString().length < formatToken.length ? "0".repeat(tokenLength) : "");
            } catch (ex) {//IE11 repeat catched
                zeroPad = (datePartValue.toString().length < formatToken.length ? repeatStringNumTimes("0", tokenLength) : "");
            }
            return (zeroPad + datePartValue).slice(-tokenLength);
        });

        return formatString;
    }
    Date.prototype.ToString = function (formatStr) { return DateToString(this.toDateString(), formatStr); }

    //IE11 repeat alternative
    function repeatStringNumTimes(string, times) {
        var repeatedString = "";
        while (times > 0) {
            repeatedString += string;
            times--;
        }
        return repeatedString;
    }

    //close event function (fadeout)
    function close() {
        fadeOutEffect(DOMstrings.divCalQ, remove);
    }

    //remove calendar box
    var remove = function () {
        try {
            document.getElementById(DOMstrings.divCal).remove();
        } catch (ex) {//ie11 fix
            const child = document.getElementById(DOMstrings.divCal);
            child.parentNode.removeChild(child);
        }
    }

    //parse date
    function DateParse(date) {
        let parsedDate, newDate;
        const currentDate = date;

        if (currentDate != null) {
            splitedDate = currentDate.split('-');
            newDate = { year: splitedDate[0], month: splitedDate[1], day: splitedDate[2] };
        }

        return newDate;
    }

    //function accesibility
    return {
        open: open,
        switchMonth: switchMonth,
        createCal: createCal,
        dayClick: dayClick,
        close: close
    };
    //DisableCalendarDays();
})();

//plain javascript fadeout alternative
function fadeOutEffect(selector, callback) {
    var fadeTarget = document.querySelector(selector);
    if (fadeTarget != null) {
        var fadeEffect = setInterval(function () {
            if (!fadeTarget.style.opacity) {
                fadeTarget.style.opacity = 1;
            }
            if (fadeTarget.style.opacity > 0) {
                fadeTarget.style.opacity -= 0.1;
            } else {
                clearInterval(fadeEffect);
                callback();
            }
        }, 20);
    }
}


//  -----------------------------------------   CALENDAR  -------------------------------------------------------------

$(function () {
    $('.button-checkbox').each(function () {

        // Settings
        var $widget = $(this),
            $button = $widget.find('button'),
            $checkbox = $widget.find('input:checkbox'),
            color = $button.data('color'),
            settings = {
                on: {
                    icon: 'fa fa-square-o'
                },
                off: {
                    icon: 'fa fa-check-square-o'
                }
            };

        // Event Handlers
        $button.on('click', function () {
            $checkbox.prop('checked', !$checkbox.is(':checked'));
            $checkbox.triggerHandler('change');
            updateDisplay();
        });
        $checkbox.on('change', function () {
            updateDisplay();
        });

        // Actions
        function updateDisplay() {
            var isChecked = $checkbox.is(':checked');

            // Set the button's state
            $button.data('state', (isChecked) ? "on" : "off");

            // Set the button's icon
            $button.find('.state-icon')
                .removeClass()
                .addClass('state-icon ' + settings[$button.data('state')].icon);

            // Update the button's color
            if (isChecked) {
                $button
                    .removeClass('btn-default')
                    .addClass('btn-' + color + ' active');
            }
            else {
                $button
                    .removeClass('btn-' + color + ' active')
                    .addClass('btn-default');
            }
        }

        // Initialization
        function init() {

            updateDisplay();

            // Inject the icon if applicable
            if ($button.find('.state-icon').length == 0) {
                $button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i>');
            }
        }
        init();
    });
});


function DisableCalendarDays(field) {

    let booked_dates = ($('#booked_dates').val()).split(";");
    let booked_date_arr, booked_from_date = [], booked_to_date = [], current_date, b = 0, is_booked = false;

    for (let i = 0; i < booked_dates.length; i++) {
        booked_date_arr = booked_dates[i].split("_");
        if (booked_date_arr.length > 1) {
            booked_from_date[b] = new Date(booked_date_arr[0].replace(/-/g,"/")+" 00:00:00");
            booked_to_date[b] = new Date(booked_date_arr[1].replace(/-/g,"/")+" 00:00:00");
        }
        b++;
    }

    if ($('#label').length === 0) { return; }

    let month = parseInt($('.month_holder').attr("data-month"));
    let year = parseInt(($('#label').html()).split(" ")[1]);

    let curr_date, curr_day, curr_month, curr_year, i;

    if (field === "filter_date_from") {
        curr_date = new Date();
        curr_day = curr_date.getDate();
        curr_month = curr_date.getMonth() + 1;
        curr_year = curr_date.getFullYear();
        $("#filter_date_to").val("")
    } else {
        curr_date = ($("#filter_date_from").val()).split("/");
        curr_day = parseInt(curr_date[0]);
        curr_month = parseInt(curr_date[1]);
        curr_year = parseInt(curr_date[2]);
    }

    let day = 1;
    let td, tds;

    tds = document.getElementsByClassName('eformDayDisabled');
    for (i = 0; i < tds.length; i++) {
        tds[i].onclick = function () {
            return true;
        };
        tds[i].classList.remove('eformDayDisabled');
        i = 0;
    }

    tds = document.getElementsByClassName('eformDay');
    for (i = 0; i < tds.length; i++) {
        day = tds[i].innerHTML;
        current_date = new Date(year+"/"+month+"/"+day+" 00:00:00");
        for (let j = 0; j < booked_from_date.length; j++) {
            if (current_date >= booked_from_date[j] && current_date <= booked_to_date[j]) {
                is_booked = true;
            }
        }

        if (!(day==="") && ((year < curr_year) || (year === curr_year && month < curr_month) ||
            (year === curr_year && month === curr_month && day < curr_day)) || is_booked === true) {
            is_booked = false;
            tds[i].classList.add('eformDayDisabled');
            tds[i].onclick = function () {
                return false;
            }
        }
    }
}

$('.inp_date').on("click", function () {
    let field = $(this).attr("id");
    pureJSCalendar.close();
    let x = parseInt($(this).offset().left) - 24;
    let y = parseInt($(this).offset().top);
    //let obj_id = $(this).attr("id");
    pureJSCalendar.open('dd/MM/yyyy', x, y, 1, '2018-5-5', '2019-8-20', field, 2000);
    DisableCalendarDays(field);
    document.getElementById('prev').addEventListener('click', function () { DisableCalendarDays(field); });

});

function ValidateRequiredFields(parent_div) {
    let results = true;
    $("#"+parent_div+" :required").each(function () {
        if ($(this).val() === "") {
            $(this).addClass('is-invalid');
            results = false;
        }
    });

    return results;
}

$('#modal_login').on('hidden.bs.modal', function (e) {
    $('#modal_alert').addClass('hideOnly');
    $('#modal_alert_cap').addClass('hideOnly');
    $('#modal_alert_sms').addClass('hideOnly');
});

function ForgotPassword() {
    let emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    let email_field = $('#id_username');
    let pass_field = $('#id_password');
    let results_msg = $('#modal_alert');

    if (!emailReg.test(email_field.val()) || email_field.val() === "") {
        pass_field.addClass("hideOnly");
        results_msg.html("Por favor, entre seu e-mail corretamente para enviarmos uma nova senha");
        results_msg.addClass("alert-danger");
        results_msg.removeClass("hideOnly");
        //email_field.attr("oninvalid","this.setCustomValidity('Por favor, entre seu e-mail corretamente para enviarmos uma nova senha')");
        //$('#login_btn').trigger("click");
    } else {
        $.ajax({
           url: '../esqueci-a-senha',
           data: {
               'email': email_field.val()
           },
            dataType: 'json',
            success: function (data) {
               if (data.status == "ok") {
                results_msg.html("Uma nova senha foi enviada para o seu e-mail.");
                results_msg.removeClass("alert-danger");
                results_msg.addClass("alert-success");
                results_msg.removeClass("hideOnly");
                } else {
                    results_msg.html("Ops, ocorreu um erro no envio da sua nova senha. Por favor envie um e-mail para contato@bnboats.com para solicitar uma nova senha.");
                    results_msg.removeClass("alert-success");
                    results_msg.addClass("alert-danger");
                    results_msg.removeClass("hideOnly");
               }
            },
            error: function (error_msg) {
                results_msg.html("Ops, ocorreu um erro no envio da sua nova senha. Por favor envie um e-mail para contato@bnboats.com para solicitar uma nova senha.");
                results_msg.removeClass("alert-success");
                results_msg.addClass("alert-danger");
                results_msg.removeClass("hideOnly");
            }
        });
    }

    setTimeout(function () {
        //email_field.attr("oninvalid","this.setCustomValidity('Por favor, entre seu e-mail')");
        pass_field.removeClass("hideOnly");
        results_msg.html("");
        results_msg.removeClass("alert-success");
        results_msg.removeClass("alert-danger");
        results_msg.addClass("hideOnly");
    },10000);
}

// curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{}' ''

$("#modal_boat_reg").on("show", function () {
  $("body").addClass("modal-open");
}).on("hidden", function () {
  $("body").removeClass("modal-open")
});
