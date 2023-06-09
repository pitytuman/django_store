from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect
from .forms import ReviewForm
from .models import Product, Category, Subcategory


# Create your views here.


def home_view(request):
    return render(request, "pages/index.html")


def get_paginator(request, queryset):
    paginator = Paginator(queryset, 2)
    page = request.GET.get("page")
    result = paginator.get_page(page)
    return result


def shop_view(request):
    products = Product.objects.all()
    result = get_paginator(request, products)
    context = {
        "products": result
    }
    return render(request, "pages/shop.html", context)

def subcategory_articles_view(request, slug):
    subcategory = Subcategory.objects.get(slug=slug)
    products = Product.objects.filter(subcategory=subcategory)
    result = get_paginator(request, products)
    context = {
        "products": result
    }
    return render(request, "pages/shop.html", context)


def product_detail_view(request, slug):
    product = Product.objects.get(slug=slug)
    related_products = Product.objects.filter(category=product.category).order_by("?")
    related_products = [item for item in related_products if item.pk != product.pk]

    if request.method == "POST":
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.product = product
            form.save()
            return redirect("product_detail", product.slug)
    else:
        form = ReviewForm()

    reviews = product.reviews.all()
    context = {
        "product_detail": product,
        "related_products": related_products[:4],
        "form": form,
        "reviews": reviews,
    }
    return render(request, "pages/product_detail.html", context)
