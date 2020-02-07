from django.forms import ModelForm
from .models import Item , Student , Cart 

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
class SignInForm(ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number','password']