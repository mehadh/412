from django.shortcuts import render
from django.views.generic import *
from .models import * # import the models
from .forms import *
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
class ShowAllProfilesView(ListView):
    """
    list of all profiles
    """
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # context variable to use in the template
class ShowProfilePageView(DetailView):
    """
    show it one page
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
class ShowProfileSelfView(LoginRequiredMixin, DetailView):
    """
    show it profile page
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
    def get_object(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
            return profile
        except Profile.DoesNotExist:
            # Redirect to create profile if it doesn't exist
            return redirect('create_profile')
class CreateProfileView(CreateView):
    """
    user creation meth bc admin anoy
    """
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        user_form = UserCreationForm(self.request.POST)

        if form.is_valid() and user_form.is_valid():
            return self.form_valid(form, user_form)
        else:
            return self.form_invalid(form, user_form)

    def form_valid(self, form, user_form):
        user = user_form.save()
        form.instance.user = user
        self.object = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())
    def form_invalid(self, form, user_form):
        return self.render_to_response(
            self.get_context_data(form=form, user_form=user_form)
        )

    def get_success_url(self):
        return reverse('show_profile_self')

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    """
    View to let a profile post a status message
    """
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])  # Fetch profile by pk from URL
        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])  # Fetch profile by pk from URL
        form.instance.profile = profile  # Attach profile to status message
        sm = form.save()

        # Handle image uploads
        files = self.request.FILES.getlist('files')
        for f in files:
            image = Image()
            image.image_file = f
            image.status_message = sm
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})  # Redirect to profile
