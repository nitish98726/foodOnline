from django import forms
from . models import Vendor
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name' , 'vendor_license']
    def __init__(self , *args , **kwargs):
        super(VendorForm , self).__init__(*args ,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['style'] = 'width:90%'
            self.fields[field].widget.attrs['class'] = 'form-control fs-6'