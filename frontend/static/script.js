const form = document.getElementById("expense-form");
const list = document.getElementById("expense-list");
const dateInput = document.getElementById("date");
const statsTable = document.getElementById("stats-table").querySelector("tbody");

const today = new Date().toISOString().split("T")[0];
dateInput.value = today;

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const amount = document.getElementById("amount").value;
  const category = document.getElementById("category").value;
  const date = dateInput.value;

  const res = await fetch("http://localhost:5000/expenses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount, category, date }),
  });

  if (res.ok) {
    form.reset();
    dateInput.value = today;
    loadExpenses();
    loadStats();
  }
});

async function deleteExpense(id) {
  const res = await fetch(`http://localhost:5000/expenses/${id}`, {
    method: "DELETE",
  });
  if (res.ok) {
    loadExpenses();
    loadStats();
  }
}

async function loadExpenses() {
  const res = await fetch("http://localhost:5000/expenses");
  const data = await res.json();

  list.innerHTML = "";
  let total = 0;

  data.forEach((exp) => {
    const item = document.createElement("li");
    let dateStr = exp.date;
    let date = dateStr.split("T")[0];
    let time = dateStr.includes("T") ? dateStr.split("T")[1].split(".")[0] : "--:--";

    item.innerHTML = `
      <div><strong>💵 Amount:</strong> ${exp.amount} den</div>
      <div><strong>🏷️ Category:</strong> ${exp.category}</div>
      <div><strong>📅 Date:</strong> ${date}</div>
      <div><strong>⏰ Time:</strong> ${time}</div>
      <button onclick="deleteExpense('${exp.id}')">🗑️ Delete</button>
    `;
    list.appendChild(item);
    total += Number(exp.amount);
  });

  const totalItem = document.createElement("li");
  totalItem.style.fontWeight = "bold";
  totalItem.style.backgroundColor = "#e6ffe6";
  totalItem.innerHTML = `🔢 Total Expenses: ${total} den`;
  list.appendChild(totalItem);
}

async function loadStats() {
  const res = await fetch("http://localhost:5000/stats");
  const data = await res.json();

  statsTable.innerHTML = "";
  data.forEach((stat) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${stat.month}</td>
      <td>${stat.category}</td>
      <td>${stat.average}</td>
    `;
    statsTable.appendChild(row);
  });
}

loadExpenses();
loadStats();
