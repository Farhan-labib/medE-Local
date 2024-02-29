'use strict';

const main = document.querySelector('main');
const userLogin = document.querySelector('.user-login');
const shoppingcart = document.querySelector('.shopping-cart');

main.addEventListener('click', function(){
    userLogin.classList.remove('active');
    shoppingcart.classList.remove('active');
})

const mobileMenuOpenBtn = document.querySelectorAll('[data-mobile-menu-open-btn]');
const mobileMenu = document.querySelectorAll('[data-mobile-menu]');
const mobileMenuCloseBtn = document.querySelectorAll('[data-mobile-menu-close-btn]');

for (let i=0; i < mobileMenuOpenBtn.length; i++) {
    const mobileMenuCloseFunc = function () {
        mobileMenu[i].classList.remove('active');
    }
    mobileMenuOpenBtn[i].addEventListener('click', function () {
        mobileMenu[i].classList.add('active');
    });

    mobileMenuCloseBtn[i].addEventListener('click', mobileMenuCloseFunc);
}


// ACCORDION MENU

const accordionBtn = document.querySelectorAll('[data-accordion-btn]');
const accordion = document.querySelectorAll('[data-accordion]');

for (let i = 0; i < accordionBtn.length; i++) {

    accordionBtn[i].addEventListener('click', function () {

        const clickedBtn = this.nextElementSibling.classList.contains('active');

        for (let i = 0; i < accordion.length; i++) {
            if (clickedBtn) break;

            if (accordion[i].classList.contains('active')) {
                
                accordion[i].classList.remove('active');
                accordionBtn[i].classList.remove('active');
            }
        }
        this.nextElementSibling.classList.toggle('active');
        this.classList.toggle('active');
    });
}

// BACK TO TOP BUTTON

const mybutton = document.querySelector("[data-back-top-btn]");
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (window.scrollY > 100) {
    mybutton.classList.add('active');
  } else {
    mybutton.classList.remove('active');
  }
}

let shoppingCart = document.querySelector('.shopping-cart');

document.querySelector('#cart-btn').onclick = () =>{
    shoppingCart.classList.toggle('active');
    loginForm.classList.remove('active');
}

let loginForm = document.querySelector('.user-login');

document.querySelector('#user-login-btn').onclick = () =>{
    loginForm.classList.toggle('active');
    shoppingCart.classList.remove('active');
}

const selectImage = document.querySelector('#select-image');
const inputFile = document.querySelector('#file-upload');
const imgArea = document.getElementById('img-area');
const backDrop = document.querySelector('.backdrop');
const elemContainer = document.querySelector('.elem-container');

selectImage.addEventListener('click', function () {
    inputFile.click();
    imgArea.classList.add('active');
    backDrop.classList.add('active');
})
backDrop.addEventListener('click', function () {
    backDrop.classList.remove('active');
    imgArea.classList.remove('active');
    document.querySelector(".popup-image").classList.remove('active');
})

inputFile.addEventListener('change', function () {
    const image = this.files[0]
    // console.log(image);
    const reader = new FileReader();
    reader.onload = ()=> {
        const imgUrl = reader.result;
        const img = document.createElement('img');
        img.src = imgUrl;
        elemContainer.appendChild(img);
        elemContainer.classList.add('active');
        elemContainer.dataset.img = image.name;
    }
    reader.readAsDataURL(image);
})

// var sidebarSections = document.querySelectorAll('.sidebar-sections');
// var contentBx = document.querySelectorAll('.contentBx');

// for (var i = 0; i < sidebarSections.length; i++){
//     sidebarSections[i].addEventListener('mouseover', function(){
//         for (var i = 0; i < contentBx.length; i++){
//             contentBx[i].className='contentBx';
//         }
//         document.getElementById(this.dataset.id).className = 'contentBx active';

//         for (var i = 0; i < sidebarSections.length; i++){
//             sidebarSections[i].className='sidebar-sections';
//         }
//         this.className = 'sidebar-sections active';
//     });
// };

document.querySelector('.label1').addEventListener('click', function(){
    document.querySelector('.gendermale').checked = true;
})
document.querySelector('.label2').addEventListener('click', function(){
    document.querySelector('.genderfemale').checked = true;
})

/////////////////////
// SIDEBAR
/////////////////////

const regForm = document.querySelector('.registration-form');
const prescriptions = document.querySelector('.prescriptions');
const history = document.querySelector('.purchase-history');
const list = document.querySelector('.list');

document.getElementById('account').addEventListener('click', function(){
    regForm.classList.add('active');
    prescriptions.classList.remove('active');
    history.classList.remove('active');
    list.classList.remove('active');
});

document.getElementById('account-mob').addEventListener('click', function(){
    regForm.classList.add('active');
    prescriptions.classList.remove('active');
    history.classList.remove('active');
    list.classList.remove('active');
});

document.getElementById('prescription').addEventListener('click', function(){
    prescriptions.classList.add('active');
    regForm.classList.remove('active');
    history.classList.remove('active');
    list.classList.remove('active');
});

document.getElementById('prescription-mob').addEventListener('click', function(){
    prescriptions.classList.add('active');
    regForm.classList.remove('active');
    history.classList.remove('active');
    list.classList.remove('active');
});

document.getElementById('history').addEventListener('click', function(){
    history.classList.add('active');
    regForm.classList.remove('active');
    prescriptions.classList.remove('active');
    list.classList.remove('active');
});
document.getElementById('history-mob').addEventListener('click', function(){
    history.classList.add('active');
    regForm.classList.remove('active');
    prescriptions.classList.remove('active');
    list.classList.remove('active');
});
document.getElementById('list').addEventListener('click', function(){
    list.classList.add('active');
    history.classList.remove('active');
    regForm.classList.remove('active');
    prescriptions.classList.remove('active');
});
document.getElementById('list-mob').addEventListener('click', function(){
    list.classList.add('active');
    history.classList.remove('active');
    regForm.classList.remove('active');
    prescriptions.classList.remove('active');
});

const prescBox = document.getElementsByClassName('.presc-box');

document.querySelectorAll(".prescriptions img").forEach(image =>{
    image.onclick = () =>{
        document.querySelector(".popup-image img").src = image.getAttribute("src");
        document.querySelector(".popup-image").classList.add('active');
        backDrop.classList.add('active');
    }
});

$(".days :nth-child(odd)").change(function(){
    $(".days :nth-child(odd)").prop('checked',false);
    $(this).prop('checked',true);
    // console.log($(this).val());
});