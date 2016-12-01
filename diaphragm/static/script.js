var httpRequest = new XMLHttpRequest();

window.onload = function() {
    ref(document.location.pathname);
}

window.onpopstate = function(e) {
    request("/api" + document.location.pathname, function(response) {
        updateContent(response.title, response.content);
    });
}

function findParent(tagname,el){
  if ((el.nodeName || el.tagName).toLowerCase()===tagname.toLowerCase()){
    return el;
  }
  while (el = el.parentNode){
    if ((el.nodeName || el.tagName).toLowerCase()===tagname.toLowerCase()){
      return el;
    }
  }
  return null;
}

window.onclick = function(ev) {

    var target = findParent('a', ev.target || ev.srcElement)

    if (target && ev.button == 0) {
        if (target.host == document.location.host) {
            stop(ev);
            ref(target.pathname);
            return false;
        }
    }

    return true;
}

function stop(event) {
    if (event.preventDefault)
        event.preventDefault();
    if (event.stopPropagation)
        event.stopPropagation();

    event.returnValue = false;
    return event;
}

function ref(url) {
    request("/api" + url, function(response) {
        updateContent(response.title, response.content);
        pushHistory(response.title, url);
    });
}

function request(url, callback) {
    hideNavigation();
    showSpinner();
    httpRequest.abort();
    httpRequest.onreadystatechange = handleResponse(callback);
    httpRequest.open('GET', url);
    httpRequest.send();
}

function handleResponse(callback) {
    return function() {

        var done = 4;

        if (httpRequest.readyState === done) {
            if (httpRequest.status === 0) {
                return;
            }

            if (httpRequest.status === 200) {
                response = JSON.parse(httpRequest.responseText);
            } else {
                response = createError(httpRequest.status);
            }

            callback(response);
            hideSpinner();

            var evt = document.createEvent('CustomEvent');
            evt.initEvent("dynload", true, true);
            document.dispatchEvent(evt);
        }
    }
}

function createError(errorNumber) {
    var error = Object();

    error.title = "Error " + errorNumber+ " | nl";
    error.content = "<div class=error>Oops...<br/>An error "
              + errorNumber
              + " occured :(</div>"

    return error;
}

function pushHistory(title, url) {
    if (history.pushState)
        history.pushState(null, title, url);
}

function updateContent(title, contentText) {
    content = getByClassName("content")[0];
    content.innerHTML = contentText;
    document.title = title;
}

function show(cls) {
    applyToAll(cls, function(e) { e.style.display = "flex"; });
}

function hide(cls) {
    applyToAll(cls, function(e) { e.style.display = "none"; });
}

function showSpinner() {
    hide("content"); show("spinner");
}

function hideSpinner() {
    hide("spinner"); show("content");
}

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

var images = [];
var preload = null;

function updatePreload() {
   var current = currentImage();
   var nextImage = (current + 1) % images.length;
   preload = new Image();
   preload.src = images[nextImage];
}

document.addEventListener('dynload', function(event) {
    if (images.length > 0) return;

    var thumbnails = getByClassName("thumbnail");

    for (var i = 0; i < thumbnails.length; ++i) {
        var image = thumbnails[i].getElementsByTagName("IMG")[0];
        images.push(image.src.replace("thumbnails", "gallery"));
    }
}, false);

function currentImage() {
    var imageFull = getByClassName("image-full")[0];
    return images.indexOf(imageFull.src);
}

function removeImageFull() {
    var imageFull = getByClassName("image-full");
    var popup = getByClassName("popup")[0];

    for (var i = 0; i < imageFull.length; ++i) {
        popup.removeChild(imageFull[i]);
    }
}

function resetImageFull() {
    removeImageFull();

    var popup = getByClassName("popup")[0];
    var imageFull = document.createElement("IMG");
    imageFull.className = "image-full";
    popup.appendChild(imageFull);

    return imageFull;
}

function showImage(event) {
    var imageFull = resetImageFull();
    imageFull.src = "";
    imageFull.src = event.target.src.replace("thumbnails", "gallery");
    var path = imageFull.src.replace("/static", "");
    pushHistory(document.title, path);
    setElement("show", "hidden", "visible");
    updatePreload();
}

function hideImage(event) {
    if (event.target !== event.currentTarget)
    {
        stop(event);
        return false;
    }
    removeImageFull();
    pushHistory(document.title, "/gallery");
    setElement("show", "visible", "hidden");
}

window.onhelp = function(ev) {
    switchElement("help", "hidden", "visible");
    stop(ev);
    return false;
}

window.addEventListener("keydown", function(event) {
    var showVisible = getByClassName("show-visible").length > 0;

    if (!showVisible)
        return;

    if (event.key === "Escape" || event.key === "Esc") {
        setElement("show", "visible", "hidden");
        pushHistory(document.title, "/gallery");
        stop(event);
        return false;
    }

    if (event.key === "ArrowRight" || event.key.toLowerCase() === "d") {
        var nextImage = (currentImage() + 1) % images.length;
        var imageFull = resetImageFull();
        imageFull.src = images[nextImage];
        var path = imageFull.src.replace("/static", "");
        pushHistory(document.title, path);
        updatePreload();
        stop(event);
        return false;
    }

    if (event.key === "ArrowLeft" || event.key.toLowerCase() === "a") {
        var nextImage = currentImage() - 1;

        if (nextImage === -1)
            nextImage += images.length;

        var imageFull = resetImageFull();
        imageFull.src = images[nextImage];
        var path = imageFull.src.replace("/static", "");
        pushHistory(document.title, path);
        stop(event);
        return false;
    }

    if (event.key === "F1") {
        switchElement("help", "hidden", "visible");
        stop(event);
        return false;
    }
});
