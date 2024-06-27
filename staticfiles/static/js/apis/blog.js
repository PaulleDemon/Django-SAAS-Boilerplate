
/**
 * Step2. save to server
 *
 * @param {string} blogid
 * @param {File} file
 */
async function saveBlogImage({ blogid, file }) {
    const fd = new FormData()
    
    fd.append('blog', blogid)
    fd.append('image', file)

    const res = await fetch(`/blog/image/upload/?blogid=${blogid}`, {
        method: "POST",
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
            // "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryABC123"
            }, 
        body: fd
    })

    return res
}