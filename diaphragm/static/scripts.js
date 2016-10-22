function switchNavigation() {
    switchElement("navigation", "open", "closed");
    switchElement("cover", "visible", "hidden");
}

function switchElement(cls, firstState, secondState) {
    applyToAll(cls, function(elem) {
        elem.className = exchangeSubstring(elem.className,
            firstState, secondState);
    });
}

function applyToAll(selector, func) {
    let elements = document.getElementsByClassName(selector);
    for (let element of elements)
        func(element);
}

function exchangeSubstring(str, substrA, substrB) {
    if (str.includes(substrA))
        return str.replace(substrA, substrB);
    else if (str.includes(substrB))
        return str.replace(substrB, substrA);
    return str;
}
