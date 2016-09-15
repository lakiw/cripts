$(document).ready(function() {
    $(document).keyup(function(e) {
        var tag = e.target.tagName.toLowerCase();
        if (tag != 'input' && tag != 'textarea' && tag != 'select' && !e.ctrlKey) {
            if (e.keyCode==78 || e.keyCode==77) {
                $('.nav-menu-icon').trigger('click');
            } else if (e.keyCode==65) {
                $('.search-menu-icon').trigger('click');
            } else if (e.keyCode==69 && e.shiftKey) {
                $( "#new-event" ).click();
            } else if (e.keyCode==27) {
                $( ".mm-opened").trigger('close');
            } else if (e.shiftKey && e.keyCode==191) {
                $( "#shortcut-keys").click();
            }
        }
    });
});

