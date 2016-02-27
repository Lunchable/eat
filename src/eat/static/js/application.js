var labelMap = {
    wages: 'Wages',
    tips: 'Tips',
    daily: 'Daily',
    weekly: 'Weekly',
    biweekly: 'Every Two Weeks',
    semimonthly: 'Twice a Month',
    monthly: 'Monthly',
    annually: 'Annually',
    first_name: 'First Name',
    middle_initial: 'Middle Initial',
    last_name: 'Last Name',
    school_name: 'School Name',
    school_city: 'School City',
    school_state: 'School State',
    school_postal: 'School Zip Code'
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
                $(this.form).find('input').val('');
                var incomes_list = $(this.form).closest('.income_container').find('.incomes_list');

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

$('a.child_delete').click(
    function (e) {
        e.preventDefault();
        var url = this.href;
        var method = 'DELETE';
        $.ajax({
            type: method,
            url: url,
            success: function(child){
                console.log("Deleted child", child);
                disappear(this.li);
            },
            error: function(err){
                console.log(err);
            },
            dataType: 'json',
            li: $(this).closest('li')
        });
    }
);

function children_form_handler(e) {
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
        success: function(child){
            console.log("Created child", child);
            if(! ($(this.form).attr('child_id'))){ // we're adding a new child
                $(this.form).find('input').val('');
                var children_list = $(this.form).closest('section').find('.children_list');
                var new_child =     $('<li>').attr('id', child._id).addClass('income_container')
                //<h3><span><a href="/svc/eat/v1/application/children/{{ child._id }}" class="child_delete glyphicon glyphicon-remove-sign"></a></span></h3>
                                    .append($('<h3>')
                                        .append( $('<span>')
                                            .append($('<a>').attr('href', '/svc/eat/v1/application/children/' + child._id).addClass('child_delete glyphicon glyphicon-remove-sign'))
                                        )
                                    )
                                    .append($('<form>').attr('child_id', child._id).attr('action', action="/svc/eat/v1/application/children/" + child._id).addClass('children_form')
                                        .append($('<div>').html('<label for="first_name">' + labelLookup('first_name') + '</label>: <input id="first_name" name="first_name" type="text" value="' + child.first_name+ '">'))
                                        .append($('<div>').html('<label for="middle_initial">' + labelLookup('middle_initial') + '</label>: <input id="middle_initial" name="middle_initial" type="text" value="' + (child.middle_initial || '') + '">'))
                                        .append($('<div>').html('<label for="last_name">' + labelLookup('last_name') + '</label>: <input id="last_name" name="last_name" type="text" value="' + child.last_name + '">'))
                                        .append($('<div>').html('<label for="school_city">' + labelLookup('school_city') + '</label>: <input id="school_city" name="school_city" type="text" value="' + child.school_city + '">'))
                                        .append($('<div>').html('<label for="school_state">' + labelLookup('school_state') + '</label>: <input id="school_state" name="school_state" type="text" value="' + child.school_state + '">'))
                                        .append($('<div>').html('<label for="school_postal">' + labelLookup('school_postal') + '</label>: <input id="school_postal" name="school_postal" type="text" value="' + child.school_postal + '">'))
                                        .append($('<div>').html('<label for="school_name">' + labelLookup('school_name') + '</label>: <input id="school_name" name="school_name" type="text" value="' + child.school_name + '">'))
                                        .append($('<button>').attr('type', 'submit').text('Update'))
                                    );

                $(children_list).append(new_child);
                //be sure to bind this handler function now to newly created forms
                $('.children_form').submit(children_form_handler);
            }

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

$('.children_form').submit(children_form_handler);
