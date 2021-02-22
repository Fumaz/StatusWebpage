window.addEventListener("load", function () {
    // Enables tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});

// Gets all cards
$card = $('.card');

// On hide
$card.on('hidden.bs.collapse', function () {
    const element = get_fa(this);
    element.setAttribute('class', 'fas fa-plus-circle');
});

// On show
$card.on('shown.bs.collapse', function () {
    const element = get_fa(this);
    element.setAttribute('class', 'fas fa-minus-circle');
});

// Gets the fontawesome element from the context
function get_fa(context) {
    return context.getElementsByClassName('card-header')[0].getElementsByClassName('btn')[0].getElementsByClassName('d-flex')[0].getElementsByClassName('mb-0')[0].getElementsByClassName('fas')[0];
}