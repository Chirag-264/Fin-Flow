document.addEventListener("DOMContentLoaded", function() {
    console.log("Fin-Flow loaded!"); // Debugging

    // Logout Button Click Handler
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function() {
            fetch("/logout", { method: "POST" })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = "/login";
                    }
                })
                .catch(error => console.error("Error logging out:", error));
        });
    }
});
