function switchNavigation() {
    switchElement("navigation", "open", "closed");
    switchElement("cover", "visible", "hidden");
}

function hideNavigation() {
    setElement("navigation", "open", "closed");
    setElement("cover", "visible", "hidden");
}

function getByClassName(selector) {
    if (document.getElementsByClassName)
        return document.getElementsByClassName(selector);
    else if (document.querySelectorAll)
        return document.querySelectorAll("." + selector);
    else
        return null;
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
    var elements = getByClassName(selector);
    for (var i = 0; i < elements.length; ++i)
        func(elements[i]);
}

function exchangeSubstring(str, substrA, substrB) {
    if (str.indexOf(substrA) >= 0)
        return str.replace(substrA, substrB);
    else if (str.indexOf(substrB) >= 0)
        return str.replace(substrB, substrA);
    return str;
}
