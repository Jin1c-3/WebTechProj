const form = document.querySelector('.needs-validation')
const username = document.querySelector('#username')
const password = document.querySelector('#pwd')
const usernameInvalid = document.querySelector('.username-invalid')
const passwordInvalid = document.querySelector('.pwd-invalid')

function checkUsername() {
    if (username.value.length < 4) {
        username.setCustomValidity('Username must be at least 4 characters long')
        usernameInvalid.innerHTML = 'Username must be at least 4 characters long'
        return false
    } else {
        username.setCustomValidity('')
        return true
    }
}

function checkPassword() {
    if (password.value.length < 3 || password.value.length > 18) {
        password.setCustomValidity('Password must be at least 8 characters long')
        passwordInvalid.innerHTML = 'Password must be at least 8 characters long'
        return false
    } else {
        password.setCustomValidity('')
        return true
    }
}

form.addEventListener('submit', (event) => {
    let count = 0
    count += checkUsername() ? 1 : 0
    count += checkPassword() ? 1 : 0
    if (count < 2) {
        event.preventDefault()
        event.stopPropagation()
    }
    form.classList.add('was-validated')
})
