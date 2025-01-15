
function toggleNav() {
    var nav = document.querySelector('nav');
    nav.classList.toggle('active');  // Toggle the 'active' class to show/hide the nav
}


document.getElementById('submit-order').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'order_confirmation_page.html';  // Change URL as needed
});

