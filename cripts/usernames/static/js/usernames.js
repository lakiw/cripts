$(document).ready(function() {
    $('#username_title').editable(function(value, settings) {
        var revert = this.revert;
        return function(value, settings, elem) {
            var data = {
                title: value,
            };
            $.ajax({
                type: "POST",
                async: false,
                url: update_username_title,
                data: data,
                success: function(data) {
                    if (!data.success) {
                        value = revert;
                        $('#username_title_error').text(data.message);
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
    populate_id(username_id, 'UserName');
    details_copy_id('UserName');
    toggle_favorite('UserName');
}); //document.ready

