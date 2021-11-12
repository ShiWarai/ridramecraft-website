var parser = new DOMParser();

function showProject(name){
    pop_up_window = document.createElement('div');
    pop_up_window.id = "pop-up_window";
    pop_up_window.style['opacity'] = 0;
    

    pop_up_message = parser.parseFromString(httpGet("../project/" + name), "text/html").getElementById('window_message');
    pop_up_window.append(pop_up_message);
    
    document.body.insertAdjacentElement("afterEnd", pop_up_window);
    
    
    counter = 0;
    timer = setInterval(function() {
        if (counter > 10) {
            clearInterval(timer);
            return;
        }
        else
        {
            document.body.style['filter'] = "blur(" + String(counter) + "px)";
            pop_up_window.style['opacity'] = counter / 10;
            counter+=0.5;
        }
    }, 20);
};

function closeProject(){
    pop_up_window = document.getElementById('pop-up_window');
    
    counter = 10;
    timer = setInterval(function() {
        if (counter < 0) {
            clearInterval(timer);
            pop_up_window.remove();
            document.body.style['filter'] = "";
            return;
        }
        else
        {
            document.body.style['filter'] = "blur(" + String(counter) + "px)";
            pop_up_window.style['opacity'] = counter / 10;
            counter-=0.5;
        }
    }, 20);
};

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
};