document.addEventListener("DOMContentLoaded", function () {
    fetchUserDashboard();
});

function fetchUserDashboard() {
    fetch("/dashboard-data")
        .then(response => response.json())
        .then(data => {
            document.getElementById("username").innerText = data.username;
            document.getElementById("balance").innerText = `$${data.balance}`;
            
            populateTransactionHistory(data.transactions);
            populateInvestmentData(data.investments);
        })
        .catch(error => console.error("Error loading dashboard data:", error));
}

function populateTransactionHistory(transactions) {
    let transactionList = document.getElementById("transaction-history");
    transactionList.innerHTML = "";
    transactions.forEach(tx => {
        let row = `<tr>
                      <td>${tx.date}</td>
                      <td>${tx.type}</td>
                      <td>$${tx.amount}</td>
                  </tr>`;
        transactionList.innerHTML += row;
    });
}

function populateInvestmentData(investments) {
    let investmentList = document.getElementById("investment-data");
    investmentList.innerHTML = "";
    investments.forEach(inv => {
        let row = `<tr>
                      <td>${inv.stock_name}</td>
                      <td>${inv.shares}</td>
                      <td>$${inv.amount}</td>
                      <td>${inv.status}</td>
                  </tr>`;
        investmentList.innerHTML += row;
    });
}

function addTransaction() {
    let amount = document.getElementById("transaction-amount").value;
    let type = document.getElementById("transaction-type").value;
    
    fetch("/track-transaction", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ amount: amount, transaction_type: type })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchUserDashboard();
    })
    .catch(error => console.error("Error adding transaction:", error));
}
