$.fn.stars = function() {
    return $(this).each(function() {
        // Get the value
        var val = parseFloat($(this).html());
        // Make sure that the value is in 0 - 5 range, multiply to get width
        var size = Math.max(0, (Math.min(5, val))) * 16;
        // Create stars holder
        var $span = $('<span />').width(size);
        // Replace the numerical value with stars
        $(this).html($span);
    });
}

$(document).ready(function(){
    $('span.stars').stars();
    right_bar_height = $('.right_bar').height();
    left_bar_width = $('.left_bar').width();
    window_width = $(document).width();
    $('.left_bar').height(right_bar_height);
    $('.right_bar').width(window_width- left_bar_width-30);
    $('.left_bar p').css('margin-top',right_bar_height/2 -40)
})