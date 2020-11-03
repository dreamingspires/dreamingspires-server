// Register collapsible components
const collapsibles = document.getElementsByClassName('is-collapsible');
for (var i=0; i<collapsibles.length; ++i) {
    new bulmaCollapsible(collapsibles[i]);
};

// Collapse on hover functionality
function mouseover_expand(elem) {
    const c = elem.querySelector('.is-collapsible');
    c.bulmaCollapsible('expand');
};

function mouseover_collapse(elem) {
    const c = elem.querySelector('.is-collapsible');
    c.bulmaCollapsible('collapse');
};

function ToggleExpand(elem) {
    const c = elem.closest('.collapsible-wrapper').querySelector('.is-collapsible');
    if (c.bulmaCollapsible('collapsed')) {
        c.bulmaCollapsible('expand');
        elem.classList.add('fa-chevron-up');
        elem.classList.remove('fa-chevron-down');
    }
    else {
        c.bulmaCollapsible('collapse');
        elem.classList.add('fa-chevron-down');
        elem.classList.remove('fa-chevron-up');
    }
}