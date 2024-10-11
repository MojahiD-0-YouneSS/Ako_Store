from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ClientForm, NonRegesteredClientForm
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from reviews.models import BannedUser, BannedNonUser
from .models import Client, NonRegesteredClient
from django.contrib.auth.models import User
# Create your views here.
def client_email_handler():
    #Client.objects.all().delete()
    users = User.objects.all().exclude(username='ILiac_Ak0')
    for user in users:
        Client.objects.get_or_create(email = user.email)
    return True

@login_required
def Client_data_hundler(request):
    if request.method == 'POST':
        ClientDataForm = ClientForm(request.POST)
        if ClientDataForm.is_valid():
            new_email = ClientDataForm.cleaned_data['new_email']
            with transaction.atomic():
                try:
                    if new_email:
                        existing_user = Client.objects.get(email=new_email)
                        if existing_user:
                            existing_user.full_name = ClientDataForm.cleaned_data['full_name']
                            existing_user.phone = ClientDataForm.cleaned_data['phone']
                            existing_user.city = ClientDataForm.cleaned_data['city']
                            existing_user.address = ClientDataForm.cleaned_data['address']
                            existing_user.save()                
                    else:
                        existing_user = Client.objects.get(email=request.user.email)
                        if existing_user:
                            existing_user.full_name = ClientDataForm.cleaned_data['full_name']
                            existing_user.phone = ClientDataForm.cleaned_data['phone']
                            existing_user.city = ClientDataForm.cleaned_data['city']
                            existing_user.address = ClientDataForm.cleaned_data['address']
                            existing_user.save()
                except:
                    ClientDataForm.save()
            url = "/checkout/checkout/"
            success_url = f"{reverse('core:success')}?redirect_url={url}"
            return redirect(success_url)
    else:
        regestred_user = Client.objects.values_list('email')
        print(list(regestred_user))
        print(request.user.email)
        ClientDataForm = ClientForm()
    return render(request, 'client/client_data.html', {
        'clientForm':ClientDataForm,
    })

def Non_Regestred_Client_data_hundler(request):
    if request.method == 'POST':
        noneRgestredClientDataForm = NonRegesteredClientForm(request.POST)
        if noneRgestredClientDataForm.is_valid():
            noneRgestredClientDataForm.save()
            name = noneRgestredClientDataForm.cleaned_data['full_name']
            request.session['user_name'] = name
            url = reverse('cart:create_temp_cart', kwargs={'known_client':name})
            success_url = f"{reverse('core:success')}?redirect_url={url}"
            return redirect(success_url)
    else:
        noneRgestredClientDataForm = NonRegesteredClientForm()
    return render(request, 'client/non_client_data.html', {
        'noneRgestredClientDataForm':noneRgestredClientDataForm,
    })

@login_required
def Client_Profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:    
        user_profile = get_object_or_404(Client, email=user.email)
        return render(request, 'client/profile.html', {'user':user, 'user_profile':user_profile})
    except:
        return render(request, 'client/profile.html', {'user':user, 'user_profile':0})

@login_required
def ban_non_client(request, user_id):
    client = get_object_or_404(NonRegesteredClient, id=user_id)
    client.is_active = False
    client.save()
    banned_user, created = BannedNonUser.objects.get_or_create(user=client)
    if not created:
        banned_user.unbanned = False
        banned_user.save()
    messages.success(request, f'User {client.full_name} has been banned.')
    return redirect('shop:non_users')

@login_required
def unban_non_user(request, user_id):
    client = get_object_or_404(NonRegesteredClient, id=user_id)
    client.is_active = True
    client.save()
    banned_user = get_object_or_404(BannedNonUser, user=client)
    banned_user.unbanned = True
    banned_user.save()
    messages.success(request, f'User {client.full_name} has been banned.')
    return redirect('shop:banned_non_user')

@login_required
def ban_client(request, user_name):
    client = get_object_or_404(User, username=user_name)
    client.is_active = False
    client.save()
    
    banned_user, created = BannedUser.objects.get_or_create(user=client)
    if not created:
        banned_user.unbanned = False
        banned_user.save()
    messages.success(request, f'User {client.username} has been banned.')
    return redirect('shop:regestred_clients')

@login_required
def unban_user(request, user_name):
    client = get_object_or_404(User, username=user_name)
    client.is_active = True
    client.save()
    banned_user = get_object_or_404(BannedUser, user=client)
    banned_user.unbanned = True
    banned_user.save()
    messages.success(request, f'User {client.username} has been banned.')
    return redirect('shop:banned_user')
