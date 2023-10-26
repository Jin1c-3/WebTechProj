const form = document.querySelector('.needs-validation')
const username = document.querySelector('#username')
const password = document.querySelector('#pwd')
const usernameInvalid = document.querySelector('.username-invalid')
const passwordInvalid = document.querySelector('.pwd-invalid')

function checkUsername() {
    const reg1 = /^[a-zA-Z0-9!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]{6,16}$/;
    if (username.value.length < 3 || username.value.length > 18) {
        username.setCustomValidity('用户名长度必须在4到18个字符之间')
        usernameInvalid.innerHTML = '用户名长度必须在4到18个字符之间'
        return false
    } else if ( !reg1.test(username.value) ) {
        username.setCustomValidity('用户名只能包含字母、数字和特殊字符')
        usernameInvalid.innerHTML = '用户名只能包含字母、数字和特殊字符'
        return false
    } else if (username.value.indexOf(" ") !== -1) {
        username.setCustomValidity('用户名不能包含空格')
        usernameInvalid.innerHTML = '用户名不能包含空格'
        return false
    } else {
        username.setCustomValidity('')
        return true
    }
}

function checkPassword() {
    if (password.value.length < 6 || password.value.length > 16) {
        password.setCustomValidity('密码长度必须在6到16个字符之间')
        passwordInvalid.innerHTML = '密码长度必须在6到16个字符之间'
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
