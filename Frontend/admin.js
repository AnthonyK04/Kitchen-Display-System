const API_BASE = `${window.location.protocol}//${window.location.hostname}:8000`;

async function loadMenu() {
  const response = await fetch(`${API_BASE}/menu-items`);
  const menuItems = await response.json();
  renderMenu(menuItems);
}

function renderMenu(menuItems) {
  const listDiv = document.getElementById("menu-admin-list");
  listDiv.innerHTML = "";

  menuItems.forEach((item) => {
    const row = document.createElement("div");
    row.className = "menu-admin-row";

    const label = document.createElement("span");
    label.textContent = item.name;

    const removeBtn = document.createElement("button");
    removeBtn.textContent = "Remove";
    removeBtn.addEventListener("click", () => {
      removeMenuItem(item.id);
    });

    row.appendChild(label);
    row.appendChild(removeBtn);
    listDiv.appendChild(row);
  });
}

async function addMenuItem() {
  const input = document.getElementById("new-item-name");
  const name = input.value.trim();

  if (!name) return;

  await fetch(`${API_BASE}/menu-items`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: name }),
  });

  input.value = "";
  loadMenu();
}

async function removeMenuItem(id) {
  await fetch(`${API_BASE}/menu-items/${id}`, {
    method: "DELETE",
  });

  loadMenu();
}

document.getElementById("add-btn").addEventListener("click", addMenuItem);

loadMenu();