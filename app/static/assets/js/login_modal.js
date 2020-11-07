function toggleModal() {
    var modal = document.getElementById('loginModal');
    var loginButton = document.getElementById('loginButton');
    const rootElement = document.documentElement;
    modal.classList.toggle('is-active');
    loginButton.classList.toggle('is-active');
    rootElement.classList.toggle('is-clipped');
};