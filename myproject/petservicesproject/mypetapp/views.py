from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Service, User, SPService, cart, Booking, Order, Payment, Orderdetail
from django.db.models import Q  
from django.contrib.auth.hashers import make_password, check_password
from .forms import createform
from django.urls import reverse_lazy
from django.http import JsonResponse
from datetime import date
from petservicesproject import settings
import razorpay


# Create your views here.

# class Serviceview(ListView):
#     model = Service
#     template_name = 'serviceview.html'
#     context_object_name = 'serviceobject'

#     def get_context_data(self, **kwargs):
#         data = self.request.session['sessionvalue']
#         context = super().get_context_data(**kwargs)
#         context['session'] = data
#         return context

class Serviceview(ListView):
    model = SPService
    template_name = 'serviceview.html'
    context_object_name = 'serviceobject'

    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context

class SPServiceList(ListView):
    model = SPService
    template_name = 'spservicelist.html'
    context_object_name = 'spserviceobject'

    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context

def filterservicebylocation(request, location):    
    serviceobjbylocation = SPService.cspserviceobj.filterdata(location)
    return render(request,'serviceview.html',{'serviceobject':serviceobjbylocation}) 

def search(request):
    if request.method == "POST":
        searchdata = request.POST.get('searchquery')
        serviceobject = SPService.objects.filter(Q(name__icontains =searchdata)|Q(description__icontains=searchdata))
        return render(request, 'serviceview.html', {'serviceobject': serviceobject})

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        epassword = make_password(password)
        usertype = request.POST.get('usertype')
        address_line1 = request.POST.get('address1')
        address_line2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        contact = request.POST.get('contact')
        userobject = User(name=name, email=email, password=epassword, usertype=usertype, address_line1=address_line1, address_line2=address_line2, city=city, state=state, pincode=pincode, contact=contact)
        print(userobject)
        userobject.save()
        return redirect('../login/')
    


def home(request):
    return render(request, 'home.html')

def aboutus(request):
    return render(request, 'aboutus.html')
    
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        print(username, password)
        user = User.objects.filter(email = username)
        print("user: ", user)
        if user:
            userobject = User.objects.get(email = username)
            print("userobject: ", userobject)
            flag = check_password(password, userobject.password)
            print("flag", flag)
            if flag:
                request.session['sessionvalue'] = userobject.email
                usertype = userobject.usertype
                username = userobject.name
                if usertype == 'pet parent':
                    return redirect('../serviceview/')
                    # return render(request, 'beforeserviceview.html')
                else:
                    print('in else of flag')
                    spobj = SPService.objects.all()
                    # return render(request, 'spservicelist.html', {'spserviceobject':spobj, 'userobj': userobject})
                    return redirect('../spservicelist/')
            else:
                return render(request, 'login.html', {'message':'Incorrect username or password!'})
        else:
            return render(request, 'login.html', {'message':'Incorrect username or password!'})

# service provider service object class based views


class SPcreateservice(CreateView):
    model = SPService
    form_class = createform
    template_name = "spcreateservice.html"
    success_url = reverse_lazy('spservicelist')


class SPupdateservice(UpdateView):
    model = SPService
    form_class = createform
    template_name = 'spupdateservice.html'
    success_url = reverse_lazy('spservicelist')

class SPdetailservice(DetailView):
    model = SPService
    template_name = 'spservicedetail.html'
    context_object_name = 'i'

class SPdeleteservice(DeleteView):
    model = SPService
    template_name = 'spdeleteservice.html'
    success_url = reverse_lazy('spservicelist')

class SPRequestList(ListView):
    model = cart
    template_name = 'sprequestlist.html'
    context_object_name = 'cartobj'

    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(SPRequestList, self).get_context_data(**kwargs)
    #     context['spserviceobj'] = SPService.objects.all()
    #     return context
    

# service provider service object class based views end

class Servicedetail(DetailView):
    model = SPService
    template_name = 'details.html'
    context_object_name = 'i'
    
    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context

def addtocart(request):
    serviceid = request.POST.get("serviceid")
    usersession = request.session['sessionvalue']  # email of user
    date = request.POST.get('servicedate')
    time = request.POST.get('servicetime')
    userobj = User.objects.get(email = usersession) #fetch record from database table using email from session
    serviceobj = SPService.objects.get(id = serviceid)

    flag = cart.objects.filter(user_id = userobj.id, service_id = serviceobj.id)
    if flag:
        cartobj = cart.objects.get(user_id = userobj.id, service_id = serviceobj.id)    
        cartobj.date = date
        cartobj.time = time    
        cartobj.totalamount = serviceobj.price  
        cartobj.save()
    else:
        cartobj = cart(user_id = userobj, service_id = serviceobj, service_date = date, service_time = time, totalamount = serviceobj.price)
        cartobj.save()
    
    return redirect('../serviceview/')

def viewcart(request):   
    usersession = request.session['sessionvalue']  # email of user    
    userobj = User.objects.get(email = usersession)
    cartobj = cart.objects.filter(user_id = userobj.id)

    return render(request, 'cart.html', {'cartobj': cartobj, 'session': usersession})    

def removefromcart(request):
    useremail = request.session['sessionvalue']
    serviceid = request.POST.get('service_id')
    print(serviceid)
    userobj = User.objects.get(email = useremail)
    serviceobj = SPService.objects.get(id = serviceid)
    cartobj = cart.objects.get(user_id = userobj.id, service_id = serviceobj.id)

    if cartobj:
        cartobj.delete()
    return redirect('../viewcart/')

