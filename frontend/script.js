const API = "http://127.0.0.1:8000";

let products = [];

/* ===============================
   LOAD PURCHASE ORDERS DASHBOARD
================================ */

async function loadPurchaseOrders() {

    const res = await fetch(`${API}/purchase-orders`);
    const orders = await res.json();

    const vendorRes = await fetch(`${API}/vendors`);
    const vendors = await vendorRes.json();

    const vendorMap = {};
    vendors.forEach(v => vendorMap[v.id] = v.name);

    const table = document.getElementById("poTable");

    if (!table) return;

    table.innerHTML = "";

    orders.forEach(po => {

        const row = `
        <tr>
            <td>${po.reference_no}</td>
            <td>${vendorMap[po.vendor_id]}</td>
            <td>$${po.total_amount}</td>
            <td>${po.status}</td>
        </tr>
        `;

        table.innerHTML += row;
    });

}

/* ===============================
   LOAD VENDORS DROPDOWN
================================ */

async function loadVendors() {

    const res = await fetch(`${API}/vendors`);
    const vendors = await res.json();

    const select = document.getElementById("vendorSelect");

    if (!select) return;

    vendors.forEach(v => {

        const option = document.createElement("option");

        option.value = v.id;
        option.textContent = v.name;

        select.appendChild(option);

    });

}

/* ===============================
   LOAD PRODUCTS
================================ */

async function loadProducts() {

    const res = await fetch(`${API}/products`);
    products = await res.json();

}

/* ===============================
   ADD PRODUCT ROW
================================ */

function addRow() {

    const table = document.getElementById("productRows");

    const row = document.createElement("tr");

    let options = "";

    products.forEach(p => {
        options += `<option value="${p.id}" data-price="${p.unit_price}">
        ${p.name}
        </option>`;
    });

    row.innerHTML = `
    <td>
        <select class="form-control productSelect">
            ${options}
        </select>
    </td>

    <td>
        <input type="number" class="form-control qty" value="1">
    </td>

    <td>
        <input type="text" class="form-control price" readonly>
    </td>
    `;

    table.appendChild(row);

    updatePrice(row);

}

/* ===============================
   UPDATE PRODUCT PRICE
================================ */

function updatePrice(row) {

    const select = row.querySelector(".productSelect");
    const priceInput = row.querySelector(".price");

    const price = select.options[select.selectedIndex].dataset.price;
    priceInput.value = price;

    select.addEventListener("change", () => {

        const newPrice = select.options[select.selectedIndex].dataset.price;
        priceInput.value = newPrice;

    });

}

/* ===============================
   CREATE PURCHASE ORDER
================================ */

async function submitPO() {

    const vendorId = document.getElementById("vendorSelect").value;

    const rows = document.querySelectorAll("#productRows tr");

    const items = [];

    rows.forEach(row => {

        const productId = row.querySelector(".productSelect").value;
        const qty = row.querySelector(".qty").value;
        const price = row.querySelector(".price").value;

        items.push({
            product_id: parseInt(productId),
            quantity: parseInt(qty),
            price: parseFloat(price)
        });

    });

    const body = {
        vendor_id: parseInt(vendorId),
        items: items
    };

    const res = await fetch(`${API}/purchase-orders`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    if (res.ok) {
        alert("Purchase Order Created Successfully");
        window.location.href = "index.html";
    }

}

/* ===============================
   AI AUTO DESCRIPTION (Fallback)
================================ */

function generateDescription() {

    const name = document.getElementById("productName").value;
    const category = document.getElementById("category").value;

    const text =
        `${name} is a high-quality product designed for the ${category} category, offering reliable performance and excellent value. Built with modern technology, it provides efficiency, durability, and convenience for everyday use.`;

    document.getElementById("description").value = text;

}

/* ===============================
   INITIALIZE PAGE
================================ */

document.addEventListener("DOMContentLoaded", () => {

    loadPurchaseOrders();
    loadVendors();
    loadProducts();

});
