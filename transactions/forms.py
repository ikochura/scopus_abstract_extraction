from django import forms

from .models import Category, Dataset


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name_group_dataset"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        name_group_dataset = self.cleaned_data['name_group_dataset']

        return name_group_dataset
