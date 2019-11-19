
$(document).ready(function() {

    $('.top_header_menu i, a, span').css("color", "dimgray");

    if ($(document).width() >= 1000) {
        $('#top_bar_search').removeClass('hideOnly');
    }

    // $('#top_bar_logo').attr("src", "/media/admin/logo_black.png");

    if ($('#id_address_country').length > 0) {
        ToggleOnyNumbersClass($('#id_address_country').val().toLowerCase(), 'brasil', 'id_address_postcode');
    }

    if ($('input[name=doc_type]:checked', '#ua_profile_form').length > 0) {
        ToggleOnyNumbersClass($('input[name=doc_type]:checked', '#ua_profile_form').val().toLowerCase(),
            'cpf', 'id_doc_number');
    }

    let boatId = $('#msg_focus').val();
    let chat_to_focus;
    if (boatId !== "") {
        chat_to_focus = $('#contact_'+boatId);
    } else {
        chat_to_focus = $('.ua_msg_contact').first();
    }
    if (chat_to_focus.length > 0 && ($(document).width() >= 765)) { chat_to_focus.trigger('click'); }

    $('#boat_favorities_div_1')
        .removeClass('hideOnly')
        .addClass('fav_show fav_first');
    $('#boat_favorities_div_2')
        .removeClass('hideOnly')
        .addClass('fav_show fav_mid')
        .attr('style', 'float: left');
    $('#boat_favorities_div_3')
        .removeClass('hideOnly')
        .addClass('fav_show fav_last');

    if ($('#add_boat').length && $('#add_boat').val() !== "") {
        modalCaptainProfile();
    }

    if ($(document).width() < 765) {
        ChangeChatToMobileVersion();
        $('.ua_msg_inputtext').each(function () {
           $(this).css("border-bottom-left-radius", "25px");
        });
        if (boatId !== "") {
            $('#contact_'+boatId).trigger('click');
        }
    }

    $('.select7_select option').each(function () {
        if ($(this).attr("selected") === "selected") {
            $(this).parent().val($(this).val()).change();
        }
    });
});

function ChangeChatToMobileVersion() {
    let div_main = $('#ua_message');
    let div_texts_area = $('#ua_msg_texts_area');
    let div_users_list = $('#ua_msg_users_list');
    div_main.css("margin", "0 10px 20px");
    div_texts_area.addClass("hideOnly");
    div_users_list.removeClass("hideOnly");
    div_users_list.css("width","100%");
    $('.ua_msg_back').each(function () {
       $(this).removeClass("hideOnly");
    });
}

function FavNextOrPrev(direction) {

    let fav_first = parseInt($('.fav_first').attr('data-id'));
    let fav_mid = parseInt($('.fav_mid').attr('data-id'));
    let fav_last = parseInt($('.fav_last').attr('data-id'));
    let obj_parent = $('.boat_favorities_div').parent();
    let fav_total = parseInt($('.boat_favorities_div').length);
    let fav_show;

    // if it's to move forward
    if (direction.toLowerCase() === "next") {
        if ((fav_last+1) <= fav_total) {
            fav_show = fav_last+1;
        } else {
            fav_show = 1;
        }

        let obj_fav_first_toHide = $('#boat_favorities_div_'+fav_first);
        obj_fav_first_toHide.addClass('hideOnly').removeClass('fav_show fav_first');

        let obj_fav_mid_toFirst = $('#boat_favorities_div_'+fav_mid);
        obj_fav_mid_toFirst.removeClass('fav_mid').addClass('fav_first');
        obj_fav_mid_toFirst.remove();

        let obj_fav_last_toMid = $('#boat_favorities_div_'+fav_last);
        obj_fav_last_toMid.removeClass('fav_last').addClass('fav_mid');
        obj_fav_last_toMid.remove();

        let obj_fav_show = $('#boat_favorities_div_'+fav_show);
        obj_fav_show.removeClass('hideOnly').addClass('fav_show fav_last');
        obj_fav_show.remove();

        obj_parent.append(obj_fav_mid_toFirst);
        obj_parent.append(obj_fav_last_toMid);
        obj_parent.append(obj_fav_show);

    // if it's to move back
    } else if (direction.toLowerCase() === "prev") {
        if ((fav_first-1) > 0) {
            fav_show = fav_first-1;
        } else {
            fav_show = fav_total;
        }

        let obj_fav_last_toHide = $('#boat_favorities_div_'+fav_last);
        obj_fav_last_toHide.removeClass('fav_show fav_last').addClass('hideOnly');

        let obj_fav_show = $('#boat_favorities_div_'+fav_show);
        obj_fav_show.removeClass('hideOnly').addClass('fav_show fav_first');
        obj_fav_show.remove();

        let obj_fav_first_toMid = $('#boat_favorities_div_'+fav_first);
        obj_fav_first_toMid.removeClass('fav_first').addClass('fav_mid');
        obj_fav_first_toMid.remove();

        let obj_fav_mid_toLast = $('#boat_favorities_div_'+fav_mid);
        obj_fav_mid_toLast.removeClass('fav_mid').addClass('fav_last');
        obj_fav_mid_toLast.remove();

        obj_parent.append(obj_fav_show);
        obj_parent.append(obj_fav_first_toMid);
        obj_parent.append(obj_fav_mid_toLast);

    }

}

$('#id_address_country').on('change', function () {
    ToggleOnyNumbersClass($('#id_address_country').val().toLowerCase(), 'brasil', 'id_address_postcode');
});

$('#id_doc_type').on('change', function () {
    ToggleOnyNumbersClass($('input[name=doc_type]:checked', '#ua_profile_form').val().toLowerCase(),
        'cpf', 'id_doc_number');
    $('#id_doc_number').val('')
        .removeClass('is-invalid')
        .removeClass('is-valid');
});

