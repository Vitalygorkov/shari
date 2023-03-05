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


def baloon(request):
    products_list = Balloon.objects.all()
    categories = Category.objects.all()
    template = loader.get_template('shop/balloon.html')
    context = {
        'products_list': products_list,
        'categories': categories,
    }
    return HttpResponse(template.render( context, request))

def cart(request):
    products_list = Balloon.objects.all()
    template = loader.get_template('shop/cart.html')
    context = {
        'products_list': products_list,
    }
    return HttpResponse(template.render( context, request))

def category(request, category_slug):
    # Category.objects.filter(url=category_slug)
    branch_categories = Category.objects.filter(url=category_slug).get_descendants(include_self=True)
    products_list = Product.objects.filter(category__in=branch_categories)
    categories = Category.objects.all()
    template = loader.get_template('shop/category.html')
    context = {
        'products_list': products_list,
        'categories': categories,
    }
    return HttpResponse(template.render( context, request))

def show_product(request, product_slug):
    categories = Category.objects.all()
    product = Product.objects.get(slug=product_slug)
    product_balloon = Balloon.objects.get(slug=product_slug)
    # prod1 = product.get_ancestors(asceding=True, include_self=False)
    template_render = "shop/baloon.html"
    # print(categories.filter(name=product.category).get_ancestors(include_self=True)[0].name)

    # if categories.filter(name=product.category).get_ancestors(include_self=True)[0].name == 'Лодки':
    #     product = Boat.objects.get(slug=product_slug)
    #     template_render = "shop/product.html"
    # print("show_product")

    return render(request, template_render, {"product": product,
                                            "product_balloon": product_balloon,
                                            'categories': categories, })