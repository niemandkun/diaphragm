window.onload = function() {
    ref(document.location.pathname);
}

window.onpopstate = function(e) {
    ref(document.location.pathname, true);
}

function raiseReload() {
    var evt = document.createEvent('CustomEvent');
    evt.initEvent("ajax_reload", true, true);
    document.dispatchEvent(evt);
}

function findParent(tagname,el){
    tagname = tagname.toLowerCase()

    if ((el.nodeName || el.tagName).toLowerCase() === tagname) {
        return el;
    }
    while (el = el.parentNode){
        if ((el.nodeName || el.tagName).toLowerCase() === tagname) {
            return el;
        }
    }
    return null;
}

window.onclick = function(ev) {
    var target = findParent('a', ev.target || ev.srcElement);

    if (target && !target.download && ev.button == 0) {
        if (target.hash) {
            pushHistory(document.title, target.href);
            jump(target.hash.substr(1));
            stop(ev);
            return false;
        }
        if (target.host == document.location.host) {
            stop(ev);
            ref(target.pathname);
            return false;
        }
    }
    return true;
}

function jump(id) {
    var element = document.getElementById(id);

    if (element) {
        var top = element.offsetTop;
        window.scrollTo(0, top - 100);
    }
}

function stop(event) {
    if (event.preventDefault)
        event.preventDefault();
    if (event.stopPropagation)
        event.stopPropagation();

    event.returnValue = false;
    return event;
}

function ref(url, notPushHistory) {
    hideNavigation();
    showSpinner();

    get("/api" + url, function(response) {

        if (!notPushHistory)
            pushHistory(response.title, url);

        hideSpinner();
        updateContent(response.title, response.content);
        raiseReload();
    });
}

function get(url, callback) {
    request("GET", url, null, callback);
}

function post(url, data, callback) {
    request("POST", url, data, callback);
}

function request(method, url, data, callback) {
    var httpRequest = new XMLHttpRequest();
    httpRequest.abort();
    httpRequest.onreadystatechange = handleResponse(callback, httpRequest);
    httpRequest.open(method, url, true);

    if (data) {
        httpRequest.send(data);
    } else {
        httpRequest.send();
    }
}

