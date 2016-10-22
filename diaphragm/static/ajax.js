httpRequest = new XMLHttpRequest();

function ref(url) {
    hideNavigation();
    showSpinner();
    httpRequest.abort();
    httpRequest.onreadystatechange = handleResponse;
    httpRequest.open('GET', url);
    httpRequest.send();
}

function handleResponse() {
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
        if (httpRequest.status === 200) {
            updateContent(httpRequest.responseText);
        } else if (httpRequest.status !== 0) {
            updateContent("<div class='error'>Error " + httpRequest.status + " :(</div>");
        }

        hideSpinner();
    }
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

function updateContent(responseText) {
    content = document.getElementsByClassName("content")[0];
    content.innerHTML = responseText;
}
