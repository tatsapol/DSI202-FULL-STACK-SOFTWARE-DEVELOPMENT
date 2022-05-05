from pyexpat import model
from django.shortcuts import render
from matplotlib import image
from matplotlib.style import context
from myapp.forms import ProfileForm
from django.http import HttpResponse
import datetime
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from myapp.models import Item, Order_Item, Profile, Record_Order
from django.shortcuts import get_object_or_404, redirect
import json 
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash



data =[]
@login_required(login_url='/accounts/login/') 
def profile(request):
#    Profile = Profile.objects.filter(name=name)
    instance = get_object_or_404(Profile, user=request.user)
    form = ProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('home')
    else:
        context = {
            'form':form,
            'user':request.user
        }
    return render(request, 'profile.html', context)


class ItemListView(ListView):
    model = Item
    paginate_by = 16
    #queryset=Student.objects.filter(type='mountain')
    template_name = 'item_list.html'

class RecordListView(ListView):
    model = Record_Order
    paginate_by = 100
    #queryset=Student.objects.filter(type='mountain')
    template_name = 'record.html'

def product_detail(request, id = None):
    items = get_object_or_404(Item, id=id)
    return render(request, 'detail.html', context={'Item_detail': items})


def About(request):
    return render(request,'about.html')

def Pay(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        order_items = Order_Item.objects.filter(profile=profile)
        #
        if request.POST.get("checkout"):
            print("checkout")
            for order_item in order_items:
                order_item.delete()
            return redirect('home')
        return render(request, 'pay.html', {'order_items': order_items})
    else:
        return redirect('home')



def Logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

@login_required(login_url='/accounts/login/') 
def add_to_cart(request):
    global data
    title = request.POST.get("title")
    order = Order_Item.objects.create(profile=Profile.objects.get(user=request.user),
    item=Item.objects.get(title=title) ,quantity=1)
    rec = Record_Order.objects.create(profile=Profile.objects.get(user=request.user),
    item=Item.objects.get(title=title) ,quantity=1)
 
    myitem={
        "title": title,
        "quantity": 1
        }
    data += [myitem,]
    dictionary = {"data": data}
    json_object = json.dumps(dictionary, indent = 4)
    
    
    response = redirect('home')
    response.set_cookie('cart', json_object)
    return response

def cart_list(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        order_items = Order_Item.objects.filter(profile=profile)
        #
        if request.POST.get("checkout"):
            print("checkout")
            for order_item in order_items:
                order_item.delete()
            return redirect('home')
        return render(request, 'realcart.html', {'order_items': order_items})
    else:
        return redirect('home')

from django.http import HttpResponse
from PIL import Image
import libscrc
import qrcode

def calculate_crc(code):
    crc = libscrc.ccitt_false(str.encode(code))
    crc = str(hex(crc))
    crc = crc[2:].upper()
    return crc.rjust(4, '0')

def gen_code(mobile="", nid="", amount=1.23):
    code="00020101021153037645802TH29370016A000000677010111"
    if mobile:
        tag,value = 1,"0066"+mobile[1:]
        seller='{:02d}{:02d}{}'.format(tag,len(value), value)
    elif nid:
        tag,value = 2,nid
        seller='{:02d}{:02d}{}'.format(tag,len(value), value)
    else:
        raise Exception("Error: gen_code() does not get seller mandatory details")
    code+=seller
    tag,value = 54, '{:.2f}'.format(amount)
    code+='{:02d}{:02d}{}'.format(tag,len(value), value)
    code+='6304'
    code+=calculate_crc(code)
    return code

def get_qr(request,mobile="",nid="",amount=""):
    message="mobile: %s, nid: %s, amount: %s"%(mobile,nid,amount)
    print( message )
    code=gen_code(mobile=mobile, amount=float(amount))#scb
    print(code)
    img = qrcode.make(code,box_size=4)
    response = HttpResponse(content_type='image/png')
    img.save(response, "PNG")
    return response


#def checkout(request):
#    context={
#        "mobile":"0826639206", #seller's mobile
#        "amount": 2.81619
#    }
#    return render(request, 'checkout.html', context)
#def add_to_cart(request):
#    global data , sum
#    title = request.POST.get("title")
#    user = request.user.username
#    order = Order_Item.objects.create(profile=Profile.objects.get(user=request.user),
#    item=Item.objects.get(title=title) ,quantity=1)
 #   sum += int(order.item.unit_price)
  #  myitem={
   #     "user": user,
    #    "title": title,
     #   "quantity": 1,
      #  "sum": sum,
       # }
    #print(sum)
    #data += [myitem,]
    #dictionary = {"data": data}
    #json_object = json.dumps(dictionary)
    #print(json_object)
    
    
    #response = redirect('home')
    #response.set_cookie('cart', json_object)
    #return response



#class cart_list(ListView):
 #   model= Order_Item
  #  paginate_by = 16
   # template_name = 'realcart.html'


# def cart_list(request):
#     if request.COOKIES.get('cart'):
#         cart = json.loads(request.COOKIES.get('cart'))
#         cart_data = cart['data']
#         a = cart_data[0]['pk']
#         return render(request,'realcart.html',{'order_items':a})
#     else:
#         return render(request,'realcart.html')






