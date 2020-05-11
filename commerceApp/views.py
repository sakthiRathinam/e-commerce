from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from django.contrib import messages
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	data=Product.objects.all()
	paginator=Paginator(data,6)
	page=request.GET.get('page')
	try:
		posts=paginator.page(page)
	except PageNotAnInteger:
		posts=paginator.page(1)
	except EmptyPage:
		posts=paginator.page(paginator.num_pages)
	context = {'page':page,'posts':posts, 'cartItems':cartItems}
	return render(request, 'store.html', context)
def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)
def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was added', safe=False)
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)
	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	if total == order.get_cart_total:
		order.complete = True
	order.save()
	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)
	return JsonResponse('Payment submitted..', safe=False)
def registerPage(request):
	form=UserForm()
	if request.method=='POST':
		form=UserForm(request.POST)
		if form.is_valid():
			user=form.save()
			username=form.cleaned_data.get('username')
			messages.success(request,"Account was created successfully" + username)
			return redirect('login')
	context={'form':form}
	return render(request,'register.html',context)
def loginPage(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('customerCreate')
		else:
			messages.info(request,'Username or password is incorrect')
	context={}
	return render(request,'login.html',context)
def logoutUser(request):
	logout(request)
	return redirect('login')
def customerCreate(request):
	form=CustomerForm()
	if request.method=="POST":
		form=CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('store')
	context={'form':form}
	return render(request,'customer.html',context)
def profileSettings(request):
	customer=request.user.customer
	form=UpdateForm(instance=customer)
	if request.method=='POST':
		form=UpdateForm(request.POST,request.FILES,instance=customer)
		if form.is_valid():
			form.save()
	context={'form':form}
	return render(request,'settings.html',context)
def productss(request):
	
	return render(request,'html/products1.html',context)