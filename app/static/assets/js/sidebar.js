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
