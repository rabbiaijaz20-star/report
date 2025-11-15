// -----------------------------------------------
//  Basic Frontend Enhancements
// -----------------------------------------------

// Button click message
function showMessage() {
    alert("Action performed successfully!");
}

// Auto date in footer
document.addEventListener("DOMContentLoaded", () => {
    const footer = document.getElementById("footer-year");
    if (footer) {
        footer.textContent = new Date().getFullYear();
    }
});
