/**
 * Contains code for home page
 */


const carouselImageContainer = document.querySelector("#slideshow")

const images = [
    "assets/images/home/hiking1.jpg",
    "assets/images/home/hiking2.jpg",
    "assets/images/home/hiking3.jpg",
    "assets/images/home/hiking4.jpg",
]

function addSlideShowImages(img) {

    const imageContainer = document.createElement("div")

    imageContainer.classList.add("swiper-slide", "slide", "tw-rounded-md", "!tw-h-[450px]")

    imageContainer.innerHTML += `
                <img src="${STATIC_URL+img}" 
                        alt="hiking"
                        class="tw-object-cover tw-w-full tw-h-full">
    `
    carouselImageContainer.prepend(imageContainer)

}

// images.forEach(img => addSlideShowImages(img))
// images.forEach(img => addSlideShowImages(img))



// const swiper = new Swiper(".slideshow-container", {
//     effect: "creative",
//     grabCursor: true,
//     loop: true,
//     centeredSlides: true,
//     slidesPerView: "auto",
//     creativeEffect: {
//         prev: {
//           shadow: true,
//           origin: "left center",
//           translate: ["-5%", 0, -200],
//           rotate: [0, 100, 0],
//         },
//         next: {
//           origin: "right center",
//           translate: ["5%", 0, -200],
//           rotate: [0, -100, 0],
//         },
//     },
//     navigation: {
//         nextEl: '.next',
//         prevEl: '.prev',
//     },
//     autoplay: {
//         delay: 5000,
//     },
// })

const reviewContainer = document.querySelector(".review-container")
const reviewSlideShow = new SlideShow(reviewContainer, true, 10000)


const reviewModal = new Modal(document.querySelector("#modal"))
