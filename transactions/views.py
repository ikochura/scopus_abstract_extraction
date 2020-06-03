from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from transactions.models import Document
from .forms import CategoryForm, UploadFileForm


@login_required()
def category_view(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        category = form.save()
        messages.success(request, 'You create category {} $.'
                         .format(category.name_group_dataset))
        return redirect("home")

    context = {
        "title": "Category",
        "form": form
    }
    return render(request, "transactions/form.html", context)


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'transactions/upload.html', context)


def doc_list(request):
    docs = Document.objects.filter(category__user=request.user)
    return render(request, 'transactions/docs_list.html', {
        'docs': docs
    })


def upload_doc(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form_doc = form.save(commit=False)
            form_doc.user = request.user
            form_doc.save()
            return redirect('transactions:doc_list')
    else:
        form = UploadFileForm()  # request.user
    return render(request, 'transactions/upload_doc.html', {
        'form': form
    })


def delete_doc(request, pk):
    if request.method == 'POST':
        doc = Document.objects.get(pk=pk)
        doc.delete()
    return redirect('transactions:doc_list')


class DocListView(ListView):
    model = Document
    template_name = 'transactions/class_doc_list.html'
    context_object_name = 'docs'


class UploadDocView(CreateView):
    model = Document
    form_class = UploadFileForm
    success_url = reverse_lazy('class_doc_list')
    template_name = 'transactions/upload_doc.html'
