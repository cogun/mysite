$(document).ready(function () {
    AOS.init();
});
$(".nav-open").click(function (e) {
    e.preventDefault();
    $(".nav").toggleClass("hidden")
});

$('.close-toast').click(function (e) { 
    e.preventDefault();
    $(this).parent().fadeOut()
});