from django.shortcuts import render ,get_object_or_404
from django.template import loader
from django.http import HttpResponse ,HttpResponseRedirect
from .models import Item, Student ,Cart
from django.views import generic
from .forms import StudentForm , SignInForm
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'colx/index.html'
    context_object_name = 'items'
    def get_queryset(self):
        """Return the items not sold."""
        return Item.objects.filter(status='not sold')
def cart(request):
	try:
		roll_number=request.session['roll_number']
		student=Student.objects.get(roll_number=roll_number)
		items=Cart.objects.filter(studentroll=student)
		return render(request,"colx/cart.html",{'items':items})
	except Exception as e:
		messages.error(request,"No Item in Cart" +str(e) )
		return HttpResponseRedirect(reverse('colx:index'))

def buy(request,item_no):
	try:
		roll_number=request.session['roll_number']
		item=Item.objects.get(item_no=item_no)
		return render(request,'colx/buy.html',{'item':item})
	except KeyError:
		err="You need to login first"
		form=SignInForm
		return render(request,'colx/login2.html',{'form': form,'err':err})
def add_to_cart(request,item_no):
	try:
		roll_number=request.session['roll_number']
		item=Item.objects.get(item_no=item_no)

		student=Student.objects.get(roll_number=roll_number)
		cart=Cart(itemitem_no=item,studentroll=student)
		cart.save()
		messages.success(request,item.item_name+" Added To Cart")
		return HttpResponseRedirect(reverse('colx:index'))
	except KeyError:
		err="You need to login first"
		form=SignInForm()
		return render(request,'colx/login2.html',{'form': form,'err':err})

def login(request):
	form=SignInForm()
	err=""
	if(request.method =='POST'):
		form=SignInForm(request.POST)
		password=request.POST['password']
		roll_number=request.POST['roll_number']
		try:
			user=Student.objects.get(roll_number=roll_number)
			#request.session['id']=user.id
		except:
			err="No user exist with this roll number"
		else:
			if(user.password==password):
				request.session['roll_number']=user.roll_number
				request.session['id']=user.id
				return HttpResponseRedirect(reverse('colx:index'))
			else:
				err="Password is incorrect"	
	return render(request,'colx/login2.html',{'form': form,'err':err})
def logout(request):
	try:
		del request.session['id']
		del request.session['roll_number']
	except KeyError:
		pass
	return HttpResponseRedirect(reverse('colx:index'))
def signup(request):
	form=StudentForm()
	err=""
	if(request.method =='POST'):
		form=StudentForm(request.POST)
		if(form.is_valid()):
			fname=form.cleaned_data['fname']
			lname=form.cleaned_data['lname']
			roll=form.cleaned_data['roll_number']
			year=form.cleaned_data['year']
			clas=form.cleaned_data['class_field']
			section=form.cleaned_data['section']
			pwd=form.cleaned_data['password']
			mob=form.cleaned_data['mobile_no']
			email=form.cleaned_data['email']
			try:
				user=Student(fname=fname,lname=lname,roll_number=roll,year=year,class_field=clas,section=section,password=pwd,mobile_no=mob,email=email)
				user.save()

			except:
				err="user already exists"
				return render(request,'colx/signup.html',{'form': form,'err':err})
			else:
				request.session['roll_number']=user.roll_number
				request.session['id']=user.id
				return HttpResponseRedirect(reverse('colx:index'))
		else:
			return render(request,'colx/signup.html',{'form': form,'err':err})
	else:
		return render(request,'colx/signup.html',{'form': form,'err':err})
def sell(request):
	try:
		seller_obj=Student.objects.get(id=request.session["id"])
	except KeyError:
		err="You need to login first to Sell any item"
		form=SignInForm()
		return render(request,'colx/login2.html',{'form': form,'err':err})
	else:
		if(request.method=='POST'):
			img=request.FILES['img']
			item_name=request.POST['item_name']
			price=request.POST['price']
			description=request.POST['description']
			fs = FileSystemStorage()
			filename=fs.save(item_name+seller_obj.roll_number,img)
			uploaded_file_url = fs.url(filename)
			seller_obj=Student.objects.get(id=request.session["id"])
			item=Item(item_name=item_name,price=price,img=uploaded_file_url,status='not sold',description=description,seller=seller_obj)
			item.save()
			return HttpResponseRedirect(reverse('colx:index'))
		return render(request,'colx/sell.html')
