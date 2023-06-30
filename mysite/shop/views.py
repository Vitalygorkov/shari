from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Category, Product, Balloon
from django.core.paginator import Paginator


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    products_list = Balloon.objects.all()
    categories = Category.objects.all()
    categories1 = Category.objects.filter(parent='1')
    categories2 = Category.objects.filter(parent='2')
    template = loader.get_template('shop/index.html')
    context = {
        'products_list': products_list,
        'categories': categories,
        'categories1': categories1,
        'categories2': categories2,
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

# def blog(request):
#     post_list = Post.objects.all()
#     categories = Category.objects.all()
#     template = loader.get_template('shop/blog.html')
#     context = {
#         'post_list': post_list,
#         'categories': categories,
#     }
#     return HttpResponse(template.render( context, request))

def post(request, post_slug):
    print('Вьюха постов')
    print(post_slug)
    post = Post.objects.get(slug=post_slug)
    # post_list = Post.objects.all()
    categories = Category.objects.all()
    template = loader.get_template('shop/post.html')
    context = {
        'post': post,
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
    context = {
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

    context = {
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

    return render(request, template_render, {"product_balloon": product_balloon,
                                             "last_category": last_category,
                                            'categories': categories, })