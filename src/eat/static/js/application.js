$('#applicant_form').submit(
    function (e) {
        e.preventDefault();
        var data = $(this).serializeArray().reduce(function (obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});
        var url = this.action;
        var method = this.method;
        var f = function(s){
            console.log(s);
        }
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
        var f = function(s){
            console.log(s);
        }
        $(this).find('input,select').removeClass('form_error');
        $('span.form_error_message').remove();
        $.ajax({
            type: method,
            url: url,
            data: data,
            success: function(income){
                console.log("Created income", income);
                var incomes_list = $(this.form).closest('section').find('.incomes_list');

                var new_income =    $('<div id="' + income._id +'" class="income_item row"></div>')
                                    .append($('<span class="col-1">').text('Source: '))
                                    .append($('<span class="col-2">').text(income.source))
                                    .append($('<span class="col-1">').text('Amount: '))
                                    .append($('<span class="col-2">').text('$' + income.amount))
                                    .append($('<span class="col-1">').text('Frequency: '))
                                    .append($('<span class="col-2">').text(income.frequency))
                                    .append($('<span class="col-3">').html('<a href="/svc/eat/v1/application/applicant/incomes/' + income._id + '" target="_applicant_income_delete">Delete this income</a>'))
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