from math import prod
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from store.models import Cart, Order, Product


# Create your views here.
def index(request):

    if request.method == 'POST':
        productName = request.POST.get('productName') 
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        peremption_date = request.POST.get('peremptionDate')
        description = request.POST.get('description')
        Product.objects.create(name = productName,
                                slug = productName.lower(),
                                price = price, 
                                quantity = quantity, 
                                peremption_date = peremption_date, 
                                description = description)


    products = Product.objects.all()


    return render(request, 'store/index.html', context={"products": products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/detail.html', context={"product": product})

def add_to_cart(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    cart, _ = Cart.objects.get_or_create(user=user) # _ variables qu'on utilisera pas (convention) (sera à 1 si le Cart est créé)
    order, created = Order.objects.get_or_create(user=user,
                                                 ordered=False,
                                                 product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse("product", kwargs={"id": id}))

def cart(request):
    cart = get_object_or_404(Cart, user=request.user)

    return render(request, 'store/cart.html', context={"orders": cart.orders.all()})

def delete_cart(request):
    if cart := request.user.cart: # = cart = request.user.cart      if cart:
        cart.delete()

    return redirect('index')

def confirm_cart(request):
    ...


def delete_product(request, id):
    if product := get_object_or_404(Product, id=id):
        product.delete()

    return redirect('index')


def modify_product(request, id):
    product = get_object_or_404(Product, id=id)


    if request.method == 'POST':
        product.name = request.POST.get('productName') 
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.peremption_date = request.POST.get('peremptionDate')
        product.description = request.POST.get('description')
        product.save()
        return redirect(reverse("product", kwargs={"id": id}))

    return render(request, 'store/modifyProduct.html', context={"product": product})
