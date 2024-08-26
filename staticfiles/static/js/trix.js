Trix.config.blockAttributes.heading2 = {
    tagName: "h2",
    className: "sample                                                                                                                                          ",
    breakOnReturn: true,
    group: false,
    terminal: true
}

Trix.config.blockAttributes.heading3 = {
    tagName: "h3",
    breakOnReturn: true,
    group: false,
    terminal: true
}


function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim()
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break
            }
        }
    }
    return cookieValue
}
let fileUploadBtn = document.querySelector("[data-trix-action='attachFiles']")


window.addEventListener('trix-file-accept', function(event) {
  
    const acceptedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if (!acceptedTypes.includes(event.file.type)) {
        event.preventDefault()
        alert("Only support image files")
    }

    // if the id is null, then save the draft before adding the image
    const id = document.querySelector(".field-id .readonly")

    if (id.innerText === '-'){
        const saveBtn = document.querySelector("input[name='_continue']")
        saveBtn.focus()
        saveBtn.click()
        
        event.preventDefault()

        return null
    }

})

// Trix.config.attachments

document.addEventListener("trix-attachment-add", function (event) {

    if (!event.attachment.file) {
        event.attachment.remove()
    }

    if (event.attachment.file) {
        handleUpload(event.attachment)
    }
})

function handleUpload(attachment) {
    uploadFile(attachment.file, setProgress, setAttributes)

    function setProgress(progress) {
        attachment.setUploadProgress(progress)
    }

    function setAttributes(attributes) {
        attachment.setAttributes(attributes)
    }
}

function uploadFile(file, progressCallback, successCallback) {
    var formData = new FormData()
    var xhr = new XMLHttpRequest()

    const id = document.querySelector(".field-id .readonly")

    formData.append("Content-Type", file.type)
    
    formData.append("image", file)
    formData.append("blog", id.innerText) // id of the blog

    xhr.open("POST", "/blog/image/upload/", true)
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"))
    xhr.upload.addEventListener("progress", function (event) {
        progressCallback(event.loaded / event.total * 100)
    })
    xhr.addEventListener("load", function (event) {
        if (xhr.status === 201) {
            let attributes = {
                url: JSON.parse(xhr.responseText).url
            }
            successCallback(attributes)
        }
    })
    xhr.send(formData)
}

window.addEventListener("trix-initialize", event => {

    const { toolbarElement } = event.target

    if (!toolbarElement.querySelector("[data-trix-action='attachFiles']")) {
        // for unfold trix editor
        const strikeAttribute = toolbarElement.querySelector("[data-trix-attribute='strike']")

        // Add the file upload button to the toolbar
        strikeAttribute.insertAdjacentHTML("afterend", `
            <button type="button" class="border-r cursor-pointer flex items-center h-8 justify-center transition-colors w-8 hover:text-primary-600 dark:border-gray-700" 
                    data-trix-action="attachFiles" title="Attach files" tabindex="-1">
                    <span class="material-symbols-outlined">
                        upload
                    </span>
            </button>
        `)
    }

    const h1Button = toolbarElement.querySelector("[data-trix-attribute=heading1]")

    // h1Button.insertAdjacentHTML("afterend", `
    //     <button type="button" class="trix-button" data-trix-attribute="heading2" 
    //             title="Heading 2" tabindex="-1" data-trix-active="">H2</button>
    // `)
    // const h2Button = toolbarElement.querySelector("[data-trix-attribute=heading2]")

    // h2Button.insertAdjacentHTML("afterend", `
    //     <button type="button" class="trix-button" data-trix-attribute="heading3" 
    //     title="Heading 3" tabindex="-1" data-trix-active="">H3</button>
    // `)
    
    
})