$('#id_doc_number').on('focusout', function () {
    ValidateCPF();
});

$('#id_doc_number').on('keyup', function (e) {
    if ($('input[name=doc_type]:checked', '#ua_profile_form').val().toLowerCase() !== "cpf") {
        $('#id_doc_number').removeClass('is-invalid')
            .removeClass('is-valid');
    }
    if ($('input[name=doc_type]:checked', '#ua_profile_form').val().toLowerCase() === "cpf") {
        if (($(this).val().length === 3 || $(this).val().length === 7) && (e.keyCode !== 8)) {
            $(this).val($(this).val() + '.');
        } else if (($(this).val().length === 11) && (e.keyCode !== 8)) {
            $(this).val($(this).val() + '-');
        }
    }
    if ($('input[name=doc_type]:checked', '#ua_profile_form').val().toLowerCase() === "cnpj") {
        if (($(this).val().length === 2 || $(this).val().length === 6) && (e.keyCode !== 8)) {
            $(this).val($(this).val() + '.');
        }
        if (($(this).val().length === 10) && (e.keyCode !== 8)) {
            $(this).val($(this).val() + '/');
        }
        if (($(this).val().length === 15) && (e.keyCode !== 8)) {
            $(this).val($(this).val() + '-');
        }

    }
});

function ToggleOnyNumbersClass(val_one, val_two, obj_id) {
    if (val_one === val_two) {
        $('#'+obj_id).addClass('onlyNumbers');
    } else {
        $('#'+obj_id).removeClass('onlyNumbers');
    }
}

function OpenUploadDialog(objId) {
    $('#'+objId).trigger('click');
}

function UploadPhoto() {
    $('#submit_newPhoto').trigger('click');
}

function SearchPostcode(postcodeId, streetId, areaId, cityId, ufId, addId, noId) {

    const address_country = $('#id_address_country');
    if (address_country.length) {
        if (address_country.val().toLowerCase() !== "brasil" || !isNaN(address_country.val())) {
            return;
        }
    }

    const xmlhttp = new XMLHttpRequest();
    const postcode = $('#'+postcodeId).val();
    let queryResults = {};

    xmlhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {

            try {
                queryResults = JSON.parse(this.responseText);
            } catch (e) {
                alert('error');
                return;
            }

            $('#'+streetId).val(queryResults.logradouro);
            if (areaId !== "") {
                $('#'+areaId).val(queryResults.bairro);
            }
            $('#'+cityId).val(queryResults.localidade);
            $('#'+ufId).val(queryResults.uf);
            if (addId !== "") {
                $('#'+addId).val('');
            }
            if (noId !== "") {
                $('#'+noId).val('')
                    .focus();
            }

         }
    };

    const link = "//viacep.com.br/ws/"+ postcode +"/json";
    xmlhttp.open("GET", link, true);
    xmlhttp.send();

}

function ValidateCPF() {

    if ($('input[name=doc_type]:checked', '#ua_profile_form').val().toLowerCase() !== "cpf") {
        return;
    }

    const cpf_obj = $('#id_doc_number');
    const cpf = cpf_obj.val().replace(/\D/g,'');
    let equalnumbers = true;

    let pOne_sum = 0;
    let pOne_factor = 10;

    if (cpf.length !== 11) {
        cpf_obj
            .removeClass("is-valid")
            .addClass("is-invalid");
        return;
    }

    for (let i = 0;i < cpf.length - 2; i++) {
        if (cpf.charAt(i) !== cpf.charAt(cpf.length-i-1)) {
            equalnumbers = false;
        }
        pOne_sum += cpf.charAt(i) * pOne_factor;
        pOne_factor--;
    }

    let code_firstChar = (pOne_sum*10)%11;

    if (code_firstChar === 10 || code_firstChar === 11) {
        code_firstChar = 0;
    }

    let pTwo_factor = 11;
    let pTwo_sum = 0;
    for (let i = 0;i < cpf.length - 1; i++) {
        pTwo_sum += cpf.charAt(i) * pTwo_factor;
        pTwo_factor--;
    }

    let code_secondChar = (pTwo_sum*10)%11;

    if (code_secondChar === 10 || code_secondChar === 11) {
        code_secondChar = 0;
    }

    if (parseInt(cpf.charAt(9)) === code_firstChar && parseInt(cpf.charAt(10)) === code_secondChar && equalnumbers === false) {
        console.log("OK");
        let formattedNo = cpf.charAt(0)+cpf.charAt(1)+cpf.charAt(2)+".";
        formattedNo +=  cpf.charAt(3)+cpf.charAt(4)+cpf.charAt(5)+".";
        formattedNo +=  cpf.charAt(6)+cpf.charAt(7)+cpf.charAt(8)+"-"+cpf.charAt(9)+cpf.charAt(10);
        cpf_obj.val(formattedNo)
            .removeClass("is-invalid")
            .addClass("is-valid");
    } else {
        cpf_obj
            .removeClass("is-valid")
            .addClass("is-invalid");
    }

}

$('#ua_submit').on('click', function () {
   if ($('#id_doc_number').hasClass('is-invalid')) {
       event.preventDefault();
       $('#ua_msg')
           .removeClass('hideOnly')
           .addClass('alert-danger')
           .html("CPF inválido");
       window.scrollTo(x-coord, y-coord);
       $('#id_doc_number').focus();
   }
});

function OpenContactChat(objId) {

    const contact_id = (objId.split("_"))[1];
    const chat_textarea = $('#msg_content_'+contact_id);

    //Hide all chats
    $('.ua_msg_content').each(function () {
       if ($(this).hasClass('hideOnly') === false) {
           $(this).addClass('hideOnly');
       }
    });

    //remove selected contact style from previous selection
    $('.ua_msg_selected_img').removeClass('ua_msg_selected_img');
    $('.ua_msg_selected_username').removeClass('ua_msg_selected_username');

    //get contact image and name
    const contact = $('#'+objId);
    const img = contact.find('img');
    const img_src = img.attr('src');
    const user = contact.find('.username');
    const username = user.html();
    const own_img = $('#own_img').attr('src');

    //add style for each chat message
    $('#msg_content_'+contact_id+' div div').each(function () {
        const obj = $(this);
        if (obj.attr('msg_type') === 'from') {
           obj.addClass('message-buble-right')
               .parent().find('.img-right')
               .removeClass('hideOnly')
               .find('img').attr('src', own_img);
        } else if (obj.attr('msg_type') === 'to') {
           obj.addClass('message-buble-left')
               .parent().find('.img-left')
               .removeClass('hideOnly')
               .find('img').attr('src', img_src);
        }
    });

    //add selected contact style
    img.addClass('ua_msg_selected_img');
    user.addClass('ua_msg_selected_username');

    //update chat header with image and name from selected contact
    const ua_msg_title = $(".ua_msg_title");
    ua_msg_title.find('img').attr('src', img_src);
    ua_msg_title.find('.username').html(username);

    //update send button to have the contact id
    $('#ua_msg_submit').attr('receiver', contact_id);

    //final step - show chat window ready
    chat_textarea.removeClass('hideOnly');

    if ($(document).width() < 765) {
        let div_texts_area = $('#ua_msg_texts_area');
        let div_users_list = $('#ua_msg_users_list');
        div_texts_area.removeClass("hideOnly");
        div_texts_area.css("width","100%");
        div_users_list.addClass("hideOnly");
    }

    chat_textarea.parent().scrollTop(chat_textarea.prop("scrollHeight"));

}

function SubmitMsg(objId) {

    const receiver = $('#'+objId).attr("receiver");
    // const sender = $('#user_id').val();
    const message = $('#ua_msg_new').val();

    // $('#id_id_from').val(parseInt(receiver));
    $('#id_id_to').val(receiver);
    $('#id_message').val(message);

    $('#form_message').submit();

}

//$('.boat_favorities_div_item > .fas').mouseenter(function () {
function ChangeToHeartBroken(objId) {
   $('#'+objId).removeClass('fa-heart');
   $('#'+objId).addClass('fa-heart-broken');
}
//});

//$('.boat_favorities_div_item > .fas').mouseleave(function () {
function ChangeBackToHeart(objId) {
    $('#'+objId).addClass('fa-heart');
    $('#'+objId).removeClass('fa-heart-broken');
}
//});

function FavChangePriceSel(boat_id) {
    let selected_option = $('#'+boat_id+' option:selected').attr('value');
    $('#boat_div_'+boat_id+' .boat_price').each(function() {
       if (!$(this).hasClass('hideOnly')) {
           $(this).addClass('hideOnly');
       }
    });
    $('#boat_'+boat_id+'_'+selected_option).removeClass('hideOnly');
}

function RemoveFavorite(boat_id) {
    $('#ua_fav_to_remove').val(boat_id);
    $('#ua_favorites_form').submit();
}

function BoatReg_Move(direction, objId) {
    let page_id = parseInt($(objId).attr("pag-id"));
    let pag_direction;
    let boat_type = $('#boat_type_inp').val();

    if (objId.parentElement) {
        let parent_div_id = objId.parentElement.parentElement.id;
        let parent_div = $('#'+parent_div_id);
        let boat_update = $('#updated_boat').val();
        if (parent_div.find('.mandatory').val() === "" && direction === "next" && (boat_update === "")) {
            alert(parent_div.attr('data-err'));
            return;
        }
    }

    // if not boat type Fishing or if its not last page of regular form
    if (boat_type !== "PES" || page_id < 18 || page_id === 30) {
        // if its go next, just go to next page, if not, go back one page
        if (direction === "next") {
            pag_direction = page_id + 1;
            if (page_id === 7) {
                pag_direction = 30;
            }
            if (page_id === 30) {
                pag_direction = 8;
            }
        } else {
            pag_direction = page_id - 1;
            if (page_id === 8) {
                pag_direction = 30;
            }
            if (page_id === 30) {
                pag_direction = 7;
            }
        }
    // if its boat type fishing and last page of regular form or already in the fishing form
    } else {
        if (direction === "next") {
            // if its next and this is the last page of regular form, skip next page (18) as its the complete page
            if (page_id === 18) {
                pag_direction = page_id + 2;
            //if its the last page of fishing form, go back to page 18, which is the complete page
            } else if (page_id === 24) {
                pag_direction = 19;
            // if none of the cases above, just go forward 1 page
            } else {
                pag_direction = page_id + 1;
            }
        } else {
            // if its to go back, but its the first page of fishing form, skip one as page 18 is the complete page
            if (page_id === 20) {
                pag_direction = page_id - 2;
            } else {
                pag_direction = page_id - 1;
            }
        }
    }

    $(objId).parent().parent().addClass("hideOnly");
    $("#boat_reg_div_"+pag_direction).removeClass("hideOnly");
}

