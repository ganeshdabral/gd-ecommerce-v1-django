$('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});

$('.same_as_shipping').click(function(){

    billing_prifix = 'billing';
    shipping_prifix = 'shipping';
    alert($('.same_as_shipping').val())
    if($('.same_as_shipping_label').hasClass('active')) {
        $('.same_as_shipping').val('on')
        $('#id_'+billing_prifix+'-firstname').attr('value',$('#id_'+shipping_prifix+'-firstname').val());
        $('#id_'+billing_prifix+'-lastname').attr('value',$('#id_'+shipping_prifix+'-lastname').val());
        $('#id_'+billing_prifix+'-address_line_1').attr('value',$('#id_'+shipping_prifix+'-address_line_1').val());
        $('#id_'+billing_prifix+'-address_line_2').attr('value',$('#id_'+shipping_prifix+'-address_line_2').val());

        $('#id_'+billing_prifix+'-city').attr('value',$('#id_'+shipping_prifix+'-city').val());
        $('#id_'+billing_prifix+'-state').attr('value',$('#id_'+shipping_prifix+'-state').val());
        $('#id_'+billing_prifix+'-postal_code').attr('value',$('#id_'+shipping_prifix+'-postal_code').val());
        $('#id_'+billing_prifix+'-phone').attr('value',$('#id_'+shipping_prifix+'-phone').val());
    }
    else {
        $('.same_as_shipping').val('off')
        $('#id_'+billing_prifix+'-firstname').attr('value','');
        $('#id_'+billing_prifix+'-lastname').attr('value','');
        $('#id_'+billing_prifix+'-address_line_1').attr('value','');
        $('#id_'+billing_prifix+'-address_line_2').attr('value','');

        $('#id_'+billing_prifix+'-city').attr('value','');
        $('#id_'+billing_prifix+'-state').attr('value','');
        $('#id_'+billing_prifix+'-postal_code').attr('value','');
        $('#id_'+billing_prifix+'-phone').attr('value','');
    }
});
