const API = "http://127.0.0.1:8000";

let products = [];

async function loadPurchaseOrders() {

const res = await fetch(`${API}/purchase-orders`);
const data = await res.json();

const table = document.getElementById("poTable");

table.innerHTML = "";

data.forEach(po => {

const row = `
<tr>
<td>${po.reference_no}</td>
<td>${po.vendor_id}</td>
<td>$${po.total_amount}</td>
<td>${po.status}</td>
</tr>
`;

table.innerHTML += row;

});

}


async function loadVendors(){

const res = await fetch(`${API}/vendors`);
const vendors = await res.json();

const select = document.getElementById("vendorSelect");

vendors.forEach(v => {

const option = document.createElement("option");

option.value = v.id;
option.text = v.name;

select.appendChild(option);

});

}


async function loadProducts(){

const res = await fetch(`${API}/products`);
products = await res.json();

}


function addRow(){

const tbody = document.querySelector("#productTable tbody");

const row = document.createElement("tr");

let options = "";

products.forEach(p => {

options += `<option value="${p.id}" data-price="${p.unit_price}">
${p.name}
</option>`

})

row.innerHTML = `
<td>
<select class="form-select productSelect">
${options}
</select>
</td>

<td>
<input type="number" class="form-control quantity" value="1">
</td>

<td>
<input type="text" class="form-control price" readonly>
</td>
`;

tbody.appendChild(row);

updatePrice(row);

row.querySelector(".productSelect")
.addEventListener("change", () => updatePrice(row));

}


function updatePrice(row){

const select = row.querySelector(".productSelect");

const price = select.options[select.selectedIndex].dataset.price;

row.querySelector(".price").value = price;

}

async function generateDescription(){

const name = document.getElementById("productName").value;
const category = document.getElementById("category").value;

const prompt = `Write a professional 2 sentence marketing description for a product called ${name} in the ${category} category`;

const response = await fetch("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyBrnAuRzToVx1qPxiXczQqwWbmlIMRQ8uI",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({

contents:[{
parts:[{text: prompt}]
}]

})

});

const data = await response.json();

const text = data.candidates[0].content.parts[0].text;

document.getElementById("description").value = text;

}


async function submitPO(){

const vendor = document.getElementById("vendorSelect").value;

const rows = document.querySelectorAll("#productTable tbody tr");

let items = [];

rows.forEach(r => {

const product_id = r.querySelector(".productSelect").value;

const quantity = r.querySelector(".quantity").value;

items.push({
product_id: parseInt(product_id),
quantity: parseInt(quantity)
})

})

const body = {

vendor_id: parseInt(vendor),
items: items

};

await fetch(`${API}/purchase-orders`,{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify(body)

})

alert("Purchase Order Created");

window.location = "index.html";

}
