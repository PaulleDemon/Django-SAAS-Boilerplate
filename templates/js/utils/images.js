/**
 * Returns compressed image to be later uploaded to server
 */
const imageCompress = async (imageFile, maxSize=5, maxWidthOrHeight=1920) => {

    const options = {
        maxSizeMB: maxSize,
        maxWidthOrHeight: maxWidthOrHeight,
        useWebWorker: true
    }

    // console.log("FILE: ", imageFile)
    if (!imageFile.name.endsWith(".gif") && !imageFile.name.endsWith(".svg")){
        // don't compress if the file is gif
        try{
            const image = await imageCompression(imageFile, options)
            // console.log("FILE compressed: ", image.size /1024 /1024, image)
            return new File([image], imageFile.name, {type: image.type}) // return file object not blob

        }catch(err){
            return imageFile
        }
    }else{
        return imageFile
    }   
}
