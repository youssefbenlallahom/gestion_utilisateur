// Sidebar Toggle
function openSidebar() {
    document.getElementById("sidebar").style.display = "block";
}

function closeSidebar() {
    document.getElementById("sidebar").style.display = "none";
}

// Profile Dropdown Toggle
function toggleProfileDropdown() {
    const dropdown = document.getElementById("profileDropdown");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

function viewProfile() {
    window.location.href = "/profile-url";
}

function logout() {
    window.location.href = "/logout-url";
}

window.onclick = function (event) {
    const dropdown = document.getElementById("profileDropdown");
    if (!event.target.matches(".profile-icon") && dropdown.style.display === "block") {
        dropdown.style.display = "none";
    }
};

// Initial section display
document.addEventListener("DOMContentLoaded", () => {
    showSection("coaches-section");
});

function showSection(sectionId) {
    document.querySelectorAll(".management-section").forEach((section) => {
        section.style.display = "none";
    });
    document.getElementById(sectionId).style.display = "block";
}