function handleResponse(callback, httpRequest) {
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

function getById(selector) {
    if (document.getElementById)
        return document.getElementById(selector);
    else if (document.querySelectorAll)
        return document.querySelectorAll("#" + selector)[0];
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

document.addEventListener('ajax_reload', function(event) {
    images = [];

    var thumbnails = getByClassName("preview");

    for (var i = 0; i < thumbnails.length; ++i) {
        var image = thumbnails[i];
        images.push(image.src.replace("/thumbnails", ""));
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
    doShowImage(event.target.src.replace("/thumbnails", ""),
        document.location.pathname);
}

function doShowImage(imageSrc, path) {
    var imageFull = resetImageFull();
    var imageName = basepath(imageSrc);

    imageFull.src = "";
    imageFull.src = imageSrc;
    imageFull.alt = imageName;
    imageFull.onclick = hideImage;

    pushHistory(document.title, path + "/" + imageName);
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
    pushHistory(document.title, dirpath(document.location.pathname));
    setElement("show", "visible", "hidden");
}

function dirpath(path) {
    return path.replace("/"+basepath(path), '');
}

function basepath(path) {
    return path.replace(/^.*[\\\/]/, '');
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
        doShowImage(images[nextImage], dirpath(document.location.pathname));
        stop(event);
        return false;
    }

    if (event.key === "ArrowLeft" || event.key.toLowerCase() === "a") {
        var nextImage = currentImage() - 1;

        if (nextImage === -1)
            nextImage += images.length;

        doShowImage(images[nextImage], dirpath(document.location.pathname));
        stop(event);
        return false;
    }

    if (event.key === "F1") {
        switchElement("help", "hidden", "visible");
        stop(event);
        return false;
    }
});

function startThread(event) {
    var message = getById("message");

    if (!message.value) {
        showFormError("Message should contain text.");
        stop(event);
        return false;
    }

    if (message.value.length > 5000) {
        showFormError("Message is too large. Limit is 5000 characters.");
        stop(event);
        return false;
    }

    if (getById("subject").value.length > 80) {
        showFormError("Subject is too large. Limit is 80 characters.");
        stop(event);
        return false;
    }

    if (getById("author").value.length > 80) {
        showFormError("Author name is too large. Limit is 80 characters.");
        stop(event);
        return false;
    }

    var file = getById("fileupload").files[0];

    if (file && file.size > 8 * 1024 * 1024) {
        showFormError("Attachment is too large. Limit is 8 Mb.");
        stop(event);
        return false;
    }

    var data = new FormData(getById("postform"));

    post("/api/start_thread", data, function(r) {
        if (r.thread_id)
            ref("/board/thread/" + r.thread_id);
    });

    stop(event);
    return false;
}

function postMessage(event) {
    var message = getById("message");

    if (!message.value) {
        showFormError("Message should contain text.");
        stop(event);
        return false;
    }

    if (message.value.length > 5000) {
        showFormError("Message is too large. Limit is 5000 characters.");
        stop(event);
        return false;
    }

    if (getById("author").value.length > 80) {
        showFormError("Author name is too large. Limit is 80 characters.");
        stop(event);
        return false;
    }

    var file = getById("fileupload").files[0];

    if (file && file.size > 8 * 1024 * 1024) {
        showFormError("Attachment is too large. Limit is 8 Mb.");
        stop(event);
        return false;
    }

    var data = new FormData(getById("postform"));
    var thread = getById("thread").value;

    post("/api/post_message", data, function(r) {
        ref("/board/thread/"+ thread);
    });

    stop(event);
    return false;
}

function showFormError(msg) {
    var error = getById("formerror");
    error.innerHTML = msg;
}

function insertMessage(str) {
    var message = getById("message");

    if (message) {
        message.value += ">>" + str;
    }
}

autoupdateLastId = null;
autoupdateHandler = null;

document.addEventListener('ajax_reload', function() { resetLastAutoupdateId(); });

function resetLastAutoupdateId() {
    var autoupdateTargets = getByClassName("autoupdate_target");

    autoupdateLastId = null;

    if (autoupdateTargets.length == 0) {
        if (autoupdateHandler) {
            clearInterval(autoupdateHandler);
            autoupdateHandler = null;
        }
        return;
    }

    for (var i = 0; i < autoupdateTargets.length; ++i) {
        var id = parseInt(autoupdateTargets[i].id);

        if (id > autoupdateLastId)
            autoupdateLastId = id;
    }

    if (!autoupdateHandler)
        autoupdateHandler = setInterval(function() { autoUpdate(); }, 5000);
}

function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function htmlToDomElements(html) {
    var template = document.createElement('template');
    template.innerHTML = html;
    return template.content.childNodes;
}

function autoUpdate() {
    var thread = thread = getById("thread").value;

    get("/ajaxapi/board/thread/" + thread + "/new/" + autoupdateLastId, function (r) {

        var nodes = htmlToDomElements(r.content);

        var lastElement = getById(autoupdateLastId);

        var _nodes = [];

        for (var i = 0; i < nodes.length; ++i) {
            _nodes.push(nodes[i]);
        }

        for (var i = 0; i < _nodes.length; ++i) {

            if (!_nodes[i].className || _nodes[i].className.indexOf("autoupdate_target") == -1)
                continue;

            insertAfter(_nodes[i], lastElement);
            lastElement = _nodes[i];
        }

        resetLastAutoupdateId();
    });
}

function doLike(event, postId) {
    post("/ajaxapi/board/like/" + postId, "", function(r) {
        event.target.innerHTML = r.count;
    });
}

function doDislike(event, postId) {
    post("/ajaxapi/board/dislike/" + postId, "", function(r) {
        event.target.innerHTML = r.count;
    });
}

function updateLikes(event, postId) {
    get("/ajaxapi/board/likes/" + postId, function(r) {
        getById("likes" + postId).innerHTML = r.likes_count;
        getById("dislikes" + postId).innerHTML = r.dislikes_count;
    });
}
