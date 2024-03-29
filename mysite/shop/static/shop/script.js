"use strict"
const isMobile = {
    Android: function () {
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function() {
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function() {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function() {
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function() {
        return navigator.userAgent.match(/IEMobile/i);
    },
    any: function() {
        return (
            isMobile.Android() || 
            isMobile.BlackBerry() || 
            isMobile.iOS() || 
            isMobile.Opera() || 
            isMobile.Windows());
    }
};

function menArr(id) {
    const element = document.getElementById(id);
    element.parentElement.classList.toggle('_active2');


}

if(isMobile.any() ) {
  document.body.classList.add('_touch');

//  let menuArrows = document.querySelectorAll('.menu__arrowa');
//  if (menuArrows.length > 0) {
//    for (let index = 0; index < menuArrows.length; index++) {
//        const menuArrow = menuArrows[index];
//        menuArrow.addEventListener("click", function (e) {
//            menuArrow.parentElement.classList.toggle('_active');
//        });
//    }
//  }

} else {
    document.body.classList.add('_pc');
}


const iconMenu = document.querySelector('.menu__icona');
if (iconMenu) {
    const menuBody = document.querySelector('.menu__bodya');
    iconMenu.addEventListener("click", function (e) {
        document.body.classList.toggle('_lock');
        iconMenu.classList.toggle('_active');
        menuBody.classList.toggle('_active');
    });
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
            const gotoBlockValue = gotoBlock.getBoundingClirntRect().top + pageYOffset - document.querySelector('headera').offsetHeight;

            window.scrollTo({
                top: gotoBlockValue,
                behavior: "smooth"
            });
            e.preventDefauit();  /*чтобы не открывалась ссылка а была только прокрутка*/
        }
    }
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

/*функция показа цветов*/
function ShowColors(){
    let element = document.getElementById("color-det-id");
    element.classList.toggle('active-colors')
    let element2 = document.getElementById("colors-img-id");
    element2.classList.toggle('colors-open-img')
}
/*функция показа цветов*/

/*------------корзина---*/
var cart_cookie = decodeURIComponent(getCookie('cart'))
var cart = cart_cookie.split(',')
var cart_length = cart.length
var cart_list_id = []
UpdateCartlistID()
CartValid()

//Валидация корзины
function CartValid(){
cart.forEach((item, i)=>{
        if (cart[i].split(':')[1]) {
            console.log('if в проверке валидности корзины')
//            cart.splice(i,1)
        }else{
        console.log('else в проверке валидности корзины')
        cart.splice(i,1)
        }
    })

}


function UpdateHtmlValues(){
        UpdateCartlistID()
        UpdateItog()
        document.getElementById("cart_numb").textContent = cart.length
//        document.getElementById("total-price-id").textContent = cart.length
        cart.forEach((item, i)=>{
//            if (cart[i].split(':')[0]==card_id) {
//                cart[i] = cart[i].split(':')[0]+':'+String(Number(cart[i].split(':')[1])+1)
                let prod_id = cart[i].split(':')[0]
                if (document.getElementById(`prod_count${prod_id}`)) {
                    document.getElementById(`prod_count${prod_id}`).textContent = cart[i].split(':')[1]
                }
                if (document.getElementById(`prod_sum${prod_id}`)) {
                    let prodprice = document.getElementById(`prod_price${prod_id}`)
                    console.log("Обновление цен, объект див суммы",prodprice.innerText )
                    document.getElementById(`prod_sum${prod_id}`).textContent = cart[i].split(':')[1]*prodprice.innerText
                }
//                document.getElementById(`prod_count${prod_id}`).textContent = cart[i].split(':')[1]
//                console.log('prod_id',prod_id, `prod_count${prod_id}`)

//            }
        })


}

function UpdateCartlistID(){
    console.log('обновление списка ID')
    cart_list_id = []
    cart.forEach((item, i)=>{
        cart_list_id[i] = cart[i].split(':')[0]
    })
}

function getCookie(name) {
  let match = document.cookie
     .split('; ')
     .find(row => row.startsWith(`${name}=`));

  return match ? match.split('=')[1] : undefined;
}

function setCookie(name, value) {
    document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}`+"; path=/;"
    console.log("setCookie: ", `${encodeURIComponent(name)}=${encodeURIComponent(value)}`+"; path=/;")
}
function AddToCart(card_id){
        UpdateHtmlValues()
        console.log("CART_LIST_ID",cart_list_id)
        card_id = String(card_id)
        if (cart_list_id.includes(card_id)) {
        console.log('Добавление товара if')
        cart.forEach((item, i)=>{
                if (cart[i].split(':')[0]==card_id) {
                    cart[i] = cart[i].split(':')[0]+':'+String(Number(cart[i].split(':')[1])+1)
                }
            })
        setCookie('cart', cart)
        UpdateCartlistID()
        console.log('cart', cart)
        }else{
        cart.push(card_id+':'+'1')
        setCookie('cart', cart)
        console.log('Добавление товара else')
        UpdateCartlistID()
        UpdateProductsInCart()
        console.log('cart', cart)
        }
        UpdateHtmlValues()
}

function RemoveToCart(card_id){
        card_id = String(card_id)
        if (cart_list_id.includes(card_id)) {
        cart.forEach((item, i)=>{
                if (cart[i].split(':')[0]==card_id) {
                    console.log('удаление, нашли нужный ид')
                    if (Number(cart[i].split(':')[1])>=2) {
                        console.log('товаров больше или равно 2 убираем 1')
                        //делаем на 1 меньше
                        cart[i] = cart[i].split(':')[0]+':'+String(Number(cart[i].split(':')[1])-1)
                    }else{console.log('товаров 1 удаляем из списка, убираем элемент')
                        let index = cart.indexOf(cart[i]);
                        console.log('index: ',index)
                        if (index !== -1) {
                          cart.splice(index, 1);
                        }
                        console.log('Удаляем element ', card_id)
                        document.getElementById(`cart-blok${card_id}`).remove();

                    }
                }else{console.log('такого товара вообще нет в списке')}
            })
        console.log('cart', cart)
        UpdateCartlistID()
        setCookie('cart', cart)
        }else{
        console.log('Удаление товара else')
        console.log('cart', cart)
        }
        UpdateHtmlValues()
}

function UpdateItog(){
    let itogsum = 0
    let elemitog = document.getElementById("total-price-id")
    let elements_for_sum = document.querySelectorAll(".cart-sum");
//    console.log('UpdateItog', elements_for_sum)

    elements_for_sum.forEach((item, i)=>{
        console.log('UpdateItog', item.innerText)
    })




}

var products_in_cart = document.getElementsByClassName('cart-blok');
 console.log("products_in_cart", products_in_cart)
function UpdateProductsInCart(){
    if(products_in_cart.length>=1){
    console.log('products_in_cart',products_in_cart)
        console.log("Функция обновления товаров в корзине")
    Array.prototype.forEach.call(products_in_cart, function(el) {
        // Do stuff here
        console.log(el.children[2].children[1].innerHTML);
    });
     console.log("products_in_cart", products_in_cart)
    }else{
    console.log("products_in_cart", products_in_cart)
    }
}

// вставляем количество товарова в менюсверху в корзине в элемент корзины
//document.getElementById("cart_numb").textContent = cart.length
UpdateHtmlValues()
// вставляем количество товаров в странице корзины
//document.getElementById("prod_count").textContent = cart_length
//pcs__calc-imput

// вручную задать куку корзины
//setCookie('cart', '1:1,7:1,3:1,12:1,4:1')
//
//document.cookie = 'cart=1,1,2,3,4'

//для исправления багов в корзине
//cart = []
//UpdateProductsInCart()
//setCookie('cart', '')


console.log("Ваши куки сэр:", document.cookie)
console.log("кука cart сэр:", decodeURIComponent(cart_cookie))
console.log("ваша корзина сэр: ", cart)
console.log("cart_list_id сэр: ", cart_list_id)