from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from base_user.tools.login_helper_view import AuthView
from base_user.forms import BaseRegistrationForm, MyUserLoginForm
from django.contrib.auth import views
from django.contrib.auth import login as auth_login
import bcrypt
import sendgrid
from sendgrid.helpers.mail import *
from talent_scoring_backend.settings import SENDGRID_API_KEY, EMAIL_HOST_USER,DEFAULT_FROM_EMAIL, SENDER
# Create your views here.


User = get_user_model()

class AccountBaseLoginView(AuthView, views.LoginView):
    """
        Account Login View
        if user is authenticated then redirect to dashboard view
    """
    template_name = "login.html"
    form_class = MyUserLoginForm
    success_url = reverse_lazy("core:index")

    def check_old_password_before_err(self, form):
        """Check old db password"""
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("username")
        user = User.objects.filter(email=email).first()

        if password and user is not None and user.old_psw_hash:

            # check if old password matches
            if bcrypt.checkpw(
                    password.encode("utf-8"), user.old_psw_hash.encode("utf-8")
            ):
                # set password as new password
                user.set_password(password)
                user.save()

                # login user
                auth_login(self.request, user)
                return HttpResponseRedirect(self.success_url)

        return super().form_invalid(form)

    def form_invalid(self, form, *args, **kwargs):
        """
            Check old password before returning error
        """
        print(form.errors)
        return self.check_old_password_before_err(form)




class AccountRegistrationView(AuthView, generic.CreateView):
    """
        Account Register View,
        if user is authenticated then redirect to dashboard view
    """
    template_name = "register.html"
    form_class = BaseRegistrationForm
    model = User
    success_url = reverse_lazy("account:login")
    user = None

    # @staticmethod
    # def __default_send_email(user, activation_link):
    #     mail_subject = "Hesabınızı aktivləşdirin"
    #     message_body = render_to_string(
    #         "client/account/email-activation.html",
    #         {"user": user, "activation_link": activation_link},
    #     )
    #     content = Content("text/html", message_body)
    #     message = Mail(
    #         from_email=Email(email=DEFAULT_FROM_EMAIL, name=SENDER),
    #         # to_emails=Email(user.email,),
    #         subject=mail_subject,
    #         html_content=content)
    #
    #     personalization = Personalization()
    #     personalization.add_to(Email(user.email))
    #     message.add_personalization(personalization)
    #
    #     try:
    #         sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    #         sg.client.mail.send.post(request_body=message.get())
    #
    #     except Exception as e:
    #         print(e.message, "error")
    #
    # @staticmethod
    # def send_activation_mail(user):
    #
    #     useractivation = user.useractivation
    #     activation_link = useractivation.full_activation_link
    #
    #     AccountRegistrationView.__default_send_email(user, activation_link)
    #
    #     useractivation.mail_sent = True
    #     useractivation.save()

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        # AccountRegistrationView.send_activation_mail(user)

        return super().form_valid(form)

    def form_invalid(self, form):
        # print(form.data)
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)