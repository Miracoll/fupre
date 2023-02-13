from django import forms
from .models import Personal,NOK

class DateInput(forms.DateInput):
    input_type = 'date'

SEX = (
    ('Male','Male'),
    ('Female','Female'),
)

RELATE = (
    ('Father','Father'),
    ('Mother','Mother'),
    ('Brother','Brother'),
    ('Sister','Sister'),
    ('Others','Others'),
)

class Level1Form(forms.ModelForm):
    last_name = forms.CharField(label='Last name',disabled=True,max_length=255,required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Last name',
        }
    ))

    first_name = forms.CharField(label='First name',disabled=True,max_length=255,required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'First name',
        }
    ))

    other_name = forms.CharField(label='Other name',disabled=True,max_length=255,required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Other name',
        }
    ))

    email = forms.CharField(label='Email',disabled=True,max_length=255,required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Email',
        }
    ))

    mobile = forms.CharField(label='Mobile',disabled=True,max_length=255,required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Mobile number',
        }
    ))

    jamb = forms.CharField(label='Jamb registration number',disabled=True,max_length=255,required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Jamb reg',
        }
    ))

    address = forms.CharField(label='Address',required=True,widget=forms.Textarea(
        attrs={
            'class':'form-control',
            'placeholder':'Address',
            'rows':2,
        }
    ))

    dob = forms.DateField(label='Date of birth',widget=DateInput(
        attrs={
            'class':'form-control',
        }
    ))

    gender = forms.ChoiceField(choices=SEX)

    photo = forms.ImageField(label='Upload passport')

    class Meta:
        model = Personal
        fields = ['last_name','first_name','other_name','email','mobile','jamb','address','dob','gender','photo']

class NOKForm(forms.ModelForm):
    full_name = forms.CharField(label='Full name',max_length=255,required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Fullname',
        }
    ))
    email = forms.CharField(label='Email',max_length=255,required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Email',
        }
    ))
    relationship = forms.ChoiceField(choices=RELATE)
    address = forms.CharField(label='Next of kin address',required=True,widget=forms.Textarea(
        attrs={
            'class':'form-control',
            'placeholder':'Address....',
            'rows':2,
        }
    ))
    class Meta:
        model = NOK
        fields = ['full_name','email','relationship','address']

# class CategoryForm(forms.ModelForm):
#     category = forms.CharField(label='Category name',max_length=30,required=True,widget=forms.TextInput(
#         attrs={
#             'class':'form-control text-uppercase',
#             'placeholder':'Category name',
#         }
#     ))
#     class Meta:
#         model = Category
#         fields = ['category']

# class CommodityForm(forms.ModelForm):
#     name = forms.CharField(label='Commdity name',max_length=255,required=True,widget=forms.TextInput(
#         attrs={
#             'class':'form-control text-uppercase',
#             'placeholder':'Commdity name',
#         }
#     ))
#     description = forms.CharField(label='Description',required=True,widget=forms.Textarea(
#         attrs={
#             'class':'form-control',
#             'placeholder':'Description',
#             'rows':2,
#         }
#     ))

#     class Meta:
#         model = Commodity
#         fields = ['name','description']

# class MainForm(forms.ModelForm):
#     localprice = forms.IntegerField(label='Local price', widget=forms.NumberInput(
#         attrs={
#             'class':'form-control',
#             'placeholder':'Local price',
#         }
#     ))

#     class Meta:
#         model = Main
#         fields = ['localprice']