let quantities = {};
let doneSeenAt = {}; // tracks when we first noticed each item was "done", by id
const API_BASE = `${window.location.protocol}//${window.location.hostname}:8000`;
const AUTO_REMOVE_MS = 30000; // 30 seconds

async function loadMenu() {
  const response = await fetch(`${API_BASE}/menu-items`);
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
    card.className = "menu-card";

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
    sendBtn.className = "send-btn";
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
  await fetch(`${API_BASE}/items`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: name, qty: qty }),
  });

  loadSentItems();
}

async function removeItem(id) {
  await fetch(`${API_BASE}/items/${id}`, {
    method: "DELETE",
  });
  delete doneSeenAt[id];
  loadSentItems();
}

async function loadSentItems() {
  const response = await fetch(`${API_BASE}/items`);
  const items = await response.json();

  const pendingItems = items.filter((item) => item.status === "pending");
  const doneItems = items.filter((item) => item.status === "done");

  checkAutoRemove(doneItems);
  renderPendingItems(pendingItems);
  renderDoneItems(doneItems);
}

function checkAutoRemove(doneItems) {
  const now = Date.now();

  doneItems.forEach((item) => {
    if (!(item.id in doneSeenAt)) {
      doneSeenAt[item.id] = now; // first time we've seen this one as done
    }
  });

  doneItems.forEach((item) => {
    const elapsed = now - doneSeenAt[item.id];
    if (elapsed >= AUTO_REMOVE_MS) {
      removeItem(item.id);
    }
  });
}

function renderPendingItems(items) {
  const pendingDiv = document.getElementById("pending-list");
  pendingDiv.innerHTML = "";

  items.forEach((item) => {
    const row = document.createElement("div");
    row.className = "sent-row";
    row.textContent = `${item.qty}x ${item.name}`;
    pendingDiv.appendChild(row);
  });
}

function renderDoneItems(items) {
  const doneDiv = document.getElementById("done-list");
  doneDiv.innerHTML = "";

  items.forEach((item) => {
    const row = document.createElement("div");
    row.className = "sent-row done";

    const label = document.createElement("span");
    label.textContent = `${item.qty}x ${item.name}`;

    const removeBtn = document.createElement("button");
    removeBtn.textContent = "Remove";
    removeBtn.className = "remove-btn";
    removeBtn.addEventListener("click", () => {
      removeItem(item.id);
    });

    row.appendChild(label);
    row.appendChild(removeBtn);
    doneDiv.appendChild(row);
  });
}

loadMenu();
loadSentItems();
setInterval(loadSentItems, 3000);