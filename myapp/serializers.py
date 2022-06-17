from rest_framework import serializers
from .models import*
from django.contrib.auth.hashers import make_password


class UsercreateSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','role','password']
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UsercreateSerializers, self).create(validated_data)
    
class UserLoginSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=250)
    class Meta:
        model=User
        fields=['email','password']
        
class EditUserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','role']
        
class DoctorEditProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','addres','gender','mobile','clinicname','types','pic']     
        
       
class PatientEditProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','addres','gender','mobile','pic']     
        
class SlotCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model=Slot
        fields=['weeks','timeslot']     
        
class EditSlotSerializers(serializers.ModelSerializer):
    class Meta:
        model=Slot
        fields=['weeks','timeslot']  
        
class CreateAppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model=Appointments
        fields=['slot','description']
        
class EditAppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model=Appointments
        fields=['description']
        
class ViewAppointmentSerializers(serializers.ModelSerializer):   
    class Meta:
        model=Appointments
        fields='__all__'
        
class ChangeStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model=Appointments
        fields=['status']