from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from app.models import slider, banner_area, Main_Category, Product, Category, Coupon_Code
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.db.models import Max, Min, Sum
from django.contrib import messages


# Create your views here.

def base(request):
    return render(request, "base.html")


def home(request):
    sliders = slider.objects.all().order_by('-id')
    banner = banner_area.objects.all().order_by('-id')

    main_category = Main_Category.objects.all()
    product = Product.objects.filter(section__name="Top Deals of The Day")
    best_seller = Product.objects.filter(section__name="Best Seller")
    recommended_for_you = Product.objects.filter(section__name="Recommended For You")
    top_featured_products_main = Product.objects.filter(section__name="Top Featured Products Main")
    top_featured_products = Product.objects.filter(section__name="Top Featured Products")
    context = {
        'sliders': sliders,
        'banner': banner,
        'main_category': main_category,
        'product': product,
        'best_seller': best_seller,
        'recommended_for_you': recommended_for_you,
        'top_featured_product_main': top_featured_products_main,
        'top_featured_product': top_featured_products,
    }
    return render(request, 'main/home.html', context)


def PRODUCT_DETAILS(request, slug):
    product = Product.objects.filter(slug=slug)
    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('404')

    context = {
        'product': product,
    }
    return render(request, 'product/product_deatil.html', context)


def Error404(request):
    return render(request, 'errors/404.html')


def MY_ACCOUNT(request):
    return render(request, 'Account/my-account.html')


def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'username is already exists')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'email id are already exists')
            return redirect('login')

        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')


def LOGIN(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email and Password are Invalid!')
            return redirect('login')


@login_required(login_url='/accounts/login/')
def PROFILE(request):
    return render(request, 'profile/profile.html')


@login_required(login_url='/accounts/login/')
def PROFILE_UPDATE(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        messages.success(request, 'Your Profile Are Successfully Updated')
    return redirect('profile')


def ABOUT(request):
    return render(request, 'main/about.html')


def CONTACT(request):
    return render(request, 'main/contact.html')


def PRODUCT(request):
    category = Category.objects.all()
    product = Product.objects.all()
    context = {
        'category': category,
        'product': product,
    }
    return render(request, 'product/product.html', context)


# cart_pre-define_pages
@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)

    coupon = None
    valid_coupon = None
    invalid_coupon = None
    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon_Code.objects.get(code=coupon_code)
                valid_coupon = "Are Applicable on Current Order !"
            except:
                invalid_coupon = "Your Coupon Code Are Invalid !"

    context = {
        'packing_cost': packing_cost,
        'tax': tax,
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
    }

    return render(request, 'cart/cart.html', context)