def summary(request):
    usersession = request.session['sessionvalue'] 
    userobj = User.objects.get(email = usersession)
    cartobj = cart.objects.filter(user_id = userobj.id, status = 'accepted')

    totalbill = 0
    count = 0
    for i in cartobj:
        totalbill = totalbill + i.totalamount
        count = count + 1    
    return render(request, 'summary.html' , {'session': usersession, 'totalbill': totalbill, 'cartobj': cartobj, 'count': count})


def payment(request):
    firstname = request.POST.get('fn')
    lastname = request.POST.get('ln')
    address = request.POST.get('address')
    state = request.POST.get('state')
    city = request.POST.get('city')
    pincode = request.POST.get('pin')
    phonenumber = request.POST.get('phone')
    datevar = date.today()
    orderobj = Order(firstname=firstname, lastname=lastname, address = address, state=state, city=city, pincode=pincode, phonenumber=phonenumber, orderdate=datevar, orderstatus = 'pending')
    orderobj.save()

    orderno = str(orderobj.id)+str(datevar).replace('-','')
    orderobj.ordernumber = orderno
    orderobj.save()
    print('orderobj: ', orderobj) 

    usersession = request.session['sessionvalue'] 
    print('usersession: ', usersession)
    userobj = User.objects.get(email = usersession)
    username = userobj.name
    cartobj = cart.objects.filter(user_id = userobj.id, status = 'accepted')
    print('cartobj: ', cartobj)

    totalbill = 0
    count = 0
    for i in cartobj:
        totalbill = totalbill + i.totalamount
        count = count + 1
            
    from django.core.mail import EmailMessage
    sm = EmailMessage('Order placed', 'Your order from the pet store app has been placed, total bill is '+str(totalbill), to=['samruddhiaware@gmail.com'])
    sm.send()

    # authorize razorpay client with API Keys.
    razorpay_client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 

    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '../serviceview'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    print("context: ", context)

    return render(request, 'payment.html', {'orderobj': orderobj, 'session': usersession, 'cartobj': cartobj, 'totalbill': totalbill, 'context':context, 'firstname': firstname,})


def paymentsuccess(request):
    orderno = request.GET.get('order_id')
    tid = request.GET.get('payment_id')
    print('orderid: ', orderno)
    print('tid: ', tid)
    usersession = request.session['sessionvalue'] 
    print('usersession: ', usersession)
    userobj = User.objects.get(email = usersession)
    print('userobj: ', userobj)
    cartobj = cart.objects.filter(user_id = userobj.id)
    print('cartobj: ', cartobj)
    orderobj = Order.objects.get(ordernumber = orderno)
    print('orderobj: ', orderobj)   

    paymentobj = Payment(userid = userobj, orderid = orderobj, paymentmode = 'razorpay', paymentstatus='paid', transactionid = tid)
    paymentobj.save() 
    print('paymentobj: ', paymentobj)

    for i in cartobj:
        orderdetailobj = Orderdetail(ordernumber = orderno, userid = userobj, serviceid=i.service_id, totalprice=i.totalamount,  paymentid=paymentobj)
        orderdetailobj.save()  
        print('orderdetailobj: ', orderdetailobj)
        i.delete()

    return render(request, 'paymentsuccess.html', {'orderdetailobj': orderdetailobj, 'paymentobj': paymentobj, 'session': usersession})

# def booking(request):   
    usersession = request.session['sessionvalue']  # email of user    
    userobj = User.objects.get(email = usersession)
    cartobj = cart.objects.filter(user_id = userobj.id) 
    for i in cartobj:
        bookingobj = Booking(cart_id = i)    
        bookingobj.save()   

    totalbill = 0
    count = 0
    for i in cartobj:
        totalbill = totalbill + i.totalamount
        count = count + 1 
        datevar = date.today()
        bookingno = str(bookingobj.id)+str(datevar).replace('-','')
        bookingobj.booking_number = bookingno
        bookingobj.save()             
    
    # if bookingobj:
    #     if bookingobj.booking_status == 'pending':
    #         return render(request, 'booking.html', {'message':'Your booking request is sent to service provider, expect response in an hour'})  
    #     elif bookingobj.booking_status == 'rejected':
    #         return render(request, 'booking.html', {'message':'The service is unavailable at the moment, please try booking another one. We regret the inconvinience'})
    #     else:
    #         return render(request, 'booking.html', {'bookingobj': bookingobj, 'session': usersession, 'cartobj': cartobj, 'totalbill': totalbill})
    # else:
    #     return render(request, 'booking.html', {'message':'Please book a service to proceed'})    
    return render(request, 'booking.html', {'bookingobj': bookingobj, 'session': usersession, 'cartobj': cartobj, 'totalbill': totalbill})
    
def spbookingdecision(request):
    bookingno = request.POST.get('bookingno')
    print(bookingno)
    bookingobj = Booking.objects.filter(booking_number = bookingno)
    print(bookingobj)

    for i in bookingobj:
        if request.POST.get('bookingdecision') == 'accept':
            i.booking_status = 'accepted'
            i.save()
        else:
            i.booking_status = 'rejected'
            i.save()

    return render(request, 'feedback.html', {'bookingobj': bookingobj})

def accept(request):
    usersession = request.session['sessionvalue']     
    userobj = User.objects.get(email = usersession)   
    service_id = request.POST.get('service_id')    
    cartobj = cart.objects.get(service_id = service_id)   

    if cartobj:
        cartobj.status = 'accepted'        
        cartobj.save()

    return redirect('../sprequestlist/')

def reject(request):
    usersession = request.session['sessionvalue']     
    userobj = User.objects.get(email = usersession)   
    service_id = request.POST.get('service_id')    
    cartobj = cart.objects.get(service_id = service_id)   

    if cartobj:
        cartobj.status = 'rejected'        
        cartobj.save()

    return redirect('../sprequestlist/')




def logout(request):
    del(request.session['sessionvalue'])
    return redirect('../login/')


