httpRequest = new XMLHttpRequest();

window.onload = function() {
    ref(document.location.pathname);
}

window.onpopstate = function(e) {
    ref(document.location.pathname, history=false);
}

function ref(url, history=true) {
    request("/api" + url, function(response) {
        updateContent(response.title, response.content);
        if (history) pushHistoty(response.title, url);
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
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
                response = JSON.parse(httpRequest.responseText);
            } else {
                response = createError(httpRequest.status);
            }

            callback(response);
            hideSpinner();
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

function pushHistoty(title, url) {
    history.pushState(null, title, url);
}

function updateContent(title, contentText) {
    content = document.getElementsByClassName("content")[0];
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
