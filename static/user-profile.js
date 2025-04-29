'use strict';

// Hide dropdowns when clicking outside
const main = document.querySelector('main');
const userLogin = document.querySelector('.user-login');
const shoppingCart = document.querySelector('.shopping-cart');

main.addEventListener('click', () => {
    userLogin.classList.remove('active');
    shoppingCart.classList.remove('active');
});

// Mobile menu toggles
const mobileMenuOpenBtn = document.querySelectorAll('[data-mobile-menu-open-btn]');
const mobileMenu = document.querySelectorAll('[data-mobile-menu]');
const mobileMenuCloseBtn = document.querySelectorAll('[data-mobile-menu-close-btn]');

mobileMenuOpenBtn.forEach((btn, i) => {
    btn.addEventListener('click', () => mobileMenu[i].classList.add('active'));
    mobileMenuCloseBtn[i].addEventListener('click', () => mobileMenu[i].classList.remove('active'));
});

// Accordion
const accordionBtn = document.querySelectorAll('[data-accordion-btn]');
const accordion = document.querySelectorAll('[data-accordion]');

accordionBtn.forEach((btn, i) => {
    btn.addEventListener('click', function () {
        const isActive = this.nextElementSibling.classList.contains('active');

        if (!isActive) {
            accordion.forEach((acc, j) => {
                acc.classList.remove('active');
                accordionBtn[j].classList.remove('active');
            });
        }

        this.nextElementSibling.classList.toggle('active');
        this.classList.toggle('active');
    });
});

// Back to top button
const mybutton = document.querySelector("[data-back-top-btn]");
window.onscroll = () => {
    if (window.scrollY > 100) {
        mybutton.classList.add('active');
    } else {
        mybutton.classList.remove('active');
    }
};

// Cart and login form toggle
const loginForm = document.querySelector('.user-login');

document.querySelector('#cart-btn').onclick = () => {
    shoppingCart.classList.toggle('active');
    loginForm.classList.remove('active');
};

document.querySelector('#user-login-btn').onclick = () => {
    loginForm.classList.toggle('active');
    shoppingCart.classList.remove('active');
};

// Image upload and popup
const selectImage = document.querySelector('#select-image');
const inputFile = document.querySelector('#file-upload');
const imgArea = document.getElementById('img-area');
const backDrop = document.querySelector('.backdrop');
const elemContainer = document.querySelector('.elem-container');

selectImage.addEventListener('click', () => {
    inputFile.click();
    imgArea.classList.add('active');
    backDrop.classList.add('active');
});

backDrop.addEventListener('click', () => {
    backDrop.classList.remove('active');
    imgArea.classList.remove('active');
    document.querySelector(".popup-image").classList.remove('active');
});

inputFile.addEventListener('change', function () {
    const image = this.files[0];
    const reader = new FileReader();

    reader.onload = () => {
        const imgUrl = reader.result;
        const img = document.createElement('img');
        img.src = imgUrl;
        elemContainer.appendChild(img);
        elemContainer.classList.add('active');
        elemContainer.dataset.img = image.name;
    };

    reader.readAsDataURL(image);
});

// Gender toggle via labels
document.querySelector('.label1').addEventListener('click', () => {
    document.querySelector('.gendermale').checked = true;
});
document.querySelector('.label2').addEventListener('click', () => {
    document.querySelector('.genderfemale').checked = true;
});

// Sidebar navigation
const regForm = document.querySelector('.registration-form');
const prescriptions = document.querySelector('.prescriptions');
const history = document.querySelector('.purchase-history');
const list = document.querySelector('.list');

function showSection(section) {
    regForm.classList.remove('active');
    prescriptions.classList.remove('active');
    history.classList.remove('active');
    list.classList.remove('active');
    section.classList.add('active');
}

document.getElementById('account').onclick =
document.getElementById('account-mob').onclick = () => showSection(regForm);

document.getElementById('prescription').onclick =
document.getElementById('prescription-mob').onclick = () => showSection(prescriptions);

document.getElementById('history').onclick =
document.getElementById('history-mob').onclick = () => showSection(history);

document.getElementById('list').onclick =
document.getElementById('list-mob').onclick = () => showSection(list);

// Prescription image popup
document.querySelectorAll(".prescriptions img").forEach(image => {
    image.onclick = () => {
        document.querySelector(".popup-image img").src = image.getAttribute("src");
        document.querySelector(".popup-image").classList.add('active');
        backDrop.classList.add('active');
    };
});

// Radio-like checkbox toggle using jQuery
$(".days :nth-child(odd)").change(function () {
    $(".days :nth-child(odd)").prop('checked', false);
    $(this).prop('checked', true);
});
