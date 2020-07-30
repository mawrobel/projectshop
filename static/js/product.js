let products = document.getElementById("product_list").value;
products = JSON.parse(products);
const list_element = document.getElementById('list');
const pagination_element = document.getElementById('pagination');
let current_page = 1
rows = 1600;

function Display_list(items, wrapper, rows_per_page,page){
    //wrapper.innerHTML = "";
    page--;

    let start = rows_per_page * page;
    let end = start+rows_per_page
    let paginatedItems = items.slice(start, start+rows_per_page);

    for(let i = start; i< paginatedItems.length; i++){
        console.log(items[i]);
    }
}
Display_list(products,list_element, rows, 1);