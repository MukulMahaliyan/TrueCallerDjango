from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from FindCallerApp.models import CustomUser, SpamReport, Contact
from FindCallerApp.serializers import RegisterSerializer, SpamReportSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User is registered successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportSpamView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        serializer = SpamReportSerializer(data=request.data);
        if serializer.is_valid():
            SpamReport.objects.create(phone_number=request.data.get('phone_number'), created_by=request.user)
            return Response({'message': 'Phone number is marked as spam'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
       
        query = request.query_params.get('q')

        if not query:
            return Response({'Error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        if query.isdigit():  
            users = CustomUser.objects.filter(phone_number=query)
            contacts = Contact.objects.filter(phone_number=query)
            
        else:  
            users = CustomUser.objects.filter(Q(name__icontains=query))
            contacts = Contact.objects.filter(Q(name__icontains=query))
           

       # spam_counts = SpamReport.objects.values('phone_number').annotate(count=Count('phone_number'))
       # spam_map = {entry['phone_number']: entry['count'] for entry in spam_counts}

        results = []
        for contact in contacts:
            results.append({
                'name': contact.name,
                'phone_number': contact.phone_number,
                'spam_likelihood': get_spam_likelihood(contact.phone_number)
            })

        for user in users:
            results.append({
                'name': user.name,
                'phone_number': user.phone_number,
                'spam_likelihood': get_spam_likelihood(user.phone_number)
            })

        return Response(results)    
 

def get_spam_likelihood(phone_number):
    
  
    report_count = SpamReport.objects.filter(phone_number=phone_number).count()
    report = 'Low'
    if report_count > 2:
        report = 'Medium' 
    elif report_count>5:
        report = 'High'
    return report


class TokenObtainView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['name'] = user.name
#         token['phone_number'] = user.phone_number
#         return token

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         # Authenticate user with custom logic
#         user = authenticate(email=email, password=password)
#         if not user:
#             raise serializers.ValidationError("Invalid email or password")

#         # Standard token generation
#         data = super().validate(attrs)
#         data['user'] = {
#             'id': user.id,
#             'name': user.name,
#             'email': user.email,
#             'phone_number': user.phone_number,
#         }
#         return data


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer