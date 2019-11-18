
$(document).ready(function() {

    Boat_Type_Onchange();

    $('.boat_img_div').each(function () {
       $('.boat_img_div').addClass("hideOnly");
    });
    $('.boat_img_div').first().removeClass("hideOnly");

    LoadFullCalendars();

});

$('#top_bar_search').removeClass("hideOnly");
$('.top_navBar_username').each(function() {
   $(this).css("color","dimgray");
});

function BoatImageNextOrPrev(direction, obj_arrow) {

    if ($(obj_arrow).hasClass('disabled')) {
        return;
    }

    let div_counter = $('.boat_img_div').length;
    let id = $(obj_arrow).attr('pag-id');

    $('#boat_img_'+id).addClass("hideOnly");

    if (direction == "next") {
        id = (parseInt(id)+1);
        $('#boat_img_'+id).removeClass("hideOnly");
        $('.left-arrow, .right-arrow').attr('pag-id', id);
    } else {
        id = parseInt(id)-1
        $('#boat_img_'+id).removeClass("hideOnly");
        $('.left-arrow, .right-arrow').attr('pag-id', id);
    }

    if (id == "1") {
        $('.left-arrow').addClass("disabled");
    } else {
        $('.left-arrow').removeClass("disabled");
    }

    if (id == div_counter) {
        $('.right-arrow').addClass("disabled");
    } else {
        $('.right-arrow').removeClass("disabled");
    }

}

function Boat_Type_Onchange() {
   let btype = $("#booking_type_select").val();
   let newprice = $('#boat_price_'+btype).val();
   let disc_newprice = $('#bprice_disc_'+btype).val();
   $('#booking_total').html(newprice);
   $('#booking_total_final').html(disc_newprice);
   $('#booking_total_price').val(parseInt(newprice));
   if (btype !== "24") {
      $('#filter_date_to').val("").attr("disabled", "disabled").removeClass("pholder_blue");
   } else {
      $('#filter_date_to').attr("disabled", false).addClass("pholder_blue");
   }
}

function PaymentSelection(obj_id) {
   event.preventDefault();
   if ($('#pay_'+obj_id).prop("checked") === false) {
      $('.collapse').collapse('hide');
      $('#pay_'+obj_id).prop("checked", "checked");
   }
}

function PaymentSelection_Expand(obj_id) {
   $('.collapse').collapse('hide');
   $('#'+obj_id).collapse('show');
}

function CreateBooking() {

    if (ValidateRequiredFields("bview_booking_dates") === false) {
        $('#booking_message').html('Por favor, preencha os campos em vermelho')
            .removeClass("hideOnly").addClass("alert-danger");
        setTimeout(function() {
            $('#booking_message').html('').removeClass("alert-danger").addClass("hideOnly");
            $("#bview_rd_item_div :required").each(function () {
                $(this).removeClass('is-invalid');
            });
        },10000);
        return;
    }

    $('#booking_request').attr("disabled", 'disabled');

    $.ajax({
        url: '../criacao-de-reserva',
        data: {
            'booking_type': $('#booking_type_select').val(),
            'booking_date_from': $('#filter_date_from').val(),
            'booking_date_to': $('#filter_date_to').val(),
            'booking_pax': $('#booking_pax').val(),
            'booking_total_price': ($('#booking_total').html()).replace(",", "."),
            'boat_pk': $('#boat_pk').val(),
        },
        dataType: 'json',
        complete: function (data) {
            try {
                let booking = JSON.parse(data.responseText);
                $('#payment_div').removeClass("hideOnly");
                $('#booking_no').val(booking.booking_id);
                $('#cust_doc_no').val(booking.doc_no);
                $('#cust_street').val(booking.street);
                $('#cust_street_no').val(booking.street_no);
                $('#cust_city_area').val(booking.city_area);
                $('#cust_postcode').val(booking.postcode);
                $('#cust_city_id').val(booking.city_code);
                $('#booking_total_price').val(booking.booking_total);
            } catch (e) {
                $('#booking_message').html('Ops, houve um erro na reserva. Por favor, nos contate em contato@bnboats.com. Obrigado.')
                    .removeClass("hideOnly").addClass("alert-danger");
                $('#booking_request').attr("disabled", false);

                setTimeout(function() {
                    $('#booking_message').html('').removeClass("alert-danger").addClass("hideOnly");
                },10000);
                return;
            }
        }
    });
}


function Pagcerto_Payment_Card(is_credit) {

    let c = ""; // define if it's credit or debit
    if (is_credit === true) {
        c = "c";
    } else {
        c = "d";
    }

    if (ValidateRequiredFields("payment_div_"+c+"card") === false) {
        $('#booking_message').html('Por favor, preencha os campos em vermelho')
            .removeClass("hideOnly").addClass("alert-danger");
        setTimeout(function() {
            $('#booking_message').html('').removeClass("alert-danger").addClass("hideOnly");
            $("#payment_div_"+c+"card :required").each(function () {
                $(this).removeClass('is-invalid');
            });
        },10000);
        return;
    }

    $('#print_boleto').attr("disabled", "disabled");
    $('#send_boleto').attr("disabled", "disabled");
    $('#boleto_send_btn').attr("disabled", "disabled");
    $('#ccard_pay_btn').attr("disabled", "disabled");
    $('#dcard_pay_btn').attr("disabled", "disabled");

    // booking parameters
    let sellingKey = $('#booking_no').val() + "_" + (new Date()).getHours() + (new Date()).getMinutes() + (new Date()).getSeconds();
    let cust_name = $('#cust_name').val();
    let email = $('#cust_email').val();
    let addr_cityCode = $('#cust_city_id').val();
    let addr_district = $('#cust_city_area').val();
    let addr_line1 = $('#cust_street').val();
    let addr_streetNumber = $('#cust_street_no').val();
    let addr_zipCode = $('#cust_postcode').val();
    let taxDocument = $('#cust_doc_no').val();
    let bnks_amount = $('#booking_total_price').val();

    // Card details
    let card_name = $('#'+c+'card_nname').val();
    let card_no = $('#'+c+'card_no').val();
    let card_mm = $('#'+c+'card_mm').val();
    let card_yy = $('#'+c+'card_yy').val();
    let card_cc = $('#'+c+'card_code').val();

    // get and convert date from
    let date_from = ($('#filter_date_from').val()).split("/");
    let date_from_final = date_from[2]+"-"+date_from[1]+"-"+date_from[0];

    // get and convert date to
    if ($('#filter_date_to').val() !== "") {
        let date_from = ($('#filter_date_to').val()).split("/");
        let date_from_final = date_from[2]+"-"+date_from[1]+"-"+date_from[0];
    }

    // get expired date
    let expire_date_obj = new Date();
    expire_date_obj.setDate(expire_date_obj.getDate() + 1);
    let expire_date_day = expire_date_obj.getDate();
    let expire_date_monthIndex = ("0" + (expire_date_obj.getMonth() + 1)).slice(-2);
    let expire_date_year = expire_date_obj.getFullYear();
    let bnks_dueDate = expire_date_year+"-"+expire_date_monthIndex+"-"+expire_date_day;

    let token = $('#pgc_tkn').val();
    $.ajax({
        type: "POST",
        url: "https://payments.paggcerto.com.br/api/v2/pay/cards",
        data: JSON.stringify({
            "amount": bnks_amount,
             "sellingKey": sellingKey,
            "cards": [{
               "holderName": card_name,
               "number": card_no,
               "expirationMonth": card_mm,
               "expirationYear": "20"+card_yy,
               "amountPaid": bnks_amount,
               "installments": 1,
               "securityCode": card_cc,
               "credit": is_credit
            }],
        }),
        headers: {
            "Accept": "application/json",
            "Authorization": "bearer "+token,
            "Content-Type": "application/json"
        },
        success: function (data) {
            //console.log(data);
            let payment_status = data.status;
            if (payment_status === "unauthorized") {
                $('#booking_message').html('Ops, pagamento não autorizado. Por favor, tente novamente ou ' +
                    'entre em contato com a administradora do seu cartão.')
                    .removeClass("hideOnly").addClass("alert-danger");
                $('#ccard_pay_btn').attr("disabled", false);
                return;
            }

            let payment_id = data.id;
            let sellingKey = data.sellingKey;
            //let payment_note = data.note;
            let payment_completedAt = data.completedAt;
            let payment_amount = data.amount;
            let payment_amountPaid = data.amountPaid;
            let ccard_brand = data.cardTransactions[0].cardBrand;
            Create_Invoice(sellingKey, payment_id, c.toUpperCase()+'Card', payment_status,
                ccard_brand, "***"+card_no.substring(parseInt(card_no.length)-4), payment_amount, payment_completedAt.substring(0,10))
        },
        error: function (errorThrown) {
            //console.log(JSON.stringify(errorThrown));
            let json_errors = JSON.parse(errorThrown.responseText)["errors"];
            let html_errors = "<ul>";
            json_errors.forEach(function(item){
                html_errors += "<li>" + item + "</li>";
            });
            html_errors += "</ul>" ;
            $('#booking_message').html('Ops, ocorreram os seguintes erros: <br>'+html_errors)
                .removeClass("hideOnly").addClass("alert-danger");
            $('#'+c+'card_pay_btn').attr("disabled", false);
        }
    });
}

function Booking_Payment_Boleto(print_request) {

    $('#print_boleto').attr("disabled", "disabled");
    $('#send_boleto').attr("disabled", "disabled");
    $('#boleto_send_btn').attr("disabled", "disabled");
    $('#ccard_pay_btn').attr("disabled", "disabled");
    $('#dcard_pay_btn').attr("disabled", "disabled");

    // booking parameters
    let sellingKey = $('#booking_no').val() + "_" + (new Date()).getHours() + (new Date()).getMinutes() + (new Date()).getSeconds();
    let cust_name = $('#cust_name').val();
    let email = $('#cust_email').val();
    let addr_cityCode = $('#cust_city_id').val();
    let addr_district = $('#cust_city_area').val();
    let addr_line1 = $('#cust_street').val();
    let addr_streetNumber = $('#cust_street_no').val();
    let addr_zipCode = $('#cust_postcode').val();
    let taxDocument = $('#cust_doc_no').val();
    let bnks_amount = $('#booking_total_price').val();

    // get and convert date from
    let date_from = ($('#filter_date_from').val()).split("/");
    let date_from_final = date_from[2]+"-"+date_from[1]+"-"+date_from[0];

    // get and convert date to
    if ($('#filter_date_to').val() !== "") {
        let date_from = ($('#filter_date_to').val()).split("/");
        let date_from_final = date_from[2]+"-"+date_from[1]+"-"+date_from[0];
    }

    // get expired date
    let expire_date_obj = new Date();
    expire_date_obj.setDate(expire_date_obj.getDate() + 1);
    let expire_date_day = expire_date_obj.getDate();
    let expire_date_monthIndex = ("0" + (expire_date_obj.getMonth() + 1)).slice(-2);
    let expire_date_year = expire_date_obj.getFullYear();
    let bnks_dueDate = expire_date_year+"-"+expire_date_monthIndex+"-"+expire_date_day;

    //let bnks_acceptedUntil = $('#').val();
    //let addr_line2 = $('#').val();

    let token = $('#pgc_tkn').val();
    $.ajax({
        type: "POST",
        url: "https://payments.paggcerto.com.br/api/v2/pay/bank-slips",
        data: JSON.stringify({
            "payers": [{
               "sellingKey": sellingKey,
               "name": cust_name,
               "email": email,
               "taxDocument": taxDocument,
               "bankSlips": [{
                  "dueDate": bnks_dueDate,
                  "amount": bnks_amount,
                  "secondBankSlip": "",
                  "acceptedUntil": 1,
               }],
               //"requestSplitters": [{
               //   "id": "",
               //   "paysFee": "",
               //   "salesCommission": "",
               //   "amount": ""
               //}]
            }],
        }),
        headers: {
            "Accept": "application/json",
            "Authorization": "bearer "+token,
            "Content-Type": "application/json"
        },
        success: function (data) {
            let payment_id = data.payments[0].id;
            let payment_sellingKey = data.payments[0].sellingKey;
            let payment_note = data.payments[0].note;
            let payment_status = data.payments[0].status;
            let payment_createdAt = data.payments[0].createdAt;
            let payment_amount = data.payments[0].amount;
            let payment_amountPaid = data.payments[0].amountPaid;
            let boleto_id = data.payments[0].bankSlips[0].id;
            let boleto_link = data.payments[0].bankSlips[0].link;
            if (print_request === true) {
                let redirectWindow = window.open(boleto_link, '_blank');
                redirectWindow.location;
            } else {
                Booking_SendBoletoEmail(boleto_id, token);
            }
            Create_Invoice(sellingKey, payment_id+'-'+boleto_id, 'Boleto', payment_status,
                "", "", payment_amount, "")
            //let payment_split_id = data.responseSplitters.id;
            //let payment_split_name = data.responseSplitters.name;
            //let payment_split_paysFee = data.responseSplitters.paysFee;
            //let payment_split_salesCommission = data.responseSplitters.salesCommission;
            //let payment_split_amount = data.responseSplitters.amount;
        },
        error: function (errorThrown) {
            let error = JSON.parse(errorThrown.responseText);
            let str_error = JSON.stringify(error.errors);
            if (str_error.search("taxDocument") > 0) {
                error = "O CPF " + taxDocument + " em seu cadastro nos parece inválido, favor corrigir e tentar novamente.";
            }
            setTimeout(function() {
                $('#booking_message').html("Desculpe, os seguintes erros foram identificados e impediram a reserva de ser realizada: "+error);
                $('#booking_message').removeClass("hideOnly");
                $('#booking_message').addClass("alert-danger");
            },10000);
        }
    });

}

function Booking_SendBoletoEmail(boleto_id, token) {
    let email_addr = $('#boleto_email').val();
    $.ajax({
        type: "POST",
        url: "https://payments.paggcerto.com.br/api/v2/bank-slips/send/single/"+boleto_id,
        data: JSON.stringify({
            "email": email_addr,
        }),
        headers: {
            "Accept": "application/json",
            "Authorization": "bearer "+token,
            "Content-Type": "application/json"
        },
        success: function (data) {
            $('#booking_message').html('Boleto enviado com sucesso para '+email_addr+'.')
                .removeClass("hideOnly").addClass("alert-success");
            return;
        },
        error: function (errorThrown) {
            $('#booking_message').html('Ops, houve um erro no envio do boleto. Por favor, tente novamente ou entre em "Meus Passeios" para imprimir o boleto. Obrigado.')
                .removeClass("hideOnly").addClass("alert-danger");

            setTimeout(function() {
                $('#booking_message').html('').removeClass("alert-danger").addClass("hideOnly");
            },10000);
            return;
        }
    });
}

function Create_Invoice(booking_id, payment_id, payment_method, payment_status, payment_ccard_brand, payment_ccard_no, payment_total, payment_paid_on) {
    booking_id = booking_id.split("_")[0];
    $.ajax({
        url: '../create_invoice',
        data: {
            'booking_id': booking_id,
            'payment_id': payment_id,
            'payment_method': payment_method,
            'payment_status': payment_status,
            'payment_ccard_brand': payment_ccard_brand,
            'payment_ccard_no': payment_ccard_no,
            'payment_total': payment_total,
            'payment_paid_on': payment_paid_on,
        },
        dataType: 'json',
        complete: function (data) {
            let invoice_id = parseInt(data.responseText);
            if (isNaN(invoice_id)) {
                $('#booking_message').html('Ops, houve um erro em sua reserva. A equipe Bnboats já foi ' +
                    'informada e entrará em contato em até 24 horas.')
                    .removeClass("hideOnly").addClass("alert-danger");
            } else {
                $('#booking_message').html('Reserva criada com sucesso, sob o número '+booking_id+'. ' +
                    'Aguarde a confirmação do pagamento e mais informações por email.')
                        .removeClass("hideOnly").removeClass("alert-danger").addClass("alert-success");
            }

        }
    });
}

function Open_SendBoletoDiv() {
    $('#send_boleto_email').removeClass("hideOnly");
    $('#send_boleto').addClass("hideOnly");
}

function SendMessage() {

    let owner_id = $('#boat_owner_pk').val();
    let message_text = $('#captain_chat_text').val();
    $('#send_btn').attr("disabled", "disabled");
    $.ajax({
        url: '../../enviar-mensagem',
        data: {
            'owner_id': owner_id,
            'message_text': message_text,
        },
        dataType: 'json',
        complete: function (data) {
            let msg_id = parseInt(data.responseText);
            $('#captain_chat').find("p").css("display","none");
            $('#captain_chat_text').css("display","none");
            $('#send_btn').css("display","none");

            if (isNaN(msg_id)) {
                $('#message_alert').html('Ops, houve um erro no envio da mensagem. Por favor, tente novamente ou ' +
                    'entre em contato com a gente através de contato@bnboats.com.')
                    .removeClass("hideOnly").addClass("alert-danger");
            } else {
                $('#message_alert').html('Mensagem enviada com sucesso.')
                    .removeClass("hideOnly").removeClass("alert-danger").addClass("alert-success");
            }
            $('#send_btn').attr("disabled", false);
            setTimeout(function () {
                $('#modal_captain_chat').modal('hide');
            },5000)
        }
    });
}

function BookShortcutOnMobile() {
    $('html,body').animate({
        scrollTop: $(".bview_right_div").offset().top
    }, 'slow');
}