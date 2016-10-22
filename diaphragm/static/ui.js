function switchNavigation() {
    switchElement("navigation", "open", "closed");
    switchElement("cover", "visible", "hidden");
}

function hideNavigation() {
    setElement("navigation", "open", "closed");
    setElement("cover", "visible", "hidden");
}

function setElement(cls, oldState, newState) {
    applyToAll(cls, function(elem) {
        elem.className = elem.className.replace(oldState,
            newState);
    });
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
