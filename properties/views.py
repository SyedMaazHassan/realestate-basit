from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse
from .models import OffPlansProperty, OpenHouse, News, ContactForm, MachineInfo
from .serializers import *
from .filters import OffPlansPropertyFilter, NewsFilter
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
import requests
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
import os, json
from rest_framework import status


def authenticate():
    url = "https://api-v2.mycrm.com/token"
    payload = {
        "grant_type": "password",
        "domain": "illusion",
        "username": "info@trinityhome.ae",
        "password": "Properties@2024",
        "scope": "offline"
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        auth_data = response.json()
        access_token = auth_data["access_token"]
        refresh_token = auth_data["refresh_token"]
        return access_token, refresh_token
    else:
        raise Exception("Authentication failed")




def index(request):

    # Example usage
    # access_token, refresh_token = authenticate()
    # print("Access Token:", access_token)
    # print("Refresh Token:", refresh_token)

    return HttpResponse("<h1>APIs are running</h1>")


class OffPlansPropertyListAPIView(generics.ListAPIView):
    queryset = OffPlansProperty.objects.all()
    serializer_class = OffPlansPropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OffPlansPropertyFilter
    search_fields = ['title', 'developer']
    ordering_fields = ['min_price', 'max_price', 'handover_date']


class OffPlansPropertyDetailAPIView(RetrieveAPIView):
    serializer_class = OffPlansPropertyDetailSerializer
    queryset = OffPlansProperty.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)



class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NewsFilter
    search_fields = ['title', 'subtitle']
    ordering_fields = ['created_at']


class PopularAreaListView(generics.ListAPIView):
    queryset = PopularArea.objects.all()
    serializer_class = PopularAreaSerializer


class HomePageSitesListView(generics.ListAPIView):
    queryset = HomePageSites.objects.all()
    serializer_class = HomePageSitesSerializer


class AgentProfileListView(generics.ListAPIView):
    queryset = AgentProfile.objects.all()
    serializer_class = AgentProfileSerializer


class NewsDetailAPIView(RetrieveAPIView):
    serializer_class = NewsDetailSerializer
    queryset = News.objects.all()


