const form = document.querySelector('.needs-validation')
const stu_id = document.querySelector('#stu_id')
const stu_name = document.querySelector('#stu_name')
const stu_age = document.querySelector('#stu_age')
const stu_origin = document.querySelector('#stu_origin')

const stuIdInvalid = document.querySelector('.stu_id-invalid')
const stuNameInvalid = document.querySelector('.stu_name-invalid')
const stuAgeInvalid = document.querySelector('.stu_age-invalid')
const stuOriginInvalid = document.querySelector('.stu_origin-invalid')

const functions = ['checkStuId', 'checkStuName', 'checkStuAge', 'checkStuOrigin']


function checkStuId() {
    const reg1 = /^[0-9]{9}$/;
    if (stu_id.value.length !== 9) {
        stu_id.setCustomValidity('学号长度必须为9位')
        stuIdInvalid.innerHTML = '学号长度必须为9位'
        return false
    } else if (!reg1.test(stu_id.value)) {
        stu_id.setCustomValidity('学号只能包含数字')
        stuIdInvalid.innerHTML = '学号只能包含数字'
        return false
    } else {
        stu_id.setCustomValidity('')
        return true
    }
}

function checkStuName() {
    const reg1 = /^[\u4e00-\u9fa5]{2,4}$/;
    if (stu_name.value.length < 2 || stu_name.value.length > 4) {
        stu_name.setCustomValidity('姓名长度必须在2到4个字符之间')
        stuNameInvalid.innerHTML = '姓名长度必须在2到4个字符之间'
        return false
    } else if (!reg1.test(stu_name.value)) {
        stu_name.setCustomValidity('姓名只能包含汉字')
        stuNameInvalid.innerHTML = '姓名只能包含汉字'
        return false
    } else {
        stu_name.setCustomValidity('')
        return true
    }
}

function checkStuAge() {
    const reg1 = /^[0-9]{1,2}$/;
    if (stu_age.value.length > 2) {
        stu_age.setCustomValidity('年龄长度不能超过2位')
        stuAgeInvalid.innerHTML = '年龄长度不能超过2位'
        return false
    } else if (!reg1.test(stu_age.value)) {
        stu_age.setCustomValidity('年龄只能包含数字')
        stuAgeInvalid.innerHTML = '年龄只能包含数字'
        return false
    } else {
        stu_age.setCustomValidity('')
        return true
    }
}

function checkStuOrigin() {
    const reg1 = /^[\u4e00-\u9fa5]{2,4}$/;
    if (stu_origin.value.length < 2 || stu_origin.value.length > 4) {
        stu_origin.setCustomValidity('籍贯长度必须在2到4个字符之间')
        stuOriginInvalid.innerHTML = '籍贯长度必须在2到4个字符之间'
        return false
    } else if (!reg1.test(stu_origin.value)) {
        stu_origin.setCustomValidity('籍贯只能包含汉字')
        stuOriginInvalid.innerHTML = '籍贯只能包含汉字'
        return false
    } else {
        stu_origin.setCustomValidity('')
        return true
    }
}

form.addEventListener('submit', (event) => {
    let count = 0
    console.log(functions)
    functions.forEach((func) => {
        if (window[func]()) {
            count += 1
        }
    })
    if (count < functions.length) {
        event.preventDefault()
        event.stopPropagation()
    }
    form.classList.add('was-validated')
})
