var parser = new DOMParser;

const animation_time = 1000;

function showProject(e) {
    pop_up_window = document.createElement("div");
    pop_up_window.id = "pop-up_window";
    // pop_up_window.style.opacity = 0;
    
    pop_up_message = parser.parseFromString(httpGet("../project/" + e), "text/html").getElementById("window_message");
    pop_up_window.append(pop_up_message);
    
    document.body.insertAdjacentElement("afterEnd", pop_up_window);
    
    document.body.style.overflow = 'hidden';
    document.body.classList.toggle('unblured', false);
    document.body.classList.toggle('blured', true);
    
    pop_up_window.classList.toggle('appeared', true);
    pop_up_window.classList.toggle('disappeared', false);
};

function closeProject() {
    pop_up_window = document.getElementById("pop-up_window");
    
    document.body.classList.toggle('blured', false);
    document.body.classList.toggle('unblured', true);
    pop_up_window.classList.toggle('appeared', false);
    pop_up_window.classList.toggle('disappeared', true);
    
    setTimeout(function(){
        document.body.classList.toggle('unblured', false);
        pop_up_window.classList.toggle('disappeared', false);
        pop_up_window.remove();
        document.body.style.overflow = 'visible';
    }, animation_time);
};

function httpGet(e) {
    var t = new XMLHttpRequest;
    return t.open("GET", e, !1), t.send(null), t.responseText
};