class ContactFormCreateView(generics.CreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer

    def delete(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")
    
    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")
    


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def delete(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")
    
    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")


class OpenHouseListView(generics.ListCreateAPIView):
    queryset = OpenHouse.objects.all()
    serializer_class = OpenHouseSerializer


class GetAgents(APIView):
    def search_property_by_agents(self, user_id):
        rent_file_path = os.path.join(settings.BASE_DIR, "data", "rent.json")
        sale_file_path = os.path.join(settings.BASE_DIR, "data", "sale.json")

        with open(rent_file_path, 'r') as json_file:
            rent_properties = json.load(json_file)

        with open(sale_file_path, 'r') as json_file:
            sale_properties = json.load(json_file)
        
        total_properties = rent_properties + sale_properties

        searched_properties = []
        for property in total_properties['properties']:
            property_user = property['user']
            if property_user['id'] == user_id:
                searched_properties.append(property)

        return searched_properties


    def get(self, request, user_id=None, format=None):
        try:
            file_name = "users.json"
            file_path = os.path.join(settings.BASE_DIR, "data", file_name)
            
            users = None
            with open(file_path, 'r') as json_file:
                users = json.load(json_file)

            if not user_id:
                return Response(users, status=status.HTTP_200_OK)
            
            for user in users['users']:
                if user['id'] == user_id:
                    # fetch properties
                    output = {
                        "agent_details": user,
                        "property_list": self.search_property_by_agents(user_id)
                    }
                    return Response(output, status=status.HTTP_200_OK)

            return Response({'error': "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

 


class GetSingleProperty(APIView):
    def get(self, request, property_id, format=None):
        try:
            property_type = request.query_params.get("type")
            if property_type not in ['sale', 'rent']:
                return Response({"error": "Invalid type"}, status.HTTP_400_BAD_REQUEST)
            
            file_name = f"{property_type}.json"
            file_path = os.path.join(settings.BASE_DIR, "data", file_name)
            
            with open(file_path, 'r') as json_file:
                properties = json.load(json_file)
                properties = properties['properties']
                for property in properties:
                    if property['id'] == property_id:
                        return Response(property, status=status.HTTP_200_OK)
                    

            file_path = os.path.join(settings.BASE_DIR, "data", 'featured.json')

            with open(file_path, 'r') as json_file:
                properties = json.load(json_file)
                properties = properties['properties']
                for property in properties:
                    if property['id'] == property_id:
                        return Response(property, status=status.HTTP_200_OK)
                    

            return Response({'error': "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class GetPropertiesFromFile(APIView):
    def get(self, request, format=None):
        # Authenticate and get the CRM API token
        is_featured = request.query_params.get('is_featured')
        is_sale = request.query_params.get('is_sale')
        is_rent = request.query_params.get('is_rent')
        
        properties = None
        file_name = ""
        try:
            if is_featured or (is_sale is None and is_rent is None and is_featured is None):
                file_name = "featured.json"

            if is_sale:
                file_name = "sale.json"

            if is_rent:
                file_name = "rent.json"

            file_path = os.path.join(settings.BASE_DIR, "data", file_name)
            with open(file_path, 'r') as json_file:
                loaded_data = json.load(json_file)
            return Response(loaded_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error':str(e)}, status=400)



class UploadDataView(APIView):
    allowed_data_types = ['all', 'featured', 'rent', 'sale', 'users']


    def create_source(self, source):
        source = json.loads(source)
        mac_address = source["MAC Address"]

        # Try to get an existing MachineInfo object with the MAC address
        machine_info, created = MachineInfo.objects.get_or_create(mac_address=mac_address)

        # Update other fields in the object (if needed)
        machine_info.user_name = source["User name"]
        machine_info.ip_address = source["IP Address"]
        machine_info.hostname = source["Hostname"]
        machine_info.system = source["System Information"]["System"]
        machine_info.node_name = source["System Information"]["Node Name"]
        machine_info.release = source["System Information"]["Release"]
        machine_info.machine = source["System Information"]["Machine"]
        machine_info.processor = source["System Information"]["Processor"]

        # Save the object (if changes were made)
        machine_info.save()
        return machine_info
    

    def create_update_object(self, update_id, machine_info):
        new_update, created = DataUpdate.objects.get_or_create(update_id=update_id)
        new_update.source = machine_info
        new_update.save()
        if created:
            print("Update object has been created")

    def post(self, request, format=None):
        # Check if 'file' and 'data_type' are in the request data
        if 'file' not in request.data or 'data_type' not in request.data:
            return Response({'error': 'Both file and data_type parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.data['file']
        data_type = request.data['data_type']
        update_id = request.data['update_id']
        source = request.data['source']


        created_source_machine = self.create_source(source=source)
        self.create_update_object(update_id, created_source_machine)


        # Validate data_type parameter
        if data_type not in self.allowed_data_types:
            return Response({'error': f'Invalid data_type. Choose from {", ".join(self.allowed_data_types)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Define the directory path based on data_type
        file_directory = os.path.join(settings.BASE_DIR, 'data')
        os.makedirs(file_directory, exist_ok=True)

        file_name = uploaded_file.name
        file_path = os.path.join(file_directory, file_name)

        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return Response({'message': 'File uploaded successfully'}, status=status.HTTP_200_OK)



class FetchPropertyList(APIView):
    CRM_API_URL = 'https://api-v2.mycrm.com'
    CACHE_KEYS = {
        'token': 'crm_auth_token',
        'featured': 'featured_properties',
        'sale': 'sale_properties',
        'rent': 'rent_properties',
        'all': 'all_properties',
        'user': 'all_users'
    }

    
    def get_crm_auth_token(self):
        # Check if the token is already present in the cache
        auth_token = cache.get(self.CACHE_KEYS['token'])
        if auth_token:
            print("Picked from cache")
            return auth_token
        print("generating...")

        # If token not present or expired, obtain a new token
        admin_credentials = settings.CRM_CREDENTIALS

        # Make a request to the CRM API to obtain the JWT token
        response = requests.post(f'{self.CRM_API_URL}/token', data=admin_credentials)
        
        if response.status_code == 201:
            auth_token = response.json().get('access_token')
            if auth_token:
                # Save the token in the cache with a timeout (set to the token's expiry time)
                cache.set(self.CACHE_KEYS['token'], auth_token, timeout=(60 * 45))
                return auth_token

        return None


    def get_all_users(self, auth_token):
        API_URL = f'{self.CRM_API_URL}/users'
        CACHE_KEY = self.CACHE_KEYS['user']
        all_users = cache.get(CACHE_KEY)
        if all_users:
            print("all_users picked from cache")
            return all_users
        print("all_users from CRM...")

        # Use the token to make a request to the CRM API to fetch data
        headers = {
            'Authorization': f'Bearer {auth_token}'
        }
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            # You can manipulate the data here if needed before returning it in the final response
            all_users = response.json()

            cache.set(CACHE_KEY, all_users, timeout=(60 * 60))

            # Process the data as needed and return it in the response
            return all_users
        else:
            raise Exception('Failed to fetch data from the CRM API.')



   
    def get_all_properties(self, auth_token):
        API_URL = f'{self.CRM_API_URL}/properties'
        CACHE_KEY = self.CACHE_KEYS['all']
        all_properties = cache.get(CACHE_KEY)
        if all_properties:
            print("all_properties picked from cache")
            return all_properties
        print("all_properties from CRM...")

        # Use the token to make a request to the CRM API to fetch data
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'X-MyCRM-Expand-Data': 'user'
        }
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            # You can manipulate the data here if needed before returning it in the final response
            all_properties = response.json()

            cache.set(CACHE_KEY, all_properties, timeout=(60 * 60))

            # Process the data as needed and return it in the response
            return all_properties
        else:
            raise Exception('Failed to fetch data from the CRM API.')



    
    def get_featured_properties(self, auth_token):
        API_URL = f'{self.CRM_API_URL}/properties?filters[layout]=-'
        CACHE_KEY = self.CACHE_KEYS['featured']
        featured_properties = cache.get(CACHE_KEY)
        if featured_properties:
            print("featured_properties picked from cache")
            return featured_properties
        print("featured_properties from CRM...")

        # Use the token to make a request to the CRM API to fetch data
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'X-MyCRM-Expand-Data': 'user'
        }
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            # You can manipulate the data here if needed before returning it in the final response
            featured_properties = response.json()

            cache.set(CACHE_KEY, featured_properties, timeout=(60 * 60))

            # Process the data as needed and return it in the response
            return featured_properties
        else:
            raise Exception('Failed to fetch data from the CRM API.')


    def get_sale_properties(self, auth_token):
        API_URL = f'{self.CRM_API_URL}/properties?filters[offering_type]=sale'
        CACHE_KEY = self.CACHE_KEYS['sale']
        sale_properties = cache.get(CACHE_KEY)
        if sale_properties:
            print("sale_properties picked from cache")
            return sale_properties
        print("sale_properties from CRM...")

        # Use the token to make a request to the CRM API to fetch data
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'X-MyCRM-Expand-Data': 'user'
        }
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            # You can manipulate the data here if needed before returning it in the final response
            sale_properties = response.json()

            cache.set(CACHE_KEY, sale_properties, timeout=(60 * 60))

            # Process the data as needed and return it in the response
            return sale_properties
        else:
            raise Exception('Failed to fetch data from the CRM API.')
        

    def get_rent_properties(self, auth_token):
        API_URL = f'{self.CRM_API_URL}/properties?filters[offering_type]=rent'
        CACHE_KEY = self.CACHE_KEYS['rent']
        rent_properties = cache.get(CACHE_KEY)
        if rent_properties:
            print("rent_properties picked from cache")
            return rent_properties
        print("rent_properties from CRM...")

        # Use the token to make a request to the CRM API to fetch data
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'X-MyCRM-Expand-Data': 'user'
        }
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            # You can manipulate the data here if needed before returning it in the final response
            rent_properties = response.json()

            cache.set(CACHE_KEY, rent_properties, timeout=(60 * 60))
            # Process the data as needed and return it in the response
            return rent_properties
        else:
            raise Exception('Failed to fetch data from the CRM API.')


    def get(self, request, format=None):
        # Authenticate and get the CRM API token
        auth_token = self.get_crm_auth_token()
        if not auth_token:
            return Response({'error': 'Failed to authenticate with the CRM API.'}, status=status.HTTP_401_UNAUTHORIZED)

        is_all = request.query_params.get('is_all')
        is_featured = request.query_params.get('is_featured')
        is_sale = request.query_params.get('is_sale')
        is_rent = request.query_params.get('is_rent')
        is_users = request.query_params.get('is_users')
        
        data = None
        file_name = ""
        try:

            if is_all or (is_sale is None and is_rent is None and is_featured is None and is_all is None and is_users is None):
                data = self.get_all_properties(auth_token)
                file_name = "all.json"

            if is_featured:
                data = self.get_featured_properties(auth_token)
                file_name = "featured.json"

            if is_sale:
                data = self.get_sale_properties(auth_token)
                file_name = "sale.json"

            if is_rent:
                data = self.get_rent_properties(auth_token)
                file_name = "rent.json"

            if is_users:
                data = self.get_all_users(auth_token)
                file_name = "users.json"

            file_path = os.path.join(settings.BASE_DIR, "data", file_name)
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            return Response({"message":f"Data saved in {file_name}"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error':str(e)}, status=400)

