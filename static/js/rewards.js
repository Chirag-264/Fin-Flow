document.addEventListener("DOMContentLoaded", function () {
    fetchRewards();
});

function fetchRewards() {
    fetch("/rewards")
        .then(response => response.json())
        .then(data => {
            displayRewards(data.rewards);
        })
        .catch(error => console.error("Error fetching rewards:", error));
}

function displayRewards(rewards) {
    const rewardsContainer = document.getElementById("rewards-list");
    rewardsContainer.innerHTML = "";

    rewards.forEach(reward => {
        const rewardItem = document.createElement("div");
        rewardItem.classList.add("reward-item");
        rewardItem.innerHTML = `
            <h3>${reward.title}</h3>
            <p>${reward.description}</p>
            <span>Points Required: ${reward.points_required}</span>
            <button onclick="redeemReward(${reward.id})">Redeem</button>
        `;
        rewardsContainer.appendChild(rewardItem);
    });
}

function redeemReward(rewardId) {
    fetch("/redeem-reward", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ reward_id: rewardId })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchRewards(); // Refresh the reward list after redeeming
    })
    .catch(error => console.error("Error redeeming reward:", error));
}
