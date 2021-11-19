function set_colorpicker(id_input, id_real_input){
    $(function () {
  $(id_input).colorpicker({format: 'hex', extensions: 'palette'});

  $(id_input).on('colorpickerChange', function(event) {
    $(id_input).css('background-color', event.color.toString());
    $(id_input).css('color', event.color.toString());
    $(id_real_input).val(event.color.toString());
  });
});
}

$( ".color_picker" ).each(
    function() 
    {
        set_colorpicker('#'+($(this).attr('id')),'#real-'+$(this).attr('id'));
    }
);

// Обработчик изменения кол-ва цветов
function setColorsAmount(n){
    
    range_inputs = document.getElementsByClassName('color_amount_range');
    
    for (i = 0; i < range_inputs.length; i++)
    {
        range_inputs[i].value = n;
    }

    elements = document.getElementsByClassName('color_amount_indicator');
    for (i = 0; i < elements.length; i++)
    {
        elements[i].textContent = 
        elements[i].textContent.replace(elements[i].textContent.split(':')[1],' ' + n);
    }
    
    button_elements = document.getElementsByClassName('change_colors_button');
    for (i = 0; i < button_elements.length; i++)
    {
        button_elements[i].disabled = false; 
        button_elements[i].classList.remove('disabled');
        button_elements[i].href = "/projects/color_combinations?color_amount=" + n + "&mode=" + i;
        button_elements[i].classList.add("pulse", "animated", "infinite");  
    }
    
    button_element_1 = document.getElementById('confirm_color_button');
    button_element_1.disabled = true; 
    
    button_element_1 = document.getElementById('predict_color_button');
    button_element_1.disabled = true;
}

// Капча
function onSubmit(token) {
 document.getElementById("demo-form").submit();
}

function show_recaptcha() {
    grecaptcha.render('recaptcha', {
        'sitekey' : '6Lc8_o4bAAAAANoPxmoIfPXylWMjMgHqipDR9nzZ',
        'callback' : close_captcha
    });
    document.getElementById('recaptcha').style.visibility = 'visible';
};

function close_captcha(response){

    setTimeout(function() {
        document.getElementById('recaptcha').style.visibility = 'hidden';
    }, 1000);
    
    
    button_element = document.getElementById('confirm_color_button');
    button_element.setAttribute('type','submit');
    // Языковой пакет нужен
    button_element.textContent = _("Отправить");
    button_element.removeAttribute('onclick');
    button_element.classList.add("pulse", "animated", "infinite");
    
    $('#color-input').colorpicker('colorpicker').disable();
};

$(document).ready(function() {
    
    button_element = document.getElementById("predict_color_button");
    if(prediction_enabled == "True")
    {
        button_element.disabled = false; 
        button_element.classList.remove('disabled');
    }
    else
    {
        button_element.disabled = true; 
        button_element.classList.add('disabled');
    }
    
    /*
    var makesquare = function()
    {
    $('.makesquare').each(
        function()
        {
            var thisso = $(this);
            var thiswidth = thisso.width();
            
            //alert(thiswidth);
            
            thisso.css('height', thiswidth);
            thisso.css('min-height', thiswidth);
            thisso.css('width', thiswidth);
        }
    );
    };
    
    makesquare();
    
    $(window).resize(function () {
    makesquare();
    });
    */
    
    /*
    var set_actual_mode = function()
    {
        if (localStorage['mode'])
            $('#main-carousel').carousel(Number(localStorage['mode']));   
        else
            localStorage['mode'] = 0;
    };
    set_actual_mode();
    
    $('#main-carousel').on('slid.bs.carousel', function (event) {
        localStorage['mode'] = event.to;
    })
    */

});