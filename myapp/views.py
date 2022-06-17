from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import*
from .serializers import*
from rest_framework.generics import*
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import*
from rest_framework import status


# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['GET'])
def index(request):
    api_url={
        '':'index/',
        'login':'/login/',
        'create-user':'/create-user/',
        'user-list':'/user-list/',
        'edit-user':'/edit-user/id',
        'delete-user':'/delete-user/id',
        'edit-doctor':'/edit-doctor/',
        'create-slot':'/create-slot/',
        'edit-slot':'edit-slot/id',
        'delete-slot':'/delete-slot/id',
        'my-slot':'/my-slot/',
        'mybook-appointment':'/mybook-appointment/slot-id',
        'edit-patient':'/edit-patient/',
        'book-appointment':'/book-appointment/',
        'my-appointment':'/my-appointment/',
        'edit-appointment':'/edit-appointment/id',
        'delete-appointment':'/delete-appointment/id'
        
    }
    
    return Response(api_url)

class LoginViews(GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UsercreateSerializers
    
    def post(self,request):
        serializer=UserLoginSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                # login(request,user)
                return Response({'token':token,'msg':'login Sucessfully'},status=status.HTTP_200_OK)
            else: 
                return Response({'msg':"invalid email and password "},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# class LogoutView(GenericAPIView):
#     queryset=User.objects.all()
#     serializer_class=UsercreateSerializers
    
#     def post(self,request):
#         token = get_tokens_for_user(request.user)
#         token.blacklist()
#         logout(request.user)
#         return Response({'Msg':'Logout'},status=status.HTTP_200_OK)
    
    
        
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ADMIN>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class UsercreateView(GenericAPIView):
    # permission_classes=[IsAdminUser]
    queryset=User.objects.all()
    serializer_class=UsercreateSerializers
    
    def post(self,request):
        serializer=UsercreateSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'user created'},status=status.HTTP_200_OK)
        return Response({'msg':'Enter the valid data'},status=status.HTTP_404_NOT_FOUND)
    
class UserListView(ListAPIView):
    permission_classes=[IsAdminUser]
    queryset=User.objects.all()
    serializer_class=EditUserSerializers
        
class EditUserView(GenericAPIView):
    permission_classes=[IsAdminUser]
    queryset=User.objects.all()
    serializer_class=EditUserSerializers
    
    def get(self,rerquest,pk):
        uid=User.objects.get(id=pk)
        serializer=EditUserSerializers(uid)
        return Response(serializer.data)
    
    def put(self,request,pk):
        uid=User.objects.get(id=pk)
        serializer=EditUserSerializers(instance=uid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'User update'},status=status.HTTP_200_OK)
        return Response({'msg':'Enter the valid data'},status=status.HTTP_404_NOT_FOUND)  
    
class DeleteUserView(GenericAPIView):
    permission_classes=[IsAdminUser]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
   
    def get(self,rerquest,pk):
        uid=self.get_object(pk=pk)
        serializer=EditUserSerializers(uid)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        uid=self.get_object(pk=pk)
        uid.delete()
        return Response('user deleted')    
    
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DOCTOR>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class DrEditView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=DoctorEditProfileSerializers
    queryset=User.objects.filter(role='doctor')
    
    def get(self,request):
        uid=User.objects.get(id=request.user.id)
        if uid.role == 'doctor':
            serializer=DoctorEditProfileSerializers(uid)
            return Response(serializer.data)
        else:
            return Response('data not found')
        
    def put(self,request):
        uid=User.objects.get(id=request.user.id)
        if uid.role == 'doctor':
            serializer= DoctorEditProfileSerializers(instance=uid,data=request.data)  
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Your profile Update'},status=status.HTTP_200_OK)
            return Response({'msg':'Enter the valid data'},status=status.HTTP_404_NOT_FOUND) 
        else:
            return Response('data not found')
        
class SlotCreateView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=SlotCreateSerializers
    queryset=Slot.objects.all()
    
    def post(self,request):
        user=request.user
        if user.role == 'doctor':
            serializer=SlotCreateSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(doctor=user)
                return Response({'status':'HTTP_200_OK','msg':'slot create'})
            return Response({'status':'HTTP_404_NOT_FOUND','msg':'Enter the valid data'})
        return Response('only doctor create slot')
    
