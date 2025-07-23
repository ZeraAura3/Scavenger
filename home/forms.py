from django import forms
from .models import BasicDetails, CommunicationDetails, EducationDetails, ExperienceDetails, OtherDetails, GeneralDetails

class BasicDetailsForm(forms.ModelForm):
    class Meta:
        model = BasicDetails
        fields = '__all__'

class CommunicationDetailsForm(forms.ModelForm):
    class Meta:
        model = CommunicationDetails
        fields = '__all__'

class EducationDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        fields = '__all__'  

class ExperienceDetailsForm(forms.ModelForm):
    class Meta:
        model = ExperienceDetails
        fields = '__all__'

class OtherDetailsForm(forms.ModelForm):
    class Meta:
        model = OtherDetails
        fields = '__all__'

class GeneralDetailsForm(forms.ModelForm):   
    class Meta:
        model = GeneralDetails
        fields = '__all__'
