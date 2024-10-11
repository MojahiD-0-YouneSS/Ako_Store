from django.shortcuts import render

# Create your views here.
'''@login_required    
def ProductLister(request): 
    item = ProductModel.objects.all()
    return render(request, 'item/itemlist.html',{
        'items':item
    })
    
@login_required
def EditProduct(request, pk):
    item = get_object_or_404(ProductModel, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            
            return redirect('item:detail', pk=item.id)
    else:
        form = EditProductForm(instance=item)
    return render(request, 'item/form.html', {
        'form':form,
        'title':'Edit Product',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(ProductModel, pk=pk, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')

def browse(request): 
    return render(request, 'product/products.html')

def image_gallery(request):
    images = ProductImage.objects.all()  # Assuming Image is your model for storing images
    return render(request, 'image_gallery.html', {'images': images})

'''