class EditSlotView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=SlotCreateSerializers
    queryset=Slot.objects.all()
    
    def get(self,request,pk):
        uid=Slot.objects.get(id=pk)
        serializer=EditSlotSerializers(uid)
        return Response(serializer.data)
    
    def put(self,request,pk):
        user=request.user
        uid=Slot.objects.get(id=pk)
        if uid.doctor == user:
            serializer=EditSlotSerializers(instance=uid,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'HTTP_200','msg':'slot Update'})
            return Response({'status':'HTTP_404_NOT_FOUND','msg':'Enter the valid data'})
        return Response('only doctor edit slot')
        
class DeleteSlotView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    def get_object(self, pk):
        try:
            return Slot.objects.get(pk=pk)
        except Slot.DoesNotExist:
            raise Http404
   
    def get(self,rerquest,pk):
        uid=self.get_object(pk=pk)
        serializer=EditSlotSerializers(uid)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        user=request.user
        uid=self.get_object(pk=pk)
        if uid.doctor == user:
            uid.delete()
            return Response('Slot deleted') 
        return Response('you can delete only your Slot')

        
class MySlotView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=EditSlotSerializers
    
    def get(self,request):
        slot=Slot.objects.filter(doctor=request.user)
        serializer=EditSlotSerializers(slot,many=True)
        return Response(serializer.data)
    
class MyBookAppointment(GenericAPIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request,pk):
        slot=Slot.objects.get(id=pk)
        app=Appointments.objects.filter(slot=slot)
        serializer=ViewAppointmentSerializers(app,many=True)
        return Response(serializer.data)

class ChangeStatusView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    
    def put(self,request,pk):
        uid=Appointments.objects.get(id=pk)
        if uid.slot.doctor == request.user:
            serializer=ChangeStatusSerializers(instance=uid,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status change'},status=status.HTTP_200_OK)
            return Response({'enter the valid data'},status=status.HTTP_200_OK)
        return Response('you can not change status')
            
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>PATIENT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class PatientEditView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=PatientEditProfileSerializers
    queryset=User.objects.filter(role='patient')
    
    def get(self,request):
        uid=User.objects.get(id=request.user.id)
        if uid.role == 'patient':
            serializer=PatientEditProfileSerializers(uid)
            return Response(serializer.data)
        else:
            return Response('data Not Found')
    
    def put(self,request):
        uid=User.objects.get(id=request.user.id)
        if uid.role == 'patient':
            serializer=PatientEditProfileSerializers(instance=uid,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Your profile update'},status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response({'msg':'Enter the valid data'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('data Not Found')
            
            
class AppointmnetCreateView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CreateAppointmentSerializers
    queryset=Appointments.objects.all()
    
    def post(self,request):
        if request.user.role == 'patient':
            serializer=CreateAppointmentSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(patient=request.user)
                return Response({'msg':'appointment book '},status=status.HTTP_200_OK)
            return Response({'msg':'enter the valid data'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('Only patient book appointment')
        
class MyAppointmentView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ViewAppointmentSerializers
    
    def get(self,request):
        uid=Appointments.objects.filter(patient=request.user)
        serializer=ViewAppointmentSerializers(uid,many=True)
        return Response(serializer.data)           
        
            
class EditAppointmentView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request,pk):
        uid=Appointments.objects.get(id=pk)
        serializer=ViewAppointmentSerializers(uid)
        return Response(serializer.data)
    
    def put(self,request,pk):
        uid=Appointments.objects.get(id=pk)
        if uid.patient == request.user:
            serializer=EditAppointmentSerializers(instance=uid,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'appointment Edit'},status=status.HTTP_200_OK)
            return Response({'msg':'enter the valid data'},status=status.HTTP_404_NOT_FOUND)
        return Response('you can edit only your appointment')
    
class DeleteAppointmnetView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    def get_object(self, pk):
        try:
            return Appointments.objects.get(pk=pk)
        except Appointments.DoesNotExist:
            raise Http404
   
    def get(self,rerquest,pk):
        uid=self.get_object(pk=pk)
        serializer=ViewAppointmentSerializers(uid)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        user=request.user
        if user.role == 'patient':
            uid=self.get_object(pk=pk)
            if uid.patient == user:
                uid.delete()
                return Response('appointment deleted') 
            return Response('you can delete only your appointment')
        return Response('only patient delete appointment')

            
                
    
    
    
    