function BoatReg_Option_Click(btnId, inpId, ValueText) {
    let clicked_btn = $('#'+btnId);
    let inp = $('#'+inpId);
    let fishes = "";
    if (inpId.substring(0, 4) !== 'fish' && inpId.substring(0, 8) !== 'edt_fish' ) {
        clicked_btn.parents('.row').find('.boat_reg_btn_cliked').removeClass('boat_reg_btn_cliked');
        clicked_btn.addClass('boat_reg_btn_cliked');
        inp.val(ValueText);
        let arrow_obj = clicked_btn.parents('.boat_reg_div').find('.boat_reg_arrows')[1];
        BoatReg_Move("next", arrow_obj);
    } else {
        let currentVal = inp.val();
        if (clicked_btn.hasClass('boat_reg_btn_cliked')) {
            clicked_btn.removeClass('boat_reg_btn_cliked');
            inp.val(currentVal.replace(ValueText+";", ""));
        } else {
            clicked_btn.addClass('boat_reg_btn_cliked');
            let parent_div = inp.parent().attr("id");
            $('#'+parent_div+" .boat_reg_btn_cliked").each(function () {
                fishes += $(this).attr("id").split("_").slice(-1)[0]+";";
            });
            inp.val(fishes);
        }
    }
}

function TriggerFileInput(objId) {
    if ($('#photos_edit_mode').length) {
        if ($('#photos_edit_mode').val() === "1") {
            $('.selected_pic').each(function () {
               $(this).removeClass("selected_pic");
            });
            let img_id = objId.replace("inp_","");
            $('#'+img_id).addClass("selected_pic");
            $('#main_photo').remove();
            $('#'+img_id).parent().append("<p class=\"fontSizeZeroEight\" style=\"text-align: center;padding-top: 5px;\" id=\"main_photo\">DESTAQUE</p>");

            let pic_inp_obj = $('#'+objId);
            if (pic_inp_obj.val() !== "") {
                str_filename = pic_inp_obj.val().split("\\").slice(-1);
            } else {
                str_filename = pic_inp_obj.attr("files");
            }
            $('#selected_main_photo').val(str_filename);
            ChangeMainPic(true);
            return;
        }
    }
    $('#'+objId).trigger('click');

}

$('#inp_pic_1, #inp_pic_2, #inp_pic_3, #inp_pic_4, #inp_pic_5, #inp_pic_6, #edt_inp_pic_1, #edt_inp_pic_2, ' +
'#edt_inp_pic_3, #edt_inp_pic_4, #edt_inp_pic_5, #edt_inp_pic_6').on("change", function () {
   // if ((this.id).substr(0, 8) === "inp_pic_") {
        $('#loaderIconBoatImage').removeClass("hideOnly");
        $('#loaderIconBoatImageEdit').removeClass("hideOnly");
        UploadBoatPicture(this);
    //}
    let img = this.files[0];
    let objId = (this.id).replace("inp_","");
    let objIdView = objId.replace("edt_","view_");
    let imgObj = document.getElementById(objId);
    let reader  = new FileReader();
    let deleted_photo = $(this).attr("files");

    reader.onloadend = function () {
        imgObj.src = reader.result;
        if ($('#' + objIdView).length) {
            let imgObjView = document.getElementById(objIdView);
            imgObjView.src = reader.result;
        }
        let photos_to_del = $('#photos_to_del').val();
        $('#photos_to_del').val(photos_to_del+deleted_photo+",");
    };

    if (img) {
        reader.readAsDataURL(img);
    } else {
        imgObj.src = "";
    }

});

function allowDrop(ev) {
  ev.preventDefault();
}

function DragBoatPhoto(ev) {
    let dragged_srv = $('#'+ev.target.id).attr("src");
    ev.dataTransfer.setData("src", dragged_srv);
    let inp_id = ev.target.id.replace("edt_pic","edt_inp_pic");
    ev.dataTransfer.setData("id", inp_id);
}

function DropBoatPhoto(ev) {
    ev.preventDefault();
    //$('#drag_drop_message').addClass("hideOnly");
    $('#edt_mainpic').removeClass("hideOnly");
    $('#div_mainpic').css("border", "none");

    let data = ev.dataTransfer.getData("src");
    $('#edt_mainpic').attr("src", data);

    let str_filename = "";
    let objId = ev.dataTransfer.getData("id");
    let pic_inp_obj = $('#'+objId);
    if (pic_inp_obj.val() !== "") {
        str_filename = pic_inp_obj.val().split("\\").slice(-1);
    } else {
        str_filename = pic_inp_obj.attr("files");
    }
    $('#selected_main_photo').val(str_filename);

    $('.edit_img .selected_pic').each(function () {
       $(this).removeClass("selected_pic");
    });
    let img_id = objId.replace("inp_","").replace("edt_","view_");

    $('#'+img_id).addClass("selected_pic");
    $('#main_photo').remove();
    $('#'+img_id).parent().append("<p class=\"fontSizeZeroEight\" style=\"text-align: center;padding-top: 5px;\" id=\"main_photo\">DESTAQUE</p>");
}

function DeletePhoto(obj_id) {
    let div = $('#div_' + obj_id);
    let img = $('#edt_' + obj_id);
    let img_view = $('#view_' + obj_id);
    let inp = $('#edt_inp_' + obj_id);

    let deleted_photo = inp.attr("files");
    let photos_to_del = $('#photos_to_del').val();
    $('#photos_to_del').val(photos_to_del+deleted_photo+",");

    if ($('#edt_mainpic').attr("src") === img.attr("src")) {
        $('#selected_main_photo').val("");
        $('#edt_mainpic').attr("src","").addClass("hideOnly");
        $('#drag_drop_message').removeClass("hideOnly");
    }

    inp.val("");
    img.attr("src","");
    img_view.attr("src","");

}

