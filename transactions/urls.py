from django.urls import path

from .views import category_view, UploadDocView, upload, doc_list, upload_doc, delete_doc, DocListView

urlpatterns = [
    path('addcat/', category_view, name='create_category'),
    path('upload/', upload, name='upload'),
    path('docs/', doc_list, name='doc_list'),
    path('docs/upload/', upload_doc, name='upload_doc'),
    path('docs/<int:pk>/', delete_doc, name='delete_doc'),
    path('class/docs/', DocListView.as_view(), name='class_doc_list'),
    path('class/docs/upload/', UploadDocView.as_view(), name='class_upload_doc'),
]

app_name = 'transactions'
