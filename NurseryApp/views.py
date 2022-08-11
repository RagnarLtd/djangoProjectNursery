from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status
from rest_framework.generics import GenericAPIView, DestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from django.contrib import messages

from NurseryApp.forms import SingUpForm, CreatePetForm
from NurseryApp.models import UserProfile, Pet
from NurseryApp.serializers import PetSerializer


class UserRegisterFormView(View):
    """
    Регистрация пользователя. При регистрации также создается расширение данных пользователя
    """
    def get(self, request):
        form = SingUpForm()
        return render(request, 'NurseryApp/register.html', context={'form': form})

    def post(self, request):
        form = SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data.get('username'))
            userprofile = UserProfile.objects.create(
                user=user,
                shelter=form.cleaned_data.get('shelter'),
                address=form.cleaned_data.get('address')
            )
            userprofile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            form = SingUpForm()
        return render(request, 'NurseryApp/register.html', context={'form': form})


class PetList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    Представление списка питомцев приюта через DRF, также возможность создания питомцев зарегестрированным пользователям
    """
    serializer_class = PetSerializer

    def get_queryset(self):
        queryset = Pet.objects.all()
        return queryset.filter(shelter_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.list(request, *args, **kwargs)
        else:
            return redirect('login')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=self.request.user.id)
        serializer.validated_data['shelter'] = user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request):
        return self.create(request)


class MyLoginView(LoginView):
    template_name = 'NurseryApp/login.html'
    next_page = 'all_pets'


class MyLogoutView(LogoutView):
    next_page = 'login'


class PetInfoAPIView(DestroyAPIView, UpdateModelMixin, RetrieveModelMixin, GenericAPIView):
    """
    Представление данных питомца через DRF с возможностью редактирования и удаления
    """
    serializer_class = PetSerializer
    queryset = Pet.objects.all()

    def get(self, request, pk):
        if request.user.is_authenticated:
            return self.retrieve(request, pk)
        else:
            return redirect('login')

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AllPetsAPIView(ListModelMixin, GenericAPIView):
    """
    Представление всех питомцев через DRF
    """
    serializer_class = PetSerializer
    queryset = Pet.objects.all().filter(is_active=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AllPetsView(View):
    """
    Вывод всех питомцев со всех питомников
    """
    def get(self, request):
        pets = Pet.objects.all().filter(is_active=True)
        return render(request, 'NurseryApp/pets.html', context={'pets': pets})


class AddPetsView(View):
    """
    Добавление питомцев для зарегестрированных пользователей
    """
    def get(self, request):
        pet_form = CreatePetForm()
        return render(request, 'NurseryApp/add_pet.html', context={'pet_form': pet_form})

    def post(self, request):
        pet_form = CreatePetForm(request.POST)
        if pet_form.is_valid():
            user = User.objects.get(id=self.request.user.id)
            Pet.objects.create(**pet_form.cleaned_data, shelter=user)
            return HttpResponseRedirect("/pets")
        return render(request, 'NurseryApp/add_pet.html', context={'pet_form': pet_form})


class EditPetView(View):
    """
    Возможность редакитрование данных питомцев только питомцев приюта пользователя
    """
    def get(self, request, pk):
        pet = Pet.objects.get(pk=pk)
        pet_form = CreatePetForm(instance=pet)
        return render(request, 'NurseryApp/edit_pet.html', context={'pet_form': pet_form, 'pk': pk})

    def post(self, request, pk):
        pet = Pet.objects.get(pk=pk)
        pet_form = CreatePetForm(request.POST, instance=pet)
        if self.request.user.id == pet.shelter.id:
            if pet_form.is_valid():
                pet.save()
                return HttpResponseRedirect('/pets')
        messages.info(request, 'Этот питомец не из вашего приюта, вы не можете его редактировать')
        return render(request, 'NurseryApp/edit_pet.html', context={'pet_form': pet_form, 'pk': pk})


class DeletePetView(View):
    """
    Удаление питомца пользователем(приютом)
    """
    def get(self, request, pk):
        try:
            pet = Pet.objects.get(pk=pk)
            if self.request.user.id == pet.shelter.id:
                pet.delete()
                return HttpResponseRedirect("/pets")
            else:
                messages.info(request, 'Этот питомец не из вашего приюта, вы не можете его удалить')
                return HttpResponseRedirect(f"/pet/{pk}")
        except Pet.DoesNotExist:
            return HttpResponseNotFound("<h2>Person not found</h2>")
