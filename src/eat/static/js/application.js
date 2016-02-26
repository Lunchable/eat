$('form').submit(
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