"use strict";


const selectImage = document.querySelector("#select-image");
const selectImage2 = document.querySelector("#select-image2");
const inputFile = document.querySelector("#file-upload");
const imgArea = document.getElementById("img-area");
const backDrop = document.querySelector(".backdrop");
const elemContainer = document.querySelector(".elem-container");

const mybutton = document.querySelector("[data-back-top-btn]");

//////////////////////
// BACK TO TOP BUTTON
//////////////////////



window.onscroll = function () {
    scrollFunction();
};

function scrollFunction() {
    if (window.scrollY > 100) {
        mybutton.classList.add("active");
    } else {
        mybutton.classList.remove("active");
    }
};


$(".days :nth-child(odd)").change(function(){
    $(".days :nth-child(odd)").prop('checked',false);
    $(this).prop('checked',true);
    // console.log($(this).val());
});

/////////////////////////////
// FRONT PAGE BANNER CAROUSEL
/////////////////////////////

var counter = 1;

setInterval(function () {
    document.getElementById("radio" + counter).checked = true;
    counter++;
    if (counter > 5) {
        counter = 1;
    }
}, 3000);

const main = document.querySelector("main");
// const userLogin = document.querySelector(".user-login");
const shoppingCart = document.querySelector(".shopping-cart");

main.addEventListener("click", function () {
    userLogin.classList.remove("active");
    shoppingCart.classList.remove("active");
});

const mobileMenuOpenBtn = document.querySelectorAll(
    "[data-mobile-menu-open-btn]"
);
const mobileMenu = document.querySelectorAll("[data-mobile-menu]");
const mobileMenuCloseBtn = document.querySelectorAll(
    "[data-mobile-menu-close-btn]"
);

for (let i = 0; i < mobileMenuOpenBtn.length; i++) {
    const mobileMenuCloseFunc = function () {
        mobileMenu[i].classList.remove("active");
    };
    mobileMenuOpenBtn[i].addEventListener("click", function () {
        mobileMenu[i].classList.add("active");
    });

    mobileMenuCloseBtn[i].addEventListener("click", mobileMenuCloseFunc);
}

// ACCORDION MENU

const accordionBtn = document.querySelectorAll("[data-accordion-btn]");
const accordion = document.querySelectorAll("[data-accordion]");

for (let i = 0; i < accordionBtn.length; i++) {
    accordionBtn[i].addEventListener("click", function () {
        const clickedBtn = this.nextElementSibling.classList.contains("active");

        for (let i = 0; i < accordion.length; i++) {
            if (clickedBtn) break;

            if (accordion[i].classList.contains("active")) {
                accordion[i].classList.remove("active");
                accordionBtn[i].classList.remove("active");
            }
        }
        this.nextElementSibling.classList.toggle("active");
        this.classList.toggle("active");
    });
}

document.querySelector("#cart-btn").onclick = () => {
    shoppingCart.classList.toggle("active");
    userLogin.classList.remove("active");
};

const userLogin = document.querySelector(".user-login");

document.querySelector("#user-login-btn").onclick = () => {
    userLogin.classList.toggle("active");
    shoppingCart.classList.remove("active");
};

///////////////////////
// PRESCRIPTION UPLOAD
//////////////////////

selectImage.addEventListener("click", function () {
    inputFile.click();
    imgArea.classList.add("active");
    backDrop.classList.add("active");
});
selectImage2.addEventListener("click", function () {
    imgArea.classList.add("active");
    backDrop.classList.add("active");
});

backDrop.addEventListener("click", function () {
    backDrop.classList.remove("active");
    imgArea.classList.remove("active");
});

inputFile.addEventListener("change", function () {
    const image = this.files[0];
    // console.log(image);
    const reader = new FileReader();
    reader.onload = () => {
        const imgUrl = reader.result;
        const img = document.createElement("img");
        img.src = imgUrl;
        elemContainer.appendChild(img);
        elemContainer.classList.add("active");
        elemContainer.dataset.img = image.name;
    };
    reader.readAsDataURL(image);
});