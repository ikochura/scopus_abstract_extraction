from django import forms

from .models import Category, Document


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


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['docfile', 'name', 'category']

    # def __init__(self, user, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super(UploadFileForm, self).__init__(*args, **kwargs)
    #     self.fields['category'].queryset = Document.objects.filter(category__user=user)
