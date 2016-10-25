$(document).ready(function() {
    $('#email_address_title').editable(function(value, settings) {
        var revert = this.revert;
        return function(value, settings, elem) {
            var data = {
                title: value,
            };
            $.ajax({
                type: "POST",
                async: false,
                url: update_email_address_title,
                data: data,
                success: function(data) {
                    if (!data.success) {
                        value = revert;
                        $('#email_address_title_error').text(data.message);
                    }
                }
            });
            return value;
        }(value, settings, this);
        },
        {
            type: 'textarea',
            height: "50px",
            width: "400px",
            tooltip: "",
            cancel: "Cancel",
            submit: "Ok",
    });
    

    var localDialogs = {

    };

    $.each(localDialogs, function(id,opt) { stdDialog(id, opt); });
    populate_id(email_address_id, 'EmailAddress');
    details_copy_id('EmailAddress');
    toggle_favorite('EmailAddress');
}); //document.ready

