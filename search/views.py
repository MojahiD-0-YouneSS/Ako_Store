from django.shortcuts import render, redirect
from product.models import ProductModel, ProductImage, ProductCategory, ProductTags, SearchLabel, ProductSearchLabel
from .forms import SearchForm
from django.db.models import Q

def search_view(request):
    query = request.GET.get('query_name', '')
    size_query = request.GET.get('size', '')
    color_query = request.GET.get('color', '')
    price_query = request.GET.get('price', '')
    mark_query = request.GET.get('mark', '')
    fabric_query = request.GET.get('fabric', '')
    results = ProductModel.objects.all()
    filter_list = [size_query, color_query,  f'{price_query} MAD', mark_query, fabric_query]
    # Apply filters
    if size_query:
        results = results.filter(size__size_value__icontains=size_query).distinct()
    if color_query:
        results = results.filter(colors__name__icontains=color_query).distinct()
    if price_query:
        try:
            min_price, max_price = map(float, price_query.split('-'))
            results = results.filter(ProductPrice__gte=min_price, ProductPrice__lte=max_price).distinct()
        except ValueError:
            # Handle the error if price_query is not in the expected format
            pass
    if mark_query:
        results = results.filter(mark__name__icontains=mark_query)
    '''
    if fabric_query:
        results = results.filter(fabric__icontains=fabric_query).distinct()
    '''
    # Apply query search if no filters are provided
    if not (size_query or color_query or price_query or mark_query or fabric_query) and query:
        results = results.filter(
            Q(ProductName__icontains=query) |
            Q(ProductCategoriesParent__ProductCategoryP__icontains=query) |
            Q(ProductCategoriesChild__ProductCategoryC__icontains=query) |
            # Q(search_tags__icontains=query) |
            Q(ProductTagsList__New__icontains=query) |
            Q(ProductTagsList__Limited__icontains=query) |
            Q(ProductTagsList__Ondemand__icontains=query) |
            Q(ProductTagsList__Viral__icontains=query)
        ).distinct()

    item_images = ProductImage.objects.all()
    if not query:
        query = ", ".join([x for x in filter_list if x])
        
    context = {
        'query': query,
        'items': results,
        'item_images':item_images,
        }
    return render(request, 'search/search.html', context)

def add_search_labels(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            p_number = form.cleaned_data['product_number']
            s_labels = form.cleaned_data['search_lables']
            search_labels_list = [label.strip() for label in s_labels.split(',')]
            product = ProductModel.objects.get(reference_number=p_number)
            
            for name in search_labels_list:
                search_label, created = SearchLabel.objects.get_or_create(name=name)
                ProductSearchLabel.objects.create(search_label=search_label, product=product)
            return redirect('search:add_label')
    else:
        form = SearchForm()
    
    context = {
        'form': form
    }
    return render(request, 'search/add_label.html', context)
