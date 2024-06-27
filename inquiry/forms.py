from django.forms import ModelForm

from .models import Inquiry


class InquiryForm(ModelForm):

    class Meta:

        model = Inquiry
        fields = '__all__'