function UploadBoatPicture(picture) {
    //let formData = new FormData(document.getElementById(picture.id));
    let formData = new FormData();
    formData.append('file', $(picture)[0].files[0]);
    $.ajax({
        type: 'POST',
        url: "../salvar-imagem-barco",
        data: formData,
        cache:false,
        contentType: false,
        processData: false,
        success:function(data){
            console.log("success");
            //$(picture).parent().find('.inp_pic_id').val(data);
            $(picture).next(".inp_pic_id").val(data);
            $(picture).val("");
            $('#loaderIconBoatImage').addClass("hideOnly");
            $('#loaderIconBoatImageEdit').addClass("hideOnly");
        },
        error: function(data){
            console.log("error");
        }
    });
}

function update_edt_boatamenities_inp() {
    let amenities_array = "";
    let get_items = get_selected_items('edt_boat_amenities_div_1','value');
    if (get_items !== null) {
        amenities_array = get_items+",";
    }
    get_items = get_selected_items('edt_boat_amenities_div_2','value');
    if (get_items !== null) {
        amenities_array = amenities_array.concat(get_items+",");
    }
    get_items = get_selected_items('edt_boat_amenities_div_3','value');
    if (get_items !== null) {
        amenities_array = amenities_array.concat(get_items+",");
    }
    get_items = get_selected_items('edt_boat_amenities_div_4','value');
    if (get_items !== null) {
        amenities_array = amenities_array.concat(get_items+",");
    }
    get_items = get_selected_items('edt_boat_amenities_div_5','value');
    if (get_items !== null) {
        amenities_array = amenities_array.concat(get_items+",");
    }
    $('#edt_boat_amenities').val(amenities_array);
}

function update_boatamenities_inp() {
    let amenities_array = "";
    let get_items = get_selected_items('boat_amenities_div_1','value');
    if (get_items !== null) {
        amenities_array = get_items+",";
    }
    get_items = get_selected_items('boat_amenities_div_2','value');
    if (get_items !== null) {
        amenities_array = amenities_array.concat(get_items+",");
    }
    get_items = get_selected_items('boat_amenities_div_3','value');
    if (get_items !== null) {
        amenities_array = amenities_array.concat(get_items+",");
    }
    get_items = get_selected_items('boat_amenities_div_4','value');
    if (get_items !== null) {
        amenities_array = amenities_array.concat(get_items+",");
    }
    get_items = get_selected_items('boat_amenities_div_5','value');
    if (get_items !== null) {
        amenities_array = amenities_array.concat(get_items+",");
    }
    $('#boat_amenities').val(amenities_array);
}

function update_boat_pincludes_inp() {
    let pincludes_1 = get_selected_items('boat_pincludes_1','value');
    let pincludes_2 = get_selected_items('boat_pincludes_2','value');
    let pincludes_3 = get_selected_items('boat_pincludes_3','value');
    let pincludes_4 = get_selected_items('boat_pincludes_4','value');
    $('#boat_pincludes_inp_1').val(pincludes_1);
    $('#boat_pincludes_inp_2').val(pincludes_2);
    $('#boat_pincludes_inp_3').val(pincludes_3);
    $('#boat_pincludes_inp_4').val(pincludes_4);
}

function update_edt_boat_pincludes_inp() {
    let pincludes_1 = get_selected_items('edt_div_boat_pincludes_1','value');
    let pincludes_2 = get_selected_items('edt_div_boat_pincludes_2','value');
    let pincludes_3 = get_selected_items('edt_div_boat_pincludes_3','value');
    let pincludes_4 = get_selected_items('edt_div_boat_pincludes_4','value');
    $('#edt_boat_pincludes_inp_1').val(pincludes_1);
    $('#edt_boat_pincludes_inp_2').val(pincludes_2);
    $('#edt_boat_pincludes_inp_3').val(pincludes_3);
    $('#edt_boat_pincludes_inp_4').val(pincludes_4);
}

function update_boat_fspecies_inp() {
    let fspecies_1 = get_selected_items('boat_fspecies_3','value');
    $('#boat_fspecies_inp').val(fspecies_1);
}

function update_edt_boat_fspecies_inp() {
    let fspecies_1 = get_selected_items('edt_boat_fspecies_3','value');
    $('#edt_boat_fspecies_inp').val(fspecies_1);
}

function remove_selected_item(elem, e) {
    e.stopPropagation();
    var option_text = elem.parentElement.querySelector(".select7_content").innerHTML;
    var option_value = elem.parentElement.querySelector(".select7_content").dataset.optionValue;
    var selector = elem.parentElement.parentElement.parentElement.querySelector(".select7_select");

    // selector.innerHTML += `<option value="${ option_value }">${ option_text }</option>`;
    selector.innerHTML += "<option value='"+ option_value +"'>"+ option_text +"</option>";

    if (selector.length > 1)
        selector.style.display = "block";

    var selected_items = elem.parentElement.parentElement.parentElement.querySelectorAll(".select7_item");
    if (selected_items.length == 1) {
        var placeholder = elem.parentElement.parentElement.parentElement.querySelector(".select7_placeholder");
        placeholder.style.display = "block";
    }

    // elem.parentElement.remove();
    elem.parentElement.parentElement.removeChild(elem.parentElement);

    if ($('#'+selector.id).hasClass("boat_edt")) {
        if ((selector.id).search("amenities") >= 0) {
            update_edt_boatamenities_inp();
        } else if ((selector.id).search("pincludes") >= 0) {
            update_edt_boat_pincludes_inp();
        } else if ((selector.id).search("fspecies") >= 0) {
            update_edt_boat_fspecies_inp();
        }
    } else {
        if ((selector.id).search("amenities") >= 0) {
            update_boatamenities_inp();
        } else if ((selector.id).search("pincludes") >= 0) {
            update_boat_pincludes_inp();
        } else if ((selector.id).search("fspecies") >= 0) {
            update_boat_fspecies_inp();
        }
    }
}

