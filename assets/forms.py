from django import forms
from .models import Asset


class AssetSubmitForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name', 'category', 'description',
            'address', 'latitude', 'longitude',
            'phone', 'website', 'hours', 'photo',
            'tags', 'submitted_by',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g. food, youth, free'}),
            'submitted_by': forms.TextInput(attrs={'placeholder': 'Your name (optional)'}),
            'hours': forms.TextInput(attrs={'placeholder': 'e.g. Mon–Fri 9am–5pm'}),
        }
        labels = {
            'submitted_by': 'Your name (optional)',
            'tags': 'Keywords (optional)',
        }

    def clean(self):
        cleaned = super().clean()
        lat = cleaned.get('latitude')
        lng = cleaned.get('longitude')
        if not lat or not lng:
            raise forms.ValidationError('Please place a pin on the map to set the location.')
        return cleaned
