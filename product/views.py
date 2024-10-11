from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductModelForm, ProductImageForm, ProductFabricForm, ProductCategoryPForm, ProductCategoryCForm, ProductTagsForm, EditProductForm, That_One_Product_Form, ProductColorForm, ProductSizeForm, Color_Size_Adder_Form, BrandForm
from .models import SearchLabel, ProductSearchLabel, ProductModel, ProductImage, ColorSizePointer, ProductTags, SIZE, Color, ProductSize, ProductColor, ProductColorSize, ProductCategory, Tags, ProductCategoryChild, ProductCategoryParent, BrandModel, ProductBrand, FabricModel, ProductFabric
from search.forms import SearchForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q, Subquery, OuterRef
import random
import string
from cart.forms import CartQuantityForm
import json

def ProductInfos(request, product_form, categoryP_form, categoryC_form, tags_form):
    forms_dict = {
        'product_form': product_form,
        'categoryC_form': categoryC_form,
        'categoryP_form': categoryP_form,
        'tags_form': tags_form,
    }

    all_valid = True
    for form_name, form in forms_dict.items():
        if not form.is_valid():
            all_valid = False
            print(f"Form {form_name} is not valid:")
            print(form.errors.as_json())
    
    if all_valid:
        def generate_reference_number():
            characters = string.ascii_letters + string.digits
            reference_number = ''.join(random.choice(characters) for _ in range(20))
            return reference_number

        def is_unique_reference(reference_number):
            return not ProductModel.objects.filter(reference_number=reference_number).exists()

        def generate_and_save_unique_reference(product_form):
            while True:
                reference_number = generate_reference_number()
                if is_unique_reference(reference_number):
            # Assign the generated reference number to the reference_number field of the product_form instance
                    product_form.instance.reference_number = reference_number
            # Save the product_form instance
                    product_form.save()
                    return reference_number
        category_parent = categoryP_form.cleaned_data['category']
        categoryC = categoryC_form.cleaned_data['ProductCategoryC']
        new = tags_form.cleaned_data.get('New')
        limited = tags_form.cleaned_data.get('Limited')
        ondemand = tags_form.cleaned_data.get('Ondemand')
        viral = tags_form.cleaned_data.get('Viral')
        tags, created = Tags.objects.get_or_create(
                New= new,
                Limited= limited,
                Ondemand= ondemand,
                Viral= viral,
         )
        
        reference_number = generate_and_save_unique_reference(product_form)
        product = product_form.save()
        product.reference_number = reference_number
        product.save()
        print(f'{product.ProductName} is saved')
        product_tags, created = ProductTags.objects.get_or_create(product=product, product_tags=tags)
        if created:
            print(f'{product.ProductName} tags are saved')
        category_child = ProductCategoryChild.objects.create(ProductCategoryC=categoryC)
        
        ProductCategory.objects.create(sub_category=category_child, main_category=category_parent, product=product)
        print(f'{product.ProductName}\' categories: "{category_child.ProductCategoryC}" and "{category_parent}" is saved')
        # Assuming 'Product_Image' is the name of the file input field in your form
        print("Data submitted successfully!")
        return product
    else:
        return False
    
@login_required
def add_color_size(request):
    if request.user.username != 'ILiac_Ak0':
        return HttpResponse('Access Denied', status=403)
    if request.method == 'POST':
        add_form = Color_Size_Adder_Form(request.POST)
        color_code = request.POST.get('user_input')
        if add_form.is_valid():
            form_values = add_form.cleaned_data['chain'].split(',')
            action = add_form.cleaned_data['action']
            switcher = add_form.cleaned_data['switcher']
            if action == 'add':
                if switcher == 'color':
                    for color_name in form_values:
                        color_name = color_name.strip()
                        if color_name:  # Ensure the name is not empty
                            Color.objects.create(name=color_name, code=color_code)
                elif switcher == 'size':
                    for size_name in form_values:
                        size_name = size_name.strip()  # Remove leading and trailing whitespace
                        if size_name:  # Ensure the name is not empty
                            SIZE.objects.create(size_value=size_name)
                add_form = Color_Size_Adder_Form()
                return render(request, 'shop/addColorsSize.html', {'form': add_form})
            elif action == 'remove':
                if switcher == 'color':
                    for color_name in form_values:
                        color_name = color_name.strip()  # Remove leading and trailing whitespace
                        if color_name:  # Ensure the name is not empty
                            Color.objects.filter(name=color_name, code=color_code).delete()
                elif switcher == 'size':
                    for size_name in form_values:
                        size_name = size_name.strip()  # Remove leading and trailing whitespace
                        if size_name:  # Ensure the name is not empty
                            SIZE.objects.filter(size_value=size_name).delete()
                add_form = Color_Size_Adder_Form()
                return render(request, 'shop/addColorsSize.html', {'form': add_form})
            else:
                return redirect('product:addProduct')
        else:
            add_form = Color_Size_Adder_Form()
            return render(request, 'shop/addColorsSize.html', {'form': add_form})
    else:
        add_form = Color_Size_Adder_Form()
        return render(request, 'shop/addColorsSize.html', {'form': add_form})

