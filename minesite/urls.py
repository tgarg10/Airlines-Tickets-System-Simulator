from minesite.views import *
from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [
    #path('',TemplateView.as_view(template_name = "login.html"), name = "login"),
    path('', login, name = 'login'),
    #path('signup/', TemplateView.as_view(template_name = "signup.html"), name = 'signup'),
    path('signup/', signup, name = 'signup'),
    path('flightbooking/<str:username>/',select_flight,name="select_flight"),
    path('mytransactions/<str:username>/',mytransactions,name="mytransactions"),
    path('accountdetails/<str:username>/',account_details,name="edit_account_details"),
    path('editaccountdetails/<str:username>/',edit_account_details,name="edit_account_details"),
    path('myupcomingflights/<str:username>/',myupcomingflights,name="myupcomingflights"),
    path('transactionpage/',transaction_page, name="transaction_page"),
    path('economyseatselectionpage/', e_seatselection_page, name="e_seatselection_page"),
    path('businessseatselectionpage/', b_seatselection_page, name="b_seatselection_page"),
    path('deletetransaction/<str:transactionid>/', deletetransaction, name="deletetransaction"),
    path('deleteaccount/<str:username>/', deleteaccount, name="deleteaccount"),
    path('aboutus/', aboutus, name="aboutus"),
]   