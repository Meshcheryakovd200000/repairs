from django.forms import ModelForm
from django import forms
from .models import Repair, Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Проголосуйте',
            'body': 'Добавьте комментарий с вашим голосом'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class RepairForm(ModelForm):
    class Meta:
        model = Repair
        fields = ['title', 'featured_image', 'description', 'demo_link',
                  'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update({'class': 'input', 'id': 'formInput#text'})
        # self.fields['description'].widget.attrs.update({'class': 'input'})
