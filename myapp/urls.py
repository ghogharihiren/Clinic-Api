from django.urls import path
from .views import*

urlpatterns = [
    path('',index,name='index'),
    path('login/',LoginViews.as_view()),
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ADMIN-API>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    path('create-user/',UsercreateView.as_view()),
    path('user-list/',UserListView.as_view()),
    path('edit-user/<int:pk>',EditUserView.as_view()),
    path('delete-user/<int:pk>',DeleteUserView.as_view()),
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Doctor-Api>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    path('edit-doctor/',DrEditView.as_view()),
    path('create-slot/',SlotCreateView.as_view()),
    path('edit-slot/<int:pk>',EditSlotView.as_view()),
    path('delete-slot/<int:pk>',DeleteSlotView.as_view()),
    path('my-slot/',MySlotView.as_view()),
    path('mybook-appointment/<int:pk>',MyBookAppointment.as_view()),
    path('edit-status/<int:pk>',ChangeStatusView.as_view()),
    
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>patient-Api>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    path('edit-patient/',PatientEditView.as_view()),
    path('book-appointment/',AppointmnetCreateView.as_view()),
    path('my-appointment/',MyAppointmentView.as_view()),
    path('edit-appointment/<int:pk>',EditAppointmentView.as_view()),
    path('delete-appointment/<int:pk>',DeleteAppointmnetView.as_view()),
    
    
    
    
]