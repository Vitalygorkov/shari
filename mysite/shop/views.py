from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Category, Product, Balloon, Post, Promotions
from django.core.paginator import Paginator


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    products_list = Balloon.objects.all()
    categories = Category.objects.all()
    categories1 = Category.objects.filter(parent='1')
    categories2 = Category.objects.filter(parent='2')
    promotions_list = Promotions.objects.all()
    template = loader.get_template('shop/index.html')
    context = {
        'products_list': products_list,
        'categories': categories,
        'categories1': categories1,
        'categories2': categories2,
        'promotions_list': promotions_list
    }
    return HttpResponse(template.render( context, request))


# def baloon(request):
#     products_list = Balloon.objects.all()
#     categories = Category.objects.all()
#     template = loader.get_template('shop/balloon.html')
#     context = {
#         'products_list': products_list,
#         'categories': categories,
#     }
#     return HttpResponse(template.render( context, request))

def cart(request):
    # cart = request.GET.get("cart", "Undefined")
    # получаем куки с ключом cart
    if request.COOKIES.get('cart'):
        cart_string = request.COOKIES["cart"]
        cart_count = len(cart_string.split(','))
        cart_list = [x.strip() for x in cart_string.split(',')]
        print(cart_list)
        add_to_cart = request.GET.get("add_to_cart", "Undefined")
        print(add_to_cart)
        if add_to_cart != "Undefined":
            cart_list.append(add_to_cart)
        print(cart_list)
        # корзина в итоге в виде объектов
        # cart = Balloon.objects.filter(pk__in=cart_list)


    else:
        cart = ''




    products_list = Balloon.objects.all()
    categories = Category.objects.all()
    template = loader.get_template('shop/cart.html')
    promotions_list = Promotions.objects.all()
    context = {
        'promotions_list': promotions_list,
        'products_list': products_list,
        'categories': categories,
        'cart': cart_list,
        'cart_count': cart_count
    }
    html = HttpResponse(template.render( context, request))

    if request.COOKIES.get('cart'):
        html.set_cookie('cart', ''.join(cart_list))
        # value = int(request.COOKIES.get('visits'))
        # html.set_cookie('cart', value + 1)
    else:
        html.set_cookie('cart', "1,6")
        # value = 1
        # text = "Welcome for the first time"
        # html.set_cookie('visits', value)
        # html.set_cookie('dataflair', text)

    # cart = Balloon.objects.filter(pk__in=cart_list)

    return html


def favorites(request):
    products_list = Balloon.objects.all()
    categories = Category.objects.all()
    template = loader.get_template('shop/favorites.html')
    promotions_list = Promotions.objects.all()
    context = {
        'promotions_list': promotions_list,
        'products_list': products_list,
        'categories': categories,
    }
    return HttpResponse(template.render( context, request))

def blog(request):
    # получаем куки с ключом cart
    if request.COOKIES.get('cart'):
        cart = request.COOKIES["cart"]
        cart_count = len(cart.split(','))
    else:
        cart = ''

    post_list = Post.objects.all()
    categories = Category.objects.all()
    template = loader.get_template('shop/blog.html')
    promotions_list = Promotions.objects.all()
    context = {
        'promotions_list': promotions_list,
        'post_list': post_list,
        'categories': categories,
        'cart': cart,
        'cart_count': cart_count
    }
    return HttpResponse(template.render( context, request))

def promotions_page(request):
    promotions_list = Promotions.objects.all()
    categories = Category.objects.all()
    template = loader.get_template('shop/promotions_page.html')
    promotions_list = Promotions.objects.all()
    context = {
        'promotions_list': promotions_list,
        'categories': categories,
    }
    return HttpResponse(template.render( context, request))

def post(request, post_slug):
    print('Вьюха постов')
    print(post_slug)
    post = Post.objects.get(slug=post_slug)
    # post_list = Post.objects.all()
    categories = Category.objects.all()
    template = loader.get_template('shop/post.html')
    promotions_list = Promotions.objects.all()
    context = {
        'promotions_list': promotions_list,
        'post': post,
        'categories': categories,
    }
    return HttpResponse(template.render( context, request))

def promotions(request, promotions_slug):
    print('Вьюха акций')
    print(promotions_slug)
    promotions = Promotions.objects.get(slug=promotions_slug)
    categories = Category.objects.all()
    template = loader.get_template('shop/promotions.html')
    promotions_list = Promotions.objects.all()
    context = {
        'promotions_list': promotions_list,
        'promotions': promotions,
        'categories': categories,
    }
    return HttpResponse(template.render( context, request))

def search(request):
    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     if query:
    #         return Balloon.objects.filter(title__icontains=query)
    #     else:
    #         return Balloon.objects.all()
    query = request.GET.get('q')
    if query:
        products_list = Balloon.objects.filter(name__icontains=query)
        paginator = Paginator(products_list, 20)
    else:
        products_list = Balloon.objects.all()
        paginator = Paginator(products_list, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    template = loader.get_template('shop/search.html')
    promotions_list = Promotions.objects.all()
    context = {
        'promotions_list': promotions_list,
        'products_list': page_obj,
        'categories': categories,
    }
    return HttpResponse(template.render( context, request))

def category(request, category_slug):
    # Category.objects.filter(url=category_slug)
    branch_categories = Category.objects.filter(url=category_slug).get_descendants(include_self=True)
    print(branch_categories)
    last_category = ''
    try:
        if category_slug:
            print(category_slug)
            last_category = Category.objects.get(url=category_slug)
    except Exception as e:
        print(e)
        print('Ошибка поиска текущей категории ')

    products_list = Balloon.objects.filter(category__in=branch_categories)
    paginator = Paginator(products_list, 30)
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    # template = loader.get_template('shop/category.html')
    template_render = "shop/category.html"
    promotions_list = Promotions.objects.all()
    context = {
        'promotions_list': promotions_list,
        'products_list': page_obj,
        "last_category": last_category,
        'categories': categories,
        'pages': paginator.count,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
    }
    print(last_category)
    print(paginator.count)
    print(paginator.num_pages)
    return render(request, template_render, context)

def show_product(request, product_slug, category_slug):
    categories = Category.objects.all()
    branch_categories = Category.objects.filter(url=category_slug).get_descendants(include_self=True)
    # product = Product.objects.get(slug=product_slug)
    last_category = Category.objects.get(url=category_slug)
    product_balloon = Balloon.objects.get(slug=product_slug)
    # prod1 = product.get_ancestors(asceding=True, include_self=False)
    template_render = "shop/baloon.html"
    # print(categories.filter(name=product.category).get_ancestors(include_self=True)[0].name)

    # if categories.filter(name=product.category).get_ancestors(include_self=True)[0].name == 'Лодки':
    #     product = Boat.objects.get(slug=product_slug)
    #     template_render = "shop/product.html"
    # print("show_product")
    promotions_list = Promotions.objects.all()

    return render(request, template_render, {"product_balloon": product_balloon,
                                             'promotions_list': promotions_list,
                                             "last_category": last_category,
                                            'categories': categories, })