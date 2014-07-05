$(document).ready(function(){

    $('.btn-popover').popover({html:true});

    $('.btn-popover').on('click', function (e) {
        $('.btn-popover').not(this).popover('hide');
    });


});