function add_selected_item(elem, e) {
    e.stopPropagation();
    var option_text =  elem[elem.selectedIndex].text;
    var option_value =  elem[elem.selectedIndex].value;
    var selected_items = elem.parentElement.querySelector(".select7_items");
    var placeholder = elem.parentElement.querySelector(".select7_placeholder");
    if (option_value === "filler" && option_text === "")
        return;

    $('.select7_container').each(function () {
       if ($(this).height() > 100) {
           var id = $(this).parent().attr("id");
            $('#'+id+' .select7_container').each(function () {
                $(this).css("width","100%");
                $(this).css("margin-right","0");
            });
       }
    });

    $(placeholder).parent().css("padding-top","20px");
    $(placeholder).css("top","10px");
    //placeholder.style.display = "none";
    // selected_items.innerHTML += `
    //     <div class="select7_item">
    //         <div data-option-value="${option_value}" class="select7_content">${option_text}</div>
    //         <div class="select7_del" onclick="remove_selected_item(this, event);">&#10006;</div>
    //     </div>`;

    selected_items.innerHTML += "<div class='select7_item'><div data-option-value='"+ option_value +"' class='select7_content'>"+ option_text +"</div><div class='select7_del' onclick='remove_selected_item(this, event);'><div class='select7_x'></div><div class='select7_x'></div></div></div> ";

    // elem[elem.selectedIndex].remove();
    elem[elem.selectedIndex].parentElement.removeChild(elem[elem.selectedIndex]);
    if (elem.length == 1)
        elem.style.display = "none";

    if ($('#'+elem.id).hasClass("boat_edt")) {
        if ((elem.id).search("amenities") >= 0) {
            update_edt_boatamenities_inp();
        } else if ((elem.id).search("pincludes") >= 0) {
            update_edt_boat_pincludes_inp();
        } else if ((elem.id).search("fspecies") >= 0) {
            update_edt_boat_fspecies_inp();
        }
    } else {
        if ((elem.id).search("amenities") >= 0) {
            update_boatamenities_inp();
        } else if ((elem.id).search("pincludes") >= 0) {
            update_boat_pincludes_inp();
        } else if ((elem.id).search("fspecies") >= 0) {
            update_boat_fspecies_inp();
        }
    }
}

function get_selected_items(select7_id, type/* = "both"*/) {
    type = type || "both";
    var selected_items = document.getElementById(select7_id).querySelectorAll(".select7_content");

    if (selected_items.length > 0) {
        var selected_values = [];

        if (type == "value")
            for (let i = 0; i < selected_items.length; i++)
                selected_values.push(selected_items[i].dataset.optionValue);

                if (type == "text")
            for (let i = 0; i < selected_items.length; i++)
                selected_values.push(selected_items[i].innerHTML);

        if (type == "both")
            for (let i = 0; i < selected_items.length; i++)
                selected_values.push({
                    "text": selected_items[i].innerHTML,
                    "value": selected_items[i].dataset.optionValue,
                });

        return selected_values;
    }

    return null;
}

function PriceChange(obj_id) {
    let obj_val = ($('#'+obj_id).val()).replace(",",".");
    let obj_pinclude;
    if (isNaN(obj_val)) { return; }
    obj_val = parseInt(obj_val);

    switch (obj_id) {
        case "price_item_single":
            obj_pinclude = $('#boat_pincludes_1');
            break;
        case "price_item_hday":
            obj_pinclude = $('#boat_pincludes_2');
            break;
        case "price_item_day":
            obj_pinclude = $('#boat_pincludes_3');
            break;
        case "price_item_overnight":
            obj_pinclude = $('#boat_pincludes_4');
            break;
    }

    if (obj_val > 0) {
        obj_pinclude.removeClass("hideOnly");
    } else {
        obj_pinclude.addClass("hideOnly");
    }
}
$( "#review_score_div .far" ).on("click", function () {
    $('#review_score_div .fas').each(function () {
        $( this ).removeClass("fas");
        $( this ).addClass("far");
    });
    let score = $( this ).attr("score");
    $('#review_score').val(score);
    $('#score_description').html($( this ).attr('score-desc'));
    $('#review_score_div .far').each(function () {
       if (parseInt($(this).attr("score")) <= score) {
            $( this ).removeClass("far");
            $( this ).addClass("fas");
       }
    });
});

$( "#review_score_div .far" ).hover(
    function() {
        if ($('#review_score').val() === "") {
            let score = parseInt($(this).attr("score"));
            $('#score_description').html($(this).attr('score-desc'));
            $('#review_score_div .far').each(function () {
                if (parseInt($(this).attr("score")) <= score) {
                    $(this).removeClass("far");
                    $(this).addClass("fas");
                }
            });
        }
    }, function() {
        if ($('#review_score').val() === "") {
            $('#review_score_div .fas').each(function () {
                $( this ).removeClass("fas");
                $( this ).addClass("far");
            });
            $('#score_description').html('');
        }
    }
);

function UpdateBookingId(booking_id, customer_id, page) {
    if (page === "bookings") {
        $('#booking_review_id').val(booking_id);
    } else {
        $('#passenger_review_id').val(customer_id);
    }
}

function UpdateBoatStatus(boat_id, new_status) {
    let action;
    if (new_status === "Paused") {
        action = "pausar";
    } else if (new_status === "Deleted") {
        action = "apagar";
    }

    if (confirm("Tem certeza que deseja "+action+" o seu anúncio?")) {
        $('#boat_id').val(boat_id);
        $('#boat_status').val(new_status);
        $('#update_status_form').submit();
    }
}

