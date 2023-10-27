const form = document.querySelector('.needs-validation')
const in_ = document.querySelector('#in')
const messages = document.querySelectorAll('.messages')

const inInvalid = document.querySelector('.in-invalid')
let code; //在全局定义验证码

function createCode() {
    code = "";
    let codeLength = 4;//验证码的长度
    let checkCode = document.getElementById("code");
    let random = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];//随机数
    for (let i = 0; i < codeLength; i++) {//循环操作
        let index = Math.floor(Math.random() * 36);//取得随机数的索引（0~35）
        code += random[index];//根据索引取得随机数加到code上
    }
    checkCode.value = code;//把code值赋给验证码
}

function check_in() {
    let inputCode = in_.value.toUpperCase(); //取得输入的验证码并转化为大写
    if (inputCode.length <= 0) { //若输入的验证码长度为0
        in_.setCustomValidity('请输入验证码！') //则弹出请输入验证码
        inInvalid.innerHTML = '请输入验证码！'
        return false
    } else if (inputCode !== code) { //若输入的验证码与产生的验证码不一致时
        in_.setCustomValidity('验证码输入错误！') //则弹出验证码输入错误
        inInvalid.innerHTML = '验证码输入错误！'
        createCode();//刷新验证码
    } else { //输入正确时
        in_.setCustomValidity('')
        return true
    }
}


form.addEventListener('submit', (event) => {
    if (!check_in()) {
        event.preventDefault()
        event.stopPropagation()
    }
    form.classList.add('was-validated')
})

window.addEventListener('load', () => {
    createCode();
})

window.setTimeout(() => {
    messages.forEach((message) => {
        let btn = message.querySelector('button')
        btn.click()
    })
}, 3000)