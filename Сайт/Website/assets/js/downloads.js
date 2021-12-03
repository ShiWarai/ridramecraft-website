const on_page = 10;
var list;
var selector_template, row_template;

function search(value){
    response = get_lists();
    list = response['list'];
    
    searched_list = [];
    for(let i = 0; i < list.length; i++)
        if((list[i]['name'] + list[i]['extension']).includes(value))
            searched_list.push(list[i]);
    
    list = searched_list;
    
    load_lists_selectors(Math.ceil(list.length/on_page));
    load_list(1);
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false);
    xmlHttp.send(null); // Пустой запрос на get
    return JSON.parse(xmlHttp.responseText);
}

function get_lists(){
    response = httpGet('/downloads/list');
    
    return {'count': response['count'], 'list': response['list']};
}

function load_templates(){
    selectors_div = document.getElementById('page_selectors');
    table_body = document.getElementById('downloads_table').lastElementChild;

    // Получение шаблона
    selector_template = selectors_div.firstElementChild.cloneNode(true);
    selectors_div.firstElementChild.remove();
    
    // Получение шаблона
    row_template = table_body.firstElementChild.cloneNode(true);
    // row_template.setAttribute('style','display: default');
    table_body.firstElementChild.remove();
}

function load_list(n){
    
    list_on_page = list.slice((n-1)*on_page, n*on_page);
    
    table_body = document.getElementById('downloads_table').lastElementChild;
    
    // Отчистка таблицы
    while (table_body.firstChild) {
        table_body.removeChild(table_body.firstChild);
    }
    
    for(let i = 0; i < list_on_page.length; i++)
    {
        let object = list_on_page[i];
        name = object['name'];
        link = object['link'];
        extension = object['extension'];
        description = object['description'];
        
        let row = row_template.cloneNode(true);
        let elements = row.children;
        let name_element = elements[0];
        let fullname_element = elements[1];
        let extension_element = elements[2];
        let description_element = elements[3];
        
        row.setAttribute('onclick', "location.href=\"/downloads/" + link + "\";");
        name_element.textContent = name;
        fullname_element.textContent = name + extension;
        extension_element.textContent = extension;
        description_element.textContent = description;
        
        table_body.appendChild(row);
    }
}

function load_lists_selectors(lists_n)
{
    while (selectors_div.firstChild) {
        selectors_div.removeChild(selectors_div.firstChild);
    }
    for(let i = 1; i <= lists_n; i++)
    {
        let selector = selector_template.cloneNode(true);
        let span = selector.firstElementChild;

        span.textContent = String(i);
        selector.setAttribute('onclick', 'load_list('+String(i)+')');

        selectors_div.appendChild(selector);
    }
}

load_templates();
// информации о доступных загрузках
response = get_lists();
var list = response['list'];
lists_n = Math.ceil(response['count']/on_page);

load_lists_selectors(lists_n);
if(lists_n || false)
    load_list(1);