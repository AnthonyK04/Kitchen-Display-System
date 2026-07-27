let quantities = {};

async function loadMenu() {
  const response = await fetch("http://localhost:8000/menu-items");
  const menuItems = await response.json();
  renderMenu(menuItems);
}

function renderMenu(menuItems) {
  const menuDiv = document.getElementById("menu-list");
  menuDiv.innerHTML = "";

  menuItems.forEach((item) => {
    if (!(item.id in quantities)) {
      quantities[item.id] = 1;
    }

    const card = document.createElement("div");

    const nameLabel = document.createElement("span");
    nameLabel.textContent = item.name;

    const minusBtn = document.createElement("button");
    minusBtn.textContent = "-";
    minusBtn.addEventListener("click", () => {
      if (quantities[item.id] > 1) {
        quantities[item.id]--;
        qtyInput.value = quantities[item.id];
      }
    });

    const qtyInput = document.createElement("input");
    qtyInput.type = "number";
    qtyInput.value = quantities[item.id];
    qtyInput.addEventListener("change", () => {
      quantities[item.id] = parseInt(qtyInput.value, 10) || 1;
    });

    const plusBtn = document.createElement("button");
    plusBtn.textContent = "+";
    plusBtn.addEventListener("click", () => {
      quantities[item.id]++;
      qtyInput.value = quantities[item.id];
    });

    const sendBtn = document.createElement("button");
    sendBtn.textContent = "Send";
    sendBtn.addEventListener("click", () => {
      sendOrder(item.name, quantities[item.id]);
    });

    card.appendChild(nameLabel);
    card.appendChild(minusBtn);
    card.appendChild(qtyInput);
    card.appendChild(plusBtn);
    card.appendChild(sendBtn);
    menuDiv.appendChild(card);
  });
}

async function sendOrder(name, qty) {
  await fetch("http://localhost:8000/items", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: name, qty: qty }),
  });

  loadSentItems();
}

async function loadSentItems() {
  const response = await fetch("http://localhost:8000/items");
  const items = await response.json();
  renderSentItems(items);
}

function renderSentItems(items) {
  const sentDiv = document.getElementById("sent-list");
  sentDiv.innerHTML = "";

  items.forEach((item) => {
    const row = document.createElement("div");
    row.textContent = `${item.qty}x ${item.name} — ${item.status}`;
    sentDiv.appendChild(row);
  });
}

loadMenu();
loadSentItems();
setInterval(loadSentItems, 3000);