@login_required
def add_features_to_product(request):
    if request.user.username != 'ILiac_Ak0':
        return HttpResponse('Access Denied', status=403)
    if request.method == 'POST':
        color_form = ProductColorForm(request.POST)
        size_form = ProductSizeForm(request.POST)
        sizes_per_color = request.POST.get('size_quantity_input')
        per_color = request.POST.get('color')
        
        that_one_product_form =  That_One_Product_Form(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)
        is_valid, product, (color_form, size_form) = that_one_product_form.process_color_and_size_forms(color_form, size_form)
        if is_valid:
            if color_form.is_valid() and size_form.is_valid():
                color_instance = color_form.save(commit=False)
                size_instance = size_form.save(commit=False)
                color_instance.product = product
                size_instance.product = product
                color_instance.save()
                size_instance.save()
                
                if sizes_per_color:
                    the_color=get_object_or_404(Color, id=per_color)
                    product_color = get_object_or_404(ProductColor, color=the_color, product=product)
                    new_color_size = ColorSizePointer.objects.create(color=the_color, product_color=product_color)
                    size_quantity_dict = json.loads(sizes_per_color)
                    
                    for size, quantity in size_quantity_dict.items():
                # Process the size and quantity data as needed
                        selected_size = get_object_or_404(SIZE, id=size)
                        new_color_size.sizes.add(selected_size)
                        new_color_size.quantities.append(quantity)
                        the_product_size = ProductSize.objects.get_or_create(product=product, size=selected_size, quantity=quantity)
                        ProductColorSize.objects.create(
                            product_color=product_color,
                            product_size=the_product_size,
                            quantity=quantity
                        )
                    new_color_size.save()
                product_images = request.FILES.getlist('Product_Image')
                
                for image in product_images:
                    
                    ProductImage.objects.create(Product=product, Product_Image=image, color=color_instance.color)

                # Redirect or render success message
                color_form = ProductColorForm()
                size_form = ProductSizeForm()
                that_one_product_form =  That_One_Product_Form()
                image_form = ProductImageForm()
                return render(request, 'product/add_to_product.html',  {
                    'color_form': color_form,
                    'size_form': size_form,
                    'that_one_product_form': that_one_product_form,
                    'image_form': image_form, 
                    })
    
            else:
                return render(request, 'product/add_to_product.html', {
                    'color_form': color_form,
                    'size_form': size_form,
                    'that_one_product_form': that_one_product_form,
                    'image_form': image_form, 
                    })
                # Render form with errors
        else:
            # Render form with errors or handle invalid reference number
            return render(request, 'product/add_to_product.html', {
                    'color_form': color_form,
                    'size_form': size_form,
                    'that_one_product_form': that_one_product_form,
                    'image_form': image_form, 
                    })
    else:
        color_form = ProductColorForm()
        size_form = ProductSizeForm()
        that_one_product_form =  That_One_Product_Form()
        image_form = ProductImageForm()  # Correcting how image_form is instantiated
    return render(request, 'product/add_to_product.html',  {
                    'color_form': color_form,
                    'size_form': size_form,
                    'that_one_product_form': that_one_product_form,
                    'image_form': image_form, 
                    })

