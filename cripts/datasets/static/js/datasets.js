$(document).ready(function() {
    $('#dataset_title').editable(function(value, settings) {
        var revert = this.revert;
        return function(value, settings, elem) {
            var data = {
                title: value,
            };
            $.ajax({
                type: "POST",
                async: false,
                url: update_dataset_title,
                data: data,
                success: function(data) {
                    if (!data.success) {
                        value = revert;
                        $('#dataset_title_error').text(data.message);
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
    populate_id(dataset_id, 'Dataset');
    details_copy_id('Dataset');
    toggle_favorite('Dataset');
}); //document.ready

