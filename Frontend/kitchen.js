let currentItems = [];
let selectedIndex = 0;

function renderItems(items) {
  const listDiv = document.getElementById("item-list");
  listDiv.innerHTML = "";

  items.forEach((item, index) => {
    const row = document.createElement("div");
    row.textContent = `${item.qty}x ${item.name}`;
    if (index === selectedIndex) {
      row.style.backgroundColor = "yellow";
    }
    listDiv.appendChild(row);
  });
}

async function loadItems() {
  const response = await fetch("http://localhost:8000/items/pending");
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
  await fetch(`http://localhost:8000/items/${selectedItem.id}/done`, {
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