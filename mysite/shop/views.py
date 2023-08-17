from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Category, Product, ProductFilter, Balloon, Post, Promotions, TagsProducts, Color
from django.core.paginator import Paginator
from django.db.models import Max,Min


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
    categories = Category.objects.all()
    products_list = Balloon.objects.all()
    promotions_list = Promotions.objects.all()
    template = loader.get_template('shop/cart.html')


    # html = HttpResponse(template.render(context, request))
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
        print(cart_list)
        print(cart_count)

        # html.set_cookie('cart', ','.join(cart_list))
        # корзина в итоге в виде объектов
        cart = Balloon.objects.filter(pk__in=cart_list).distinct("pk")


    else:
        # html.set_cookie('cart', "")
        cart = ''
        cart_list = ''
        cart_count = ''


    context = {
        'categories': categories,
        'promotions_list': promotions_list,
        'products_list': products_list,
        'categories': categories,
        'cart': cart,
        'cart_count': cart_count
    }


    html = HttpResponse(template.render( context, request))
    html.set_cookie('cart', ','.join(cart_list))

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
        cart_list = ''
        cart_count = ''

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
    parents = Category.objects.filter(url=category_slug).get_ancestors(include_self=False)
    # parents_categories = Category.objects.filter(url=category_slug).get_ancestors(ascending=False, include_self=False)
    print('запрос:')
    if request.method == 'GET':
        color_filter_leist = request.GET.getlist('color__name')
    elif request.method == 'POST':
        qd = request.POST
    print(color_filter_leist)
    # Category.objects.filter(url=category_slug)
    colors = Color.objects.all()
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
    print(branch_categories)
    products_list = Balloon.objects.filter(category__in=branch_categories)
    max_price = Balloon.objects.filter(category__in=branch_categories).aggregate(Max('price'))['price__max']
    min_price = Balloon.objects.filter(category__in=branch_categories).aggregate(Min('price'))['price__min']
    filter = ProductFilter(request.GET, queryset=products_list)
    products_list = filter.qs
    paginator = Paginator(products_list, 30)
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    tags = TagsProducts.objects.all()
    # template = loader.get_template('shop/category.html')
    template_render = "shop/category.html"
    promotions_list = Promotions.objects.all()
    context = {
        'parents': parents,
        'promotions_list': promotions_list,
        'products_list': page_obj,
        "last_category": last_category,
        'categories': categories,
        'pages': paginator.count,
        "branch_categories": branch_categories,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "tags": tags,
        'colors': colors,
        'filter': filter,
        'max_price': max_price,
        'min_price': min_price,
    }
    print(last_category)
    print(paginator.count)
    print(paginator.num_pages)
    return render(request, template_render, context)

def tags_view(request, tag_slug):
    # Category.objects.filter(url=category_slug)
    # branch_categories = Category.objects.filter(slug=category_slug).get_descendants(include_self=True)
    # print(branch_categories)
    last_category = ''
    # try:
    #     if category_slug:
    #         print(category_slug)
    #         last_category = Category.objects.get(url=category_slug)
    # except Exception as e:
    #     print(e)
    #     print('Ошибка поиска текущей категории ')

    tag_obj = TagsProducts.objects.filter(slug=tag_slug)
    print(tag_obj)
    print(tag_obj[0].id)
    products_list = Balloon.objects.filter(tag=tag_obj[0].id)
    paginator = Paginator(products_list, 30)
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = TagsProducts.objects.all()
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
        "tags": tags
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

    promotions_list = Promotions.objects.all()
    print(promotions_list)
    context = {
        'product_balloon': product_balloon,
        'promotions_list': promotions_list,
        "last_category": last_category,
        'categories': categories,
    }

    # return render(request, template_render, {"product_balloon": product_balloon,
    #                                          'promotions_list': promotions_list,
    #                                          "last_category": last_category,
    #                                         'categories': categories, })
    return render(request, template_render, context)