function UpdateBoat(boat_id) {
    $('#boat_id').val(boat_id);
    $('#boat_status').val("update");
    $('#update_status_form').submit();
}

function EditBoat() {
    $('#ua_boat_reg').addClass("hideOnly");
    $('#ua_boat_edit').removeClass("hideOnly");
}

function BackToBoatsList() {
    $('#ua_boat_reg').removeClass("hideOnly");
    $('#ua_boat_edit').addClass("hideOnly");
}

function ApproveBooking(is_approved) {
    event.preventDefault();
    console.log(is_approved);
    $('#approve_booking_action').val(is_approved);
    console.log($('#approve_booking_action').val());
    $('#approve_booking_form').submit();
}

function BookingCancelRequest(form_id, current_status) {
    event.preventDefault();
    let message = "";
    if (current_status === "Confirmed") {
        message = "Você tem certeza que deseja cancelar sua reserva? Favor consultar a política de cancelamento para entender possíveis taxas que serão cobradas.";
    } else {
        message = "Você tem certeza que deseja recusar esse pedido de reserva?";
    }
    if (confirm(message)) {
        $('#'+form_id).submit();
    }
}

function GetBoatDetails(boat_no, debug) {

    $.ajax({
       url: '../meus-barcos/ler-barco',
       data: {
           'boat_no': boat_no
       },
        dataType: 'json',
        success: function (data) {

            $('#edt_boat_title').val(data.title);
            $('#edt_boat_reg_title').val(data.title);
            $("#edt_boat_type_inp").val(data.boat_type_id).change();
            $("#edt_boat_fab_year").val(data.fab_year).change();
            $("#edt_boat_manufactor").val(data.manufacturer).change();
            $("#edt_boat_size").val(data.size).change();
            $("#edt_boat_capacity").val(data.capacity).change();
            $("#edt_boat_overnight_capacity").val(data.overnight_capacity).change();
            $("#edt_boat_rooms").val(data.rooms).change();
            $("#edt_boat_bathrooms").val(data.bathrooms).change();
            $("#edt_pet_inp").val(data.animals).change();
            $("#edt_smoking_inp").val(data.smoke).change();
            $("#edt_accessibility_inp").val(data.wheelchair).change();
            $('#edt_address_street').val(data.address);
            $('#edt_address_city').val(data.city_name);
            $("#edt_address_state").val(data.state_name).change();
            $('#edt_boat_reg_description').val(data.description);
            $('#edt_price_item_single').val(data.owner_price_single.replace(".",","));
            $('#edt_price_item_hday').val(data.owner_price_half_day.replace(".",","));
            $('#edt_price_item_day').val(data.owner_price_day.replace(".",","));
            $('#edt_price_item_overnight').val(data.owner_price_overnight.replace(".",","));
            $("#edt_boat_edit_fish_type").val(data.fish_rules).change();
            $('#edt_updated_boat').val(data.id);
            $('#booked_dates').val(data.bookings);

            // BOAT AMENITIES
            if (data.amenities !== null && data.amenities !== "") {
                let amenities = data.amenities.split(",");
                let amenities_inp = "";
                $('#edt_boat_amenities').val("");
                for (var i = 0; i < amenities.length - 1; i++) {
                    $('.select7_select option').each(function () {
                        if ($(this).html() === amenities[i]) {
                            $(this).attr("selected", "selected");
                            $(this).parent().val($(this).val()).change();
                            amenities_inp = $('#edt_boat_amenities').val();
                            $('#edt_boat_amenities').val(amenities_inp + "," + $(this).val());
                        }
                    });
                }
            }

            // BOAT IMAGES
            $('.edit_img img').each(function () {
               $(this).attr("src","");
            });
            $('.edit_img_popup img').each(function () {
               $(this).attr("src","");
            });
            $('.inp_pic_id').each(function () {
               $(this).val("");
            });
            $('.edt_inp_pic').each(function () {
               $(this).val("");
               $(this).attr("files","");
            });
            if (data.images !== null && data.images !== "") {
                let boat_images = data.images.split(",");
                $('#selected_main_photo').val(boat_images[0].split("/").slice(-1)[0]);
                for (i = 0; i < boat_images.length - 1; i++) {
                    if ($('#view_pic_' + (i + 1)).length) {
                        $('#view_pic_' + (i + 1)).attr("src", boat_images[i]);
                    }
                    $('#edt_pic_' + (i + 1)).attr("src", boat_images[i]);
                    $('#edt_inp_pic_' + (i + 1)).attr("files", boat_images[i].split("/").slice(-1)[0]);
                }
            }

            // GET SINGLE TRIP PRICE INCLUDES
            if (data.boat_single_includes !== null && data.boat_single_includes !== "") {
                let boat_single_includes = data.boat_single_includes.split(",");
                let boat_single_includes_inp = "";
                $('#edt_boat_pincludes_inp_1').val("");
                for (i = 0; i < boat_single_includes.length - 1; i++) {
                    $('#edt_boat_pincludes_1 option').each(function () {
                        if ($(this).html() === boat_single_includes[i]) {
                            $(this).attr("selected", "selected");
                            $(this).parent().val($(this).val()).change();
                            boat_single_includes_inp = $('#edt_boat_pincludes_inp_1').val();
                            $('#edt_boat_pincludes_inp_1').val(boat_single_includes_inp + "," + $(this).val());
                        }
                    });
                }
            }

            // GET HALF DAY TRIP PRICE INCLUDES
            if (data.boat_hday_includes !== null && data.boat_hday_includes !== "") {
                let boat_hday_includes = data.boat_hday_includes.split(",");
                let boat_hday_includes_inp = "";
                $('#edt_boat_pincludes_inp_2').val("");
                for (i = 0; i < boat_hday_includes.length - 1; i++) {
                    $('#edt_boat_pincludes_2 option').each(function () {
                        if ($(this).html() === boat_hday_includes[i]) {
                            $(this).attr("selected", "selected");
                            $(this).parent().val($(this).val()).change();
                            boat_hday_includes_inp = $('#edt_boat_pincludes_inp_2').val();
                            $('#edt_boat_pincludes_inp_2').val(boat_hday_includes_inp + "," + $(this).val());
                        }
                    });
                }
            }

            // GET DAY TRIP PRICE INCLUDES
            if (data.boat_day_includes !== null && data.boat_day_includes !== "") {
                let boat_day_includes = data.boat_day_includes.split(",");
                let boat_day_includes_inp = "";
                $('#edt_boat_pincludes_inp_3').val("");
                for (i = 0; i < boat_day_includes.length - 1; i++) {
                    $('#edt_boat_pincludes_3 option').each(function () {
                        if ($(this).html() === boat_day_includes[i]) {
                            $(this).attr("selected", "selected");
                            $(this).parent().val($(this).val()).change();
                            boat_day_includes_inp = $('#edt_boat_pincludes_inp_3').val();
                            $('#edt_boat_pincludes_inp_3').val(boat_day_includes_inp + "," + $(this).val());
                        }
                    });
                }
            }

            // GET OVERNIGHT TRIP PRICE INCLUDES
            if (data.boat_overnight_includes !== null && data.boat_overnight_includes !== "") {
                let boat_overnight_includes = data.boat_overnight_includes.split(",");
                let boat_overnight_includes_inp = "";
                $('#edt_boat_pincludes_inp_4').val("");
                for (i=0;i<boat_overnight_includes.length-1;i++) {
                    $('#edt_boat_pincludes_4 option').each(function () {
                        if ($(this).html() === boat_overnight_includes[i]) {
                            $(this).attr("selected", "selected");
                            $(this).parent().val($(this).val()).change();
                            boat_overnight_includes_inp = $('#edt_boat_pincludes_inp_4').val();
                            $('#edt_boat_pincludes_inp_4').val(boat_overnight_includes_inp+","+$(this).val());
                        }
                    });
                }
            }

            // GET FISH SPECIES
            if (data.fish_species !== null && data.fish_species !== "") {
                let fish_species = data.fish_species.split(",");
                let edt_boat_fspecies_inp = "";
                $('#edt_boat_fspecies_inp').val("");
                for (i=0;i<fish_species.length-1;i++) {
                    $('#edt_boat_fspecies_1 option').each(function () {
                        if ($(this).html() === fish_species[i]) {
                            $(this).attr("selected", "selected");
                            $(this).parent().val($(this).val()).change();
                            edt_boat_fspecies_inp = $('#edt_boat_fspecies_inp').val();
                            $('#edt_boat_fspecies_inp').val(edt_boat_fspecies_inp+","+$(this).val());
                        }
                    });
                }
            }

            if (data.fish_bait !== null && data.fish_bait !== "") {
                //$('#edt_fish_bait_inp').val(data.fish_bait);
                let fish_baits = data.fish_bait.split(";");
                for (i=0;i<fish_baits.length-1;i++) {
                    $('#edt_fish_bait_opt_'+fish_baits[i]).trigger("click");
                }
            }

            if (data.fish_places !== null && data.fish_places !== "") {
                //$('#edt_fish_place_inp').val(data.fish_places);
                let fish_places = data.fish_places.split(";");
                for (i=0;i<fish_places.length-1;i++) {
                    $('#edt_fish_place_opt_'+fish_places[i]).trigger("click");
                }
            }

            LoadFullCalendars();

            // open boat edit page
            EditBoat();
        },
        error: function (error_msg) {
            console.log(error_msg);
        }
    });
}

