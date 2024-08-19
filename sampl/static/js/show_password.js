document.addEventListener('DOMContentLoaded', (event) => {
    const showPasswordCheckbox = document.getElementById('show_password');
    const passwordField = document.getElementById('password');

    showPasswordCheckbox.addEventListener('change', function() {
        const type = this.checked ? 'text' : 'password';
        passwordField.type = type;
    });
});
