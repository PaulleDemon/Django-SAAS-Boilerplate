
const countryCodeDropdown = document.getElementById("country-codes")


// console.log(JSON.parse(countryCodes))

async function loadCountryCodes(){

    const countryCodes = await fetchCountryCodes()

    if (!countryCodes){
        toastAlert("failed to fetch country codes")
        return
    }

    countryCodes.forEach(e => {
        const option = document.createElement("option")

        option.innerText = `${e.emoji} ${e.dial_code}`
        option.setAttribute("value", e.dial_code)
        
        if (e.code === "US")
            option.setAttribute("selected", "selected")

        countryCodeDropdown.appendChild(option)
    }) 


}

loadCountryCodes()


const phone = document.querySelector("input[name='phone']") // full phone number
const countryCode = document.querySelector("select[name='country-codes']")
const phoneNumber = document.querySelector("input[name='phone-number']") // number without country code
const visitorName = document.querySelector("input[name='name']")
const email = document.querySelector("input[name='email']")


setInputFilter(phoneNumber, (value) => {
    return /^[0-9]*$/.test(value)
}, "only numbers are allowed")


function onSubmit(event){
    // event.preventDefault()

    if (visitorName.value.length < 2){
        toastAlert(null, "Enter a proper name", "danger")
        event.stopImmediatePropagation()
        return false
    }

    if (!isValidEmail(email.value)){
        toastAlert(null, "Enter a valid email", "danger")
        event.stopImmediatePropagation()
        return false
    }

    if ((phoneNumber.getAttribute("required") || phoneNumber.value.length > 1) && phoneNumber.value.length < 5){
        toastAlert(null, "Enter a proper phone number", "danger")
        event.stopImmediatePropagation()
        
        return false
    }

    phone.value = `${countryCode.value + phoneNumber.value}`

    // console.log("phone number: ", phone.value)

    return true
}