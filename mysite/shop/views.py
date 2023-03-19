from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Category, Product, Balloon


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    products_list = Balloon.objects.all()
    categories = Category.objects.all()
    template = loader.get_template('shop/index.html')
    context = {
        'products_list': products_list,
        'categories': categories,
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
    products_list = Balloon.objects.all()
    categories = Category.objects.all()
    template = loader.get_template('shop/cart.html')
    context = {
        'products_list': products_list,
        'categories': categories,
    }
    return HttpResponse(template.render( context, request))

def favorites(request):
    products_list = Balloon.objects.all()
    categories = Category.objects.all()
    template = loader.get_template('shop/favorites.html')
    context = {
        'products_list': products_list,
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
    print(products_list)
    categories = Category.objects.all()
    # template = loader.get_template('shop/category.html')
    template_render = "shop/category.html"
    context = {
        'products_list': products_list,
        "last_category": last_category,
        'categories': categories,
    }
    print(last_category)
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

    return render(request, template_render, {"product_balloon": product_balloon,
                                             "last_category": last_category,
                                            'categories': categories, })