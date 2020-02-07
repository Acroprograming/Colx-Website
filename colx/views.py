from django.shortcuts import render ,get_object_or_404
from django.template import loader
from django.http import HttpResponse ,HttpResponseRedirect
from .models import Item, Student
from django.views import generic
from .forms import StudentForm , SignInForm
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'colx/index.html'
    context_object_name = 'items'
    def get_queryset(self):
        """Return the items not sold."""
        return Item.objects.filter(status='not sold')
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
				request.session['id']=user.id
				return HttpResponseRedirect(reverse('colx:index'))
			else:
				err="Password is incorrect"	
	return render(request,'colx/login2.html',{'form': form,'err':err})
def logout(request):
	try:
		del request.session['id']
	except KeyError:
		pass
	return HttpResponseRedirect(reverse('colx:index'))
def signup(request):
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
			student=Student(fname=fname,lname=lname,roll_number=roll,year=year,class_field=clas,section=section,password=pwd,mobile_no=mob,email=email)
			student.save()
			return HttpResponseRedirect(reverse('colx:index'))
		else:
			return HttpResponse(form.errors.as_data())
	else:
		return render(request,'colx/signup.html',{'form': StudentForm})
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
			filename=fs.save(img.name,img)
			uploaded_file_url = fs.url(filename)
			seller_obj=Student.objects.get(id=request.session["id"])
			item=Item(item_name=item_name,price=price,img=uploaded_file_url,status='not sold',description=description,seller=seller_obj)
			item.save()
			return HttpResponseRedirect(reverse('colx:index'))
		return render(request,'colx/sell.html')
