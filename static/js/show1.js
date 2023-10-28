const messages = document.querySelectorAll('.messages')
const allRadios = document.querySelector('#all-radios')
const allRadiosValue = document.querySelector('#all-radios-value')
const tbody = document.querySelector('tbody')
const form = document.querySelector('form')
const pageLinks = document.querySelectorAll('.page-link')
const currentPage = document.querySelector('#current_page')

const radios = tbody.querySelectorAll('.form-check-input')

let value = {}

function All(...args) {
    if (args[0] === 'dels') {
        form.action = '/multidel'
        if (allRadiosValue.value === '' || allRadiosValue.value === '{}') {
            return
        }
    }
    form.submit()
}

window.setTimeout(() => {
    messages.forEach((message) => {
        let btn = message.querySelector('button')
        btn.click()
    })
}, 3000)

allRadios.addEventListener('click', () => {
    radios.forEach((radio) => {
        radio.checked = allRadios.checked
        if (radio.checked) {
            value[radio.value] = radio.value
        } else {
            delete value[radio.value]
        }
    })
    allRadiosValue.value = JSON.stringify(value)
})

radios.forEach((radio) => {
    radio.addEventListener('click', () => {
        if (radio.checked) {
            value[radio.value] = radio.value
            let count = 0
            radios.forEach((radio) => {
                count += radio.checked ? 1 : 0
            })
            if (count === radios.length) {
                allRadios.checked = true
            }
        } else {
            delete value[radio.value]
            allRadios.checked = false
        }
        allRadiosValue.value = JSON.stringify(value)
    })
})

pageLinks.forEach((pageLink) => {
    pageLink.addEventListener('click', () => {
        currentPage.value = pageLink.dataset.page
        All()
    })
})



