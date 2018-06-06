from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
# DOing a Q lookup

from django.db.models import Q


from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )


User = get_user_model()




#==================================  REGISTRATION  ======================================

class UserCreateSerializer(ModelSerializer):
    email = EmailField(label = "Email Address")
    email2 = EmailField(label = "Confirm email")
    class Meta:
        model = User
        fields = [
             
             'username',
             'email',
             'email2',
             'password',
        ]

        #Setting the password to write only
        extra_kwargs = { "password": 
                        { "write_only":True }
                                             }

    #checking if email exists, General validation
    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email = email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered")
        return data

    #validating email1
    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        # Checking if email exists
        user_qs = User.objects.filter(email = email2)
        if user_qs.exists():
            raise ValidationError("This user has already registered")
        
        return value    

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value

    #overwrite the create() method
    def create(self, validated_data):
        print validated_data #a dictionary

        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        #create an isntance of the object and save it
        user_obj = User(            
            username = username,
            email = email
        )
        
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



#=============================== LOGIN ===============================

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank = True, read_only = True)
    username = CharField(required=False, allow_blank = True)
    email = EmailField(label = "Email Address",required=False, allow_blank = True)
    class Meta:
        model = User 
        fields = [
             
             'username',
             'email',   
             'password',
             'token',

        ]
        
        #Setting the password to write only
        extra_kwargs = {"password": 
                        {"write_only":True}
                                  }

    #checking if email exists, General validation
    def validate(self, data):
        user_obj = None
        email = data.get("emial", None) #dont need to use None though, its the default
        username = data.get("username", None)
        password = data["password"]

        if not email and not username:
            raise ValidationError("A username or email is required to login")

        #getting user object from this
        user = User.objects.filter(
            Q(email=email)|  
            Q(username=username)
            ).distinct()

        user = user.exclude(email__isnull=True).exclude(email__iexact='') #excludes from the above filtered those without email
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials, please try again.")

        data["token"] =  "SOME RANDOM TOKEN"
        return data



















