from django.urls import path
from NurseryApp.views import UserRegisterFormView, PetList, MyLoginView, MyLogoutView, PetInfoAPIView, AllPetsAPIView, \
    AllPetsView, AddPetsView, EditPetView, DeletePetView

urlpatterns = [
    path('register', UserRegisterFormView.as_view(), name='register'),
    path('api/pet', PetList.as_view(), name='pet'),
    path('login', MyLoginView.as_view(), name='login'),
    path('logout', MyLogoutView.as_view(), name='logout'),
    path('api/pet/<int:pk>', PetInfoAPIView.as_view(), name='api_pet_info'),
    path('api/pets', AllPetsAPIView.as_view(), name='api_all_pets'),
    path('pets', AllPetsView.as_view(), name='all_pets'),
    path('pet/add', AddPetsView.as_view(), name='add_pet'),
    path('pet/<int:pk>', EditPetView.as_view(), name='edit_pet'),
    path('pet/delete/<int:pk>', DeletePetView.as_view(), name='delete')
]
