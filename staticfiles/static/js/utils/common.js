/**
 * Author: Paul
 */

/**
 * commonly used functions
 */
let defaultToast = new Toast("#toast")

window.addEventListener("load", () => {
    defaultToast = new Toast("#toast")
})

/**
 * Fetches the country codes json file
 * @returns JS object
 */
async function fetchCountryCodes(){

    try{
        const response = await fetch(`${STATIC_URL}assets/json/phone-codes.json`)

        return await response.json()
    }catch(e){
        return 
    }
}


/**
 * 
 * @param {HTMLElement} alert 
 */
function hideAlertError(alert) {
    alert.classList.add("tw-hidden")
    alert.innerText = ""
}

/**
 * @param {HTMLElement} alert 
 * @param {string} text 
 */
function alertError(alert, text = "") {
    alert.innerText = text
    alert.classList.remove("tw-hidden")
    alert.classList.remove("!tw-hidden")
}

/**
 * Shows toast alert 
 * @param {HTMLElement | null} toast 
 * @param {string} text 
 * @param {"normal" | "danger"} type 
 */
function toastAlert(toast, text = "", type = "normal") {

    if (toast == null) {
        toast = defaultToast
    }

    if (type === "danger") {
        toast.toastContainer.classList.add("tw-bg-red-500",)
        toast.toastContainer.classList.remove("tw-bg-blue-400",)
    } else {
        toast.toastContainer.classList.remove("tw-bg-red-500",)
        toast.toastContainer.classList.add("tw-bg-blue-400")
    }

    toast.show(text)
}

/**
 * 
 * @param {HTMLElement} toast 
 * @param {string} text 
 */
function resetToast(toast) {

    const toastBody = Array.from(toast.getElementsByClassName('toast-body'))
    toastBody.at(-1).innerText = ""

}


function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}


/**
 * 
 * @param {HTMLElement} textbox 
 * @param {function} inputFilter - a function that returns true or false 
 * @param {string} errMsg 
 */
function setInputFilter(textbox, inputFilter, errMsg) {
    ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop", "focusout"].forEach(function (event) {
        textbox.addEventListener(event, function (e) {
            if (inputFilter(this.value)) {
                // Accepted value.
                if (["keydown", "mousedown", "focusout"].indexOf(e.type) >= 0) {
                    this.classList.remove("input-error")
                    this.setCustomValidity("")
                }

                this.oldValue = this.value
                this.oldSelectionStart = this.selectionStart
                this.oldSelectionEnd = this.selectionEnd
            }
            else if (this.hasOwnProperty("oldValue")) {
                // Rejected value: restore the previous one.
                this.classList.add("input-error")
                this.setCustomValidity(errMsg)
                this.reportValidity()
                this.value = this.oldValue
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd)
            }
            else {
                // Rejected value: nothing to restore.
                this.value = ""
            }
        })
    })
}


function slugify(text) {
    if (text) {
        return text.toString().toLowerCase()
            .replace(/\s+/g, '-')
            .replace(/[^\w-]+/g, '')
            .replace(/--+/g, '-')
            .replace(/^-+/, '')
            .replace(/-+$/, '')
    }
    return '';
}

/**
 * 
 * @param {File} file 
 * @param {'MB'|'KB'} unit 
 * @returns 
 */
function getFileSize(file, unit = 'MB') {
    // Check if the input is a valid File object
    if (file instanceof File) {
        const fileSizeInBytes = file.size;

        if (unit === 'KB') {
            // Calculate the file size in kilobytes
            const fileSizeInKB = fileSizeInBytes / 1024;
            return fileSizeInKB.toFixed(2) // Round to 2 decimal places and add the unit
        } else if (unit === 'MB') {
            // Calculate the file size in megabytes
            const fileSizeInMB = fileSizeInBytes / (1024 * 1024);
            return fileSizeInMB.toFixed(2) // Round to 2 decimal places and add the unit
        }
    } else {
        return null; // Invalid input, return null
    }
}

function generateUUID() {
    let d = new Date().getTime();
    if (typeof performance !== 'undefined' && typeof performance.now === 'function') {
        d += performance.now(); // Use high-precision timer if available
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
    });
}

/**
 * returns the current time + additional_time
 * @param {HTMLElement|null} datetimeElement 
 * @param {number} datetimeElement // used to add or subtract to the current time in ms
 */
function setDatetimeToLocal(datetimeElement, additonal_time = 0) {
    const currentDate = new Date();

    // Calculate the datetime 10 minutes from now
    const minDate = new Date(currentDate.getTime() + additonal_time);

    // Format the minDate as a string for the input field
    const minDateString = minDate.toISOString().slice(0, 16);
    // const minDateString = minDate.toUTCString();
    datetimeElement?.setAttribute('min', minDateString);

    return minDate
}

/**
 * 
 * @param {Date} datetime 
 * @returns 
 */
function toLocalTime(datetime) {

    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        timeZoneName: 'short',
        hour12: true,
    };

    return datetime.toLocaleString('en-US', options);

}



function isElementInViewport(el) {
    // tells  if the element is in the viewport
    var rect = el.getBoundingClientRect()

    return (
        rect.top >= -1 &&
        rect.left >= 0 &&
        rect.bottom <=
        (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    )
}

// Check if the element is within the container
/**
 * 
 * @param {HTMLElement} element 
 * @param {HTMLElement} container 
 * @returns 
 */
function isElementVisibleInContainer(element, container) {
    const elementRect = element.getBoundingClientRect();
    const containerRect = container.getBoundingClientRect();

    const isVisible =
        elementRect.top >= containerRect.top &&
        elementRect.bottom <= containerRect.bottom &&
        elementRect.left >= containerRect.left &&
        elementRect.right <= containerRect.right;

    return isVisible;
}