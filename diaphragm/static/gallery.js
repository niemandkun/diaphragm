var images = [];

//function ensureGalleryInitialized() {
document.addEventListener('dynload', function(event) {
    if (images.length > 0) return;

    var thumbnails = getByClassName("thumbnail");

    for (var i = 0; i < thumbnails.length; ++i) {
        var image = thumbnails[i].getElementsByTagName("IMG")[0];
        images.push(image.src);
    }
}, false);

function currentImage() {
    var imageFull = getByClassName("image-full")[0];
    return images.indexOf(imageFull.src);
}


function showImage(event) {
    var imageFull = getByClassName("image-full")[0];
    imageFull.src = event.target.src;
    var path = imageFull.src.replace("/static", "");
    pushHistory(document.title, path);
    setElement("show", "hidden", "visible");
}

function hideImage(event) {
    if (event.target !== event.currentTarget)
    {
        stop(event);
        return false;
    }
    pushHistory(document.title, "/gallery");

    setElement("show", "visible", "hidden");
}

window.onhelp = function(ev) {
    switchElement("help", "hidden", "visible");
    stop(ev);
    return false;
}

window.addEventListener("keydown", function(event) {
    var imageFull = getByClassName("image-full")[0];

    var showVisible = getByClassName("show-visible").length > 0;

    stop(event);

    if (!showVisible)
        return false;

    if (event.key === "Escape" || event.key === "Esc") {
        setElement("show", "visible", "hidden");
        pushHistory(document.title, "/gallery");
    }

    if (event.key === "ArrowRight" || event.key.toLowerCase() === "d") {
        imageFull.src = images[(currentImage() + 1) % images.length];
        var path = imageFull.src.replace("/static", "");
        pushHistory(document.title, path);
    }

    if (event.key === "ArrowLeft" || event.key.toLowerCase() === "a") {
        var nextImage = currentImage() - 1;
        if (nextImage === -1)
            nextImage += images.length;

        imageFull.src = images[nextImage];
        var path = imageFull.src.replace("/static", "");
        pushHistory(document.title, path);
    }

    if (event.key === "F1") {
        switchElement("help", "hidden", "visible");
    }

    return false;
});
