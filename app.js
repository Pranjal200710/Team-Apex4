const transactions = [
  { id: "TXN-842195", date: "12 Aug 2026", from: "HDFC Bank •••• 4921", source: "UPI payment", to: "Green Valley Hospital", target: "Bengaluru", purpose: "Cardiology consultation", amount: "₹1,250.00", status: "paid", description: "Payment for a consultation with Dr. Rohan Kapoor in the Cardiology department." },
  { id: "TXN-841703", date: "06 Aug 2026", from: "ICICI Bank •••• 2108", source: "Net banking", to: "Green Valley Hospital", target: "Bengaluru", purpose: "Diagnostic tests", amount: "₹3,600.00", status: "paid", description: "Payment for diagnostic tests including blood panel and ECG." },
  { id: "TXN-839624", date: "29 Jul 2026", from: "HDFC Bank •••• 4921", source: "UPI payment", to: "Care Pharmacy", target: "Bengaluru", purpose: "Prescription medicines", amount: "₹825.00", status: "paid", description: "Payment for prescribed medication following your consultation." },
  { id: "TXN-838512", date: "22 Jul 2026", from: "HealthFirst Insurance", source: "Insurance claim", to: "Green Valley Hospital", target: "Bengaluru", purpose: "Insurance settlement", amount: "₹5,400.00", status: "paid", description: "Insurance claim settlement paid directly to your hospital provider." },
  { id: "TXN-836901", date: "15 Jul 2026", from: "HDFC Bank •••• 4921", source: "UPI payment", to: "Green Valley Hospital", target: "Bengaluru", purpose: "Annual health check-up", amount: "₹2,200.00", status: "paid", description: "Payment for your annual preventive health screening." },
  { id: "TXN-843210", date: "18 Aug 2026", from: "HDFC Bank •••• 4921", source: "Scheduled payment", to: "Green Valley Hospital", target: "Bengaluru", purpose: "Follow-up consultation", amount: "₹4,850.00", status: "pending", description: "Scheduled payment for your upcoming specialist follow-up consultation." }
];

const body = document.querySelector("#transactionBody");
const dialog = document.querySelector("#purposeDialog");
let activeFilter = "all";

function renderTransactions() {
  const query = document.querySelector("#searchInput").value.trim().toLowerCase();
  const visible = transactions.filter(t => (activeFilter === "all" || t.status === activeFilter) && Object.values(t).join(" ").toLowerCase().includes(query));
  body.innerHTML = visible.map(t => `<tr><td class="transaction-id">${t.id}</td><td class="date">${t.date}</td><td class="from">${t.from}<small>${t.source}</small></td><td class="to">${t.to}<small>${t.target}</small></td><td><button class="purpose-link" data-id="${t.id}">${t.purpose}</button></td><td class="amount ${t.status === "pending" ? "" : "negative"}">${t.amount}</td><td><span class="status ${t.status}">${t.status === "paid" ? "Paid" : "Pending"}</span></td></tr>`).join("") || `<tr><td colspan="7" style="text-align:center;padding:32px;color:#7b8b85">No transactions match your search.</td></tr>`;
  document.querySelector("#tableCount").textContent = `Showing ${visible.length ? "1–" + visible.length : "0"} of ${visible.length} transaction${visible.length === 1 ? "" : "s"}`;
}

document.querySelector("#searchInput").addEventListener("input", renderTransactions);
document.querySelectorAll(".filter").forEach(button => button.addEventListener("click", () => { activeFilter = button.dataset.filter; document.querySelectorAll(".filter").forEach(b => b.classList.toggle("active", b === button)); renderTransactions(); }));
body.addEventListener("click", event => { const button = event.target.closest(".purpose-link"); if (!button) return; const transaction = transactions.find(t => t.id === button.dataset.id); document.querySelector("#dialogTitle").textContent = transaction.purpose; document.querySelector("#dialogDescription").textContent = transaction.description; document.querySelector("#dialogDetails").innerHTML = `<span>Transaction ID <b>${transaction.id}</b></span><span>Payment to <b>${transaction.to}</b></span><span>Amount <b>${transaction.amount}</b></span>`; dialog.showModal(); });
document.querySelectorAll(".close-dialog, .close-primary").forEach(button => button.addEventListener("click", () => dialog.close()));
const toast = document.querySelector("#toast");
function showToast(message) { toast.textContent = message; toast.classList.add("show"); window.setTimeout(() => toast.classList.remove("show"), 3000); }
document.querySelector("#makePayment").addEventListener("click", () => showToast("Secure payment flow would open here."));
document.querySelector("#payDue").addEventListener("click", () => showToast("Your ₹4,850 payment is ready to review."));
document.querySelector("#downloadBtn").addEventListener("click", () => { const text = ["Transaction ID,Date,Made From,Made To,Purpose,Amount,Status", ...transactions.map(t => [t.id,t.date,t.from,t.to,t.purpose,t.amount,t.status].join(","))].join("\n"); const link = document.createElement("a"); link.href = URL.createObjectURL(new Blob([text], {type:"text/csv"})); link.download = "medicare-payment-statement.csv"; link.click(); URL.revokeObjectURL(link.href); showToast("Payment statement downloaded."); });
renderTransactions();
