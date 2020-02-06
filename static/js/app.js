$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

$card = $('.card');

$card.on('hidden.bs.collapse', function () {
    const element = get_fa(this);
    element.setAttribute('class', 'fas fa-plus-circle');
});

$card.on('shown.bs.collapse', function () {
    const element = get_fa(this);
    element.setAttribute('class', 'fas fa-minus-circle');
});

function get_fa(context) {
    return context.getElementsByClassName('card-header')[0].getElementsByClassName('btn')[0].getElementsByClassName('d-flex')[0].getElementsByClassName('mb-0')[0].getElementsByClassName('fas')[0];
}