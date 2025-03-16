document.addEventListener("DOMContentLoaded", function() {
    fetch("/get-rewards")
        .then(response => response.json())
        .then(data => {
            document.getElementById("rewardPoints").textContent = `${data.reward_points} Points`;
        })
        .catch(error => console.error("Error fetching rewards:", error));
});
