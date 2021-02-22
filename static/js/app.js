window.addEventListener("load", function () {
    // Toggles tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
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