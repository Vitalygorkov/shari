"use strict"

const isMobile = {
    Android: function () {
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function () {
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function () {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function () {
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function () {
        return navigator.userAgent.match(/IEMobile/i);
    },
    any: function () {
        return (
            isMobile.Android() ||
            isMobile.BlackBerry() ||
            isMobile.iOS() ||
            isMobile.Opera() ||
            isMobile.Windows());
    }
};

if (isMobile.any()) {
    document.body.classList.add('_touch');
    let menuArrows =document.querySelectorAll('.menu__arrow');
    if (menuArrows.length > 0){
        for (let index = 0; index < menuArrows.length; index++) {
            const menuArrow = menuArrows[index];
            menuArrow.addEventListener("click", function(e) {
                menuArrow.parentElement.classList.toggle('_active')
            });
        }
    }
} else {
    document.body.classList.add('_pc');
}

/*прокрутка при клике*/
const menuLinkas = document.querySelectorAll('.menu__linka[data-goto]');
if (menuLinkas.length > 0) {
    menuLinkas.forEach(menuLinka => {
        menuLinka.addEventListener("click", onMenuLinkaClick);
    });

    function onMenuLinkaClick(e) {
        const menuLinka = e.target;
        if (menuLinka.dataset.goto && document.querySelector(menuLinka.dataset.goto)){
            const gotoBlock = document.querySelector(menuLinka.dataset.goto);
            const gotoBlockValue = gotoBlock.getBoundingClirntRect().top + pageYOffset - document.querySelector('header').offsetHeight;

            window.scrollTo({
                top: gotoBlockValue,
                behavior: "smooth"
            });
            e.preventDefauit();  /*чтобы не открывалась ссылка а была только прокрутка*/
        }
    }
}
/*меню бургер*/
const iconMenu = document.querySelector('.menu__icona');
if (iconMenu){
    const menuBody = document.querySelector('.menu__bodya');
    iconMenu.addEventListener("click", function (e) {
        document.body.classList.toggle('_lock');
        iconMenu.classList.toggle('_active');
        menuBody.classList.toggle('_active');
    });
}
/*появление при скроле*/
function onEntry(entry) {
    entry.forEach(change => {
      if (change.isIntersecting) {
       change.target.classList.add('element-show');
      }
    });
  }
  
  let options = {
    threshold: [0.5] };
  let observer = new IntersectionObserver(onEntry, options);
  let elements = document.querySelectorAll('.element-animation');
  
  for (let elm of elements) {
    observer.observe(elm);
  }
/*появление при скроле карточки товара*/
