from django.shortcuts import render, redirect
from django.db.models import Q

# Create your views here.

from product.models import ProductBrand, BrandModel, ProductCategory, ProductCategoryParent, ProductCategoryChild, ProductColor, ProductImage, ProductSize, ProductModel, ProductTags
from reviews.models import Review
# Create your models here.

def filter_options(request):
    brands = BrandModel.objects.all().distinct()
    pp = ProductCategoryParent.objects.all().distinct()
    pc = ProductCategoryChild.objects.values('ProductCategoryC').distinct()
    items = ProductModel.objects.all()
    return render(request, 'filter/product_listing.html', {
        'pcp':pp,
        'pcc':pc,
        'brands':brands,
        'items':items,
    }
)

def filter_output(request):
    if request.method == 'POST':
        brand = request.POST.getlist('brand', [])
        categoryC = request.POST.getlist('categoryC', [])
        categoryP = request.POST.getlist('categoryP', [])
        results = ProductModel.objects.all()

        if categoryC:
            results = results.filter(ProductCategoriesChild__ProductCategoryC__in=categoryC).distinct()
        if categoryP:
            results = results.filter(ProductCategoriesParent__ProductCategoryP__in=categoryP).distinct()
        if brand:
            results = results.filter(mark__name__in=brand).distinct()

        item_images = ProductImage.objects.all()
        filter_list = brand + categoryC + categoryP

        query = ", ".join([x for x in filter_list if x])
        brands = BrandModel.objects.all().distinct()
        pp = ProductCategoryParent.objects.all().distinct()
        pc = ProductCategoryChild.objects.values('ProductCategoryC').distinct()

        context = {
        'query': query,
        'items': results,
        'item_images':item_images,
        'pcp':pp,
        'pcc':pc,
        'brands':brands,

        }
        return render(request, 'filter/product_listing.html', context)
    else:
        return redirect('filter:filter_options')

def brand_filter(request, brand):
    results = ProductModel.objects.all()
    if brand:
        results = results.filter(mark__name__in=[brand]).distinct()
    else:
        brand = None
    item_images = ProductImage.objects.all()
    brands = BrandModel.objects.all().distinct()
    pp = ProductCategoryParent.objects.all().distinct()
    pc = ProductCategoryChild.objects.values('ProductCategoryC').distinct()

    context = {
        'query': brand,
        'items': results,
        'item_images':item_images,
        'pcp':pp,
        'pcc':pc,
        'brands':brands,

        }
    return render(request, 'filter/product_listing.html', context)
def Category_filter(request, category):
    results = ProductModel.objects.all()
    print('category ****')
    if category:
        results = results.filter(ProductCategoriesParent__ProductCategoryP__in=[category]).distinct()
    else:
        category = None

    item_images = ProductImage.objects.all()
    brands = BrandModel.objects.all().distinct()
    pp = ProductCategoryParent.objects.all().distinct()
    pc = ProductCategoryChild.objects.values('ProductCategoryC').distinct()

    context = {
        'query': category,
        'items': results,
        'item_images':item_images,
        'pcp':pp,
        'pcc':pc,
        'brands':brands,

        }
    return render(request, 'filter/product_listing.html', context)

def Material_Fabric_filter(request, categoryC):
    results = ProductModel.objects.all()
    print(categoryC)
    if categoryC:
            results = results.filter(ProductCategoriesChild__ProductCategoryC__in=[categoryC]).distinct()
    else:
        categoryC = None

    item_images = ProductImage.objects.all()
    brands = BrandModel.objects.all().distinct()
    pp = ProductCategoryParent.objects.all().distinct()
    pc = ProductCategoryChild.objects.values('ProductCategoryC').distinct()

    context = {
        'query': categoryC,
        'items': results,
        'item_images':item_images,
        'pcp':pp,
        'pcc':pc,
        'brands':brands,

        }
    return render(request, 'filter/product_listing.html', context)

def Discount_filter(request, discount):
    results = ProductModel.objects.all()

    if brand:
        results = results.filter(mark__name__in=brand).distinct()
    else:
        brand = None

    item_images = ProductImage.objects.all()
    brands = BrandModel.objects.all().distinct()
    pp = ProductCategoryParent.objects.all().distinct()
    pc = ProductCategoryChild.objects.values('ProductCategoryC').distinct()

    context = {
        'query': brand,
        'items': results,
        'item_images':item_images,
        'pcp':pp,
        'pcc':pc,
        'brands':brands,

        }
    return render(request, 'filter/product_listing.html', context)

def Rating_filter(request, rate):
    results = ProductModel.objects.all()

    if brand:
        results = results.filter(mark__name__in=brand).distinct()
    else:
        brand = None

    item_images = ProductImage.objects.all()
    brands = BrandModel.objects.all().distinct()
    pp = ProductCategoryParent.objects.all().distinct()
    pc = ProductCategoryChild.objects.values('ProductCategoryC').distinct()

    context = {
        'query': brand,
        'items': results,
        'item_images':item_images,
        'pcp':pp,
        'pcc':pc,
        'brands':brands,

        }
    return render(request, 'filter/product_listing.html', context)

def New_Arrivals_filter(request, new_tag):
    results = ProductModel.objects.all()

    if brand:
        results = results.filter(mark__name__in=brand).distinct()
    else:
        brand = None

    item_images = ProductImage.objects.all()
    brands = BrandModel.objects.all().distinct()
    pp = ProductCategoryParent.objects.all().distinct()
    pc = ProductCategoryChild.objects.values('ProductCategoryC').distinct()

    context = {
        'query': brand,
        'items': results,
        'item_images':item_images,
        'pcp':pp,
        'pcc':pc,
        'brands':brands,

        }
    return render(request, 'filter/product_listing.html', context)
