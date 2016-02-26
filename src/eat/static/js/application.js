var labelMap = {
    wages: 'Wages',
    tips: 'Tips',
    daily: 'Daily',
    weekly: 'Weekly',
    biweekly: 'Every Two Weeks',
    semimonthly: 'Twice a Month',
    monthly: 'Monthly',
    annually: 'Annually'
}

function labelLookup(value){
    return labelMap[value] || value;
}

$('#applicant_form').submit(
    function (e) {
        e.preventDefault();
        var data = $(this).serializeArray().reduce(function (obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});
        var url = this.action;
        var method = this.method;
        $(this).find('input').removeClass('form_error');
        $('span.form_error_message').remove();
        $.ajax({
            type: method,
            url: url,
            data: data,
            success: function(s){
                console.log(s);
            },
            error: function(err){
                if(err.status==400){
                    for(var i in err.responseJSON.errors) {
                        var inputField = $(this.form).find('input[name=' + i + ']');
                        inputField.addClass('form_error');
                        inputField.after('<span class="form_error_message">' + err.responseJSON.errors[i][0] + "</span>");
                    }
                }
            },
            dataType: 'json',
            form: this
        });
    }
);

$('.incomes_form').submit(
    function (e) {
        e.preventDefault();
        var data = $(this).serializeArray().reduce(function (obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});
        var url = this.action;
        var method = this.method;
        $(this).find('input,select').removeClass('form_error');
        $('span.form_error_message').remove();
        $.ajax({
            type: method,
            url: url,
            data: data,
            success: function(income){
                console.log("Created income", income);
                var incomes_list = $(this.form).closest('section').find('.incomes_list');

                var new_income =    $('<div>').attr('id', income._id).addClass('income_item row')
                                    .append($('<span>').addClass('col-1').text('Source: '))
                                    .append($('<span>').addClass('col-2').text(labelLookup(income.source)))
                                    .append($('<span>').addClass('col-1').text('Amount: '))
                                    .append($('<span>').addClass('col-2').text('$' + income.amount))
                                    .append($('<span>').addClass('col-1').text('Frequency: '))
                                    .append($('<span>').addClass('col-2').text(labelLookup(income.frequency)))
                                    .append($('<span>').addClass('col-3').html('<a href="/svc/eat/v1/application/applicant/incomes/' + income._id + '" class="income_delete glyphicon glyphicon-remove-sign"></a>'))
                                    .append($('<br>'));
                $(incomes_list).append(new_income);

            },
            error: function(err){
                if(err.status==400){
                    for(var i in err.responseJSON.errors) {
                        var inputField = $(this.form).find('input[name=' + i + ']');
                        inputField.addClass('form_error');
                        inputField.after('<span class="form_error_message">' + err.responseJSON.errors[i][0] + "</span>");
                    }
                }
            },
            dataType: 'json',
            form: this
        });
    }
);

function disappear(element) {
    $(element).fadeOut(300, function() { 
        $(this).remove(); 
       });

}

$('a.income_delete').click(
    function (e) {
        e.preventDefault();
        var url = this.href;
        var method = 'DELETE';
        $.ajax({
            type: method,
            url: url,
            success: function(income){
                console.log("Deleted income", income);
                disappear(this.row);
            },
            error: function(err){
                console.log(err);
            },
            dataType: 'json',
            row: $(this).closest('.row')
        });
    }
);
