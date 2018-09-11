from django.conf.urls import url
from catalog import views

# homepage
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/', views.BookListView.as_view(), name='books'),
    url(r'^owners/$', views.OwnerListView.as_view(), name='owners'),
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'^mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'^loanbooks/', views.LoanedBooksListView.as_view(), name='all-loaned'),
]

# book manage
urlpatterns += [
    url(r'^book/create/', views.BookCreate.as_view(), name='book_create'),
    url(r'^book/(?P<pk>\d+)/update/', views.BookUpdate.as_view(), name='book_update'),
    url(r'^book/(?P<pk>\d+)/delete/', views.BookDelete.as_view(), name='book_delete'),
    url(r'^book/(?P<pk>\d+)', views.BookDetailView.as_view(), name='book-detail'),
]

# book instance manage
urlpatterns += [
    url(r'^bookinst/create/', views.BookInstCreate.as_view(), name='bookinst_create'),
    url(r'^bookinst/(?P<pk>\w{8}(-\w{4}){3}-\w{12}?)/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

# owner manage
urlpatterns += [
    url(r'^owner/create/', views.OwnerCreate.as_view(), name='owner_create'),
    url(r'^owner/(?P<pk>\d+)/update/', views.OwnerUpdate.as_view(), name='owner_update'),
    url(r'^owner/(?P<pk>\d+)/delete/', views.OwnerDelete.as_view(), name='owner_delete'),
    url(r'^owner/(?P<pk>\d+)', views.OwnerDetailView.as_view(), name='owner_detail'),
]

# author manage
# urlpatterns += [
#     url(r'^author/create/', views.AuthorCreate.as_view(), name='author_create'),
#     url(r'^author/(?P<pk>\d+)/update/', views.AuthorUpdate.as_view(), name='author_update'),
#     url(r'^author/(?P<pk>\d+)/delete/', views.AuthorDelete.as_view(), name='author_delete'),
#     url(r'^author/(?P<pk>\d+)', views.AuthorDetailView.as_view(), name='author-detail'),
# ]
