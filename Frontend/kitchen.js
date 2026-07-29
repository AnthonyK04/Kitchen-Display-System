let currentItems = [];
let selectedIndex = 0;
const API_BASE = `${window.location.protocol}//${window.location.hostname}:8000`;
function renderItems(items) {
  const listDiv = document.getElementById("item-list");
  listDiv.innerHTML = "";
  if(items.length === 0){
    listDiv.textContent = "No Special Orders Currently!";
    return;
  }

  items.forEach((item, index) => {
    const row = document.createElement("div");
    row.className = "item-row";
    if(index === selectedIndex) {
        row.className += " selected";
        }
    row.textContent = `${item.qty}x ${item.name}`;
    listDiv.appendChild(row);
  });
}

async function loadItems() {
  const response = await fetch(`${API_BASE}/items/pending`

  );
  const items = await response.json();
  currentItems = items;

  if (selectedIndex > currentItems.length - 1) {
    selectedIndex = currentItems.length - 1;
  }
  if (selectedIndex < 0) {
    selectedIndex = 0;
  }

  renderItems(currentItems);
}

async function markSelectedDone() {
  if (currentItems.length === 0) return;

  const selectedItem = currentItems[selectedIndex];
  await fetch(`${API_BASE}/items/${selectedItem.id}/done`, {
    method: "PATCH",
  });

  loadItems();
}

document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowDown") {
    if (selectedIndex < currentItems.length - 1) {
      selectedIndex++;
    }
    renderItems(currentItems);
  }
  if (e.key === "ArrowUp") {
    if (selectedIndex > 0) {
      selectedIndex--;
    }
    renderItems(currentItems);
  }
  if (e.key === "Enter") {
    markSelectedDone();
  }
});

loadItems();
setInterval(loadItems, 3000);