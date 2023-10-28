const messages = document.querySelectorAll('.messages')
const allRadios = document.querySelector('#all-radios')
const allRadiosValue = document.querySelector('#all-radios-value')
const tbody = document.querySelector('tbody')
const form = document.querySelector('form')
const pageLinks = document.querySelectorAll('.page-link')
const currentPage = document.querySelector('#current_page')
const updateMany = document.querySelector('#updateMany')
const updateTable = document.querySelector('.modal-body').querySelector('table')
const allUpdateData = document.querySelector('#all-updates-data')

const radios = tbody.querySelectorAll('.form-check-input')

let value = {}

function All(...args) {
    if (args[0] === 'dels') {
        form.action = '/multidel'
        if (allRadiosValue.value === '' || allRadiosValue.value === '{}') {
            return
        }
    } else if (args[0] === 'updates') {
        form.action = '/multupdate'
        if (allUpdateData.value === '' || allUpdateData.value === '[]') {
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

updateMany.addEventListener('click', () => {
    let datas = []
    let trs = updateTable.querySelector('tbody').querySelectorAll('tr')
    trs.forEach((tr) => {
        let data = []
        let inputs = tr.querySelectorAll('input')
        inputs.forEach((input) => {
            data.push(input.value)
        })
        datas.push(data)
    })
    allUpdateData.value = JSON.stringify(datas)
    All('updates')
})