@login_required
def add_product(request):
    if request.user.username != 'ILiac_Ak0':
        return HttpResponse('Access Denied', status=403)
    if request.method == 'POST':
        product_form = ProductModelForm(request.POST, request.FILES)
        tags_form = ProductTagsForm(request.POST)
        categoryC_form = ProductCategoryCForm(request.POST)
        categoryP_form = ProductCategoryPForm(request.POST)
        if ProductInfos(request, product_form, categoryP_form, categoryC_form ,tags_form):
            return redirect('product:addProduct')
        
    else:
        product_form = ProductModelForm()
        tags_form = ProductTagsForm()
        categoryC_form = ProductCategoryCForm()
        categoryP_form = ProductCategoryPForm()

    return render(request, 'product/add_product.html', {
        'product_form': product_form, 
        'tags_form': tags_form, 
        'categoryC_form': categoryC_form, 
        'categoryP_form': categoryP_form, 
    })
    
def ProductDetail(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    product_color_sizes = ProductColorSize.objects.filter(product_color__product=product)
    product_color = ProductColor.objects.filter(product=product)
    for pc in product_color:
        product_color_size_pointer = ColorSizePointer.objects.get(product_color=pc, color=pc.color)
    # Organize data by color
    color_size_quantity_map = {}
    for pcs in product_color_sizes:
        product = pcs.product_color.product
        color = pcs.product_color.color
        size = pcs.product_size.size
        quantity = pcs.quantity
        product_color_size_pointer = ColorSizePointer.objects.get(product_color=pcs.product_color, color=color)
        if size in product_color_size_pointer.sizes.all():
            if color not in color_size_quantity_map:
                color_size_quantity_map[color] = []
                color_size_quantity_map[color].append({
                'size': size,
                'quantity': quantity
                })
    product_category = get_object_or_404(ProductCategory, product=product)
    related_products = ProductModel.objects.filter(
        ProductCategoriesParent__in=product.ProductCategoriesParent.all(),
    ).exclude(pk=product.pk).distinct()
    product_images = ProductImage.objects.filter(Product=product)
    product_tags = ProductTags.objects.filter(product=product)
    quantity_form = CartQuantityForm()
    
    # Group images by color
    grouped_images = {}
    for color in color_size_quantity_map.keys():
        grouped_images[color.name.replace(' ', '_')] = [image.Product_Image.url for image in product_images if image.color == color]
    
    return render(request, 'product/details.html', {
        'product': product,
        'images': product_images,
        'quantity_form': quantity_form,
        'color_size_quantity_map': color_size_quantity_map,
        'product_tags': product_tags,
        'related_products': related_products,
        'product_category': product_category,
        'grouped_images': grouped_images,
    })
    
def Delete_product(request, id):
    product = ProductModel.objects.filter(id=id)
    product.delete()
    return redirect('core:index')

def brandlister(request):
    brands = BrandModel.objects.all()
    return render(request, 'product/brands.html', {'brands':brands})

def create_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            product = get_object_or_404(ProductModel, reference_number=form.cleaned_data['ref_number'])
            form.save()
            brand = get_object_or_404(BrandModel,name=form.cleaned_data['name'])
            ProductBrand.objects.get_or_create(product=product, brand=brand)

            return redirect('product:add_brand')
    else:
        form = BrandForm()

    return render(request, 'product/create_brand.html', {'form': form})

def add_one_time_product(request):
    if request.method == 'POST':
        brand_form = BrandForm(request.POST, request.FILES)
        fabric_form = ProductFabricForm(request.POST)
        color_form = ProductColorForm(request.POST)
        size_form = ProductSizeForm(request.POST)
        product_form = ProductModelForm(request.POST, request.FILES)
        search_form = SearchForm(request.POST)

        if request.FILES.get('Product_Image'):
            image_form = ProductImageForm(request.POST, request.FILES)
        else:
            image_form = None
        
        tags_form = ProductTagsForm(request.POST)
        categoryC_form = ProductCategoryCForm(request.POST)
        categoryP_form = ProductCategoryPForm(request.POST)
        product = ProductInfos(request, product_form, categoryP_form, categoryC_form, tags_form)
        if all([x.is_valid() for x in [ fabric_form, search_form, color_form, size_form,]]) and product:
            if product:
                name = request.POST.get('name', None)
                brand_Image = request.FILES.get('brand_Image', None)
                if brand_Image:
                    brand, created = BrandModel.objects.get_or_create(name=name)
                    if created:
                        brand.brand_Image = brand_Image
                        brand.save()
                else:
                    brand, created = BrandModel.objects.get_or_create(name=name)

                brand = get_object_or_404(BrandModel, name=name)
                productbrand, created = ProductBrand.objects.get_or_create(product=product, brand=brand)
                if created:
                    print(f'{product.ProductName}\'s brand is added')
                color_instance = color_form.save(commit=False)
                size_instance = size_form.save(commit=False)
                color_instance.product = product
                size_instance.product = product
                color_instance.save()
                size_instance.save()
                if color_instance.color:
                    the_color=get_object_or_404(Color, name=color_instance.color)
                    product_color = get_object_or_404(ProductColor, color=the_color, product=product)
                    new_color_size = ColorSizePointer.objects.create(color=the_color, product_color=product_color)
                    
                    selected_size = get_object_or_404(SIZE, size_value=size_instance.size)
                    new_color_size.sizes.add(selected_size)
                    new_color_size.quantities.append(color_instance.quantity)
                    the_product_size, created = ProductSize.objects.get_or_create(product=product, size=selected_size, quantity=color_instance.quantity)
                    ProductColorSize.objects.create(
                            product_color=product_color,
                            product_size=the_product_size,
                            quantity=color_instance.quantity
                        )
                    new_color_size.save()
                print(f'color and size added !')
                product_images = request.FILES.getlist('Product_Image')
                
                for image in product_images:
                    
                    ProductImage.objects.create(Product=product, Product_Image=image, color=color_instance.color)
                print(f'{product.ProductName}\'s images are added !')
                fabric = fabric_form.cleaned_data['fabric']
                pure = fabric_form.cleaned_data['pure']
                if pure:
                    fabric_obj, created = FabricModel.objects.get_or_create(name=fabric)
                    if created:
                        ProductFabric.objects.create(product=product, pure=pure, fabric=fabric_obj.name)
                        print(f'{product.ProductName}\'s fabric is added !')
                else:
                    fabric_names = []
                    L1_fabric_comb = fabric.split('\n')
                    for x in L1_fabric_comb:
                        try:
                            name = x.split(' ', 1)[1].strip()  # Extract the fabric name
                            fabric_names.append(name)
                        except IndexError:
                            print("Invalid fabric format. Ensure each line follows the format '<percentage> <fabricName>'.")

                    for name in fabric_names:
                        FabricModel.objects.get_or_create(name=name)

                    ProductFabric.objects.create(product=product, pure=pure, fabric=fabric)
                    print(f'{product.ProductName}\'s fabric is added')
                s_labels = search_form.cleaned_data['search_lables']
                search_labels_list = [label.strip() for label in s_labels.split(',')]
            
                for name in search_labels_list:
                    search_label, created = SearchLabel.objects.get_or_create(name=name)
                    ProductSearchLabel.objects.create(search_label=search_label, product=product)
                print('search Label added')
            return redirect('product:detail', pk=product.id)
        else:
            
            print(f'image_form: {image_form.errors}')
            print(f'color_form: {color_form.errors}')
            print(f'size_form: {size_form.errors}')
            print(f'product_form: {product_form.errors}')
            print(f'tags_form: {tags_form.errors}')
            print(f'categoryC_form: {categoryC_form.errors}')
            print(f'categoryP_form: {categoryP_form.errors}')
            print(f'brand_form: {brand_form.errors}')
            print(f'fabric_form: {fabric_form.errors}')
            print(f'search_form: {search_form.errors}')
            context = {
        'color_form' : color_form,
        'size_form' : size_form,
        'product_form' : product_form,
        'tags_form' : tags_form,
        'categoryC_form' : categoryC_form,
        'categoryP_form' : categoryP_form,
        'brand_form' : brand_form,
        'fabric_form' : fabric_form,
        'image_form' : image_form,
        'search_form' : search_form,
            
        }
            return render(request, 'shop/add_one_time.html', context)
    else:
        search_form = SearchForm()
        color_form = ProductColorForm()
        size_form = ProductSizeForm()
        product_form = ProductModelForm()
        tags_form = ProductTagsForm()
        categoryC_form = ProductCategoryCForm()
        categoryP_form = ProductCategoryPForm()
        brand_form = BrandForm()
        fabric_form = ProductFabricForm()
        image_form = ProductImageForm()
        context = {
        'color_form' : color_form,
        'size_form' : size_form,
        'product_form' : product_form,
        'tags_form' : tags_form,
        'categoryC_form' : categoryC_form,
        'categoryP_form' : categoryP_form,
        'brand_form' : brand_form,
        'fabric_form' : fabric_form,
        'image_form' : image_form,
        'search_form' : search_form,
            
        }
        return render(request, 'shop/add_one_time.html', context)