function fishing_area_display(select_obj_id) {
    let boat_type = $('#' + select_obj_id + ' :selected').val();
    if (boat_type === "PES") {
        $('#fishing_area_div').removeClass("hideOnly");
    } else {
        $('#fishing_area_div').addClass("hideOnly");
    }
}

function ChangeMainPic(option) {
    if (option === false) {
        $('#click_tochange').addClass("hideOnly");
        $('#select_img').removeClass("hideOnly");
        $('#photos_edit_mode').val("1");
    } else {
        $('#click_tochange').removeClass("hideOnly");
        $('#select_img').addClass("hideOnly");
        $('#photos_edit_mode').val("0");
    }
}



function SaveBlockingDates() {
    let barco = $('#edt_updated_boat').val();
    let date_array = ($('#block_date_from').val()).split("/");
    let date_chk = $('#chk_block_date_from').is(':checked');

    $.ajax({
        url: "../bloquear-datas",
        data: {
            "barco": barco,
            "date_from": date_array[2]+"-"+date_array[1]+"-"+date_array[0],
            "date_availability": date_chk
        },
        success:function(data){
            $('#booked_dates').val(data);
            LoadFullCalendars();
            $('#modal_calendar').modal('hide');
        },
        error: function(data){
            console.log("error: " + data);
        }
    });
}

function SetDateAvailability() {
    let curr_style = $('#block_date_from').attr("style")
        .replace("background-color: white !important","")
        .replace("background-color: #f1f3f7 !important","");
    if ($('#chk_block_date_from').is(":checked")) {
        $('#lbl_block_date_from').html("Data disponível");
        $('#block_date_from').attr("style", curr_style + "background-color: white !important");
    } else {
        $('#lbl_block_date_from').html("Data indisponível");
        $('#block_date_from').attr("style", curr_style + "background-color: #f1f3f7 !important");
    }
}