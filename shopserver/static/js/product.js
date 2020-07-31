let products = document.getElementById("product_list").value;
products = JSON.parse(products);
const list_element = document.getElementById('list');
const pagination_element = document.getElementById('pagination');

let current_page = 1
rows = 5;

function Display_list(items, wrapper, rows_per_page,page){
    wrapper.innerHTML = "";
    page--;

    let start = rows_per_page * page;
    let end = start+rows_per_page;
    let paginatedItems = items.slice(start, start+rows_per_page);

    for(let i = 0; i< paginatedItems.length; i++){
        let item = items[i];

        let item_element = document.createElement ('div');
        item_element.classList.add('item');
        item_element.innerText = item.fields.name;
        wrapper.appendChild(item_element);
    }
}
Display_list(products,list_element, rows, 1);
console.log(products[0])