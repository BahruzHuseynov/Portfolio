from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, authenticate
from base_user.models import MyUser

User = get_user_model()


class MyUserLoginForm(AuthenticationForm):

    error_messages = {
        **AuthenticationForm.error_messages,
        # 'is_blocked': _("This account is blocked."),
    }

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            user = User.objects.filter(email = email).first()
            if user and not user.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
            # if user and user.is_blocked:
            #     raise forms.ValidationError(
            #         self.error_messages['is_blocked'],
            #         code='is_blocked',
            #     )

            self.user_cache = authenticate(self.request, email = email, password = password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def clean_username(self):
        # print(self.cleaned_data,'clean_username')
        email = self.cleaned_data.get("username")
        user = User.objects.filter(email__iexact = email).first()
        if user:
            return user.email
        return email.lower()



class BaseRegistrationForm(forms.ModelForm):
    """
        A form that creates a user in client side, with no privileges.
    """
    error_messages = {
        "password_incorrect": _("Cari şifrə yanlışdır"),
        "password_mismatch": _("Şifrə təsdiqləməsi yanlışdır"),
        "short_password": _("Şifrə minimum 6 simvoldan ibarət olmalıdır"),
        "only_english_letters": _("Yalnız ingilis hərfləri"),
    }

    password = forms.CharField(
        label=_("Şifrə"),
        widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label=_("Şifrənin təkrarı"),
        widget=forms.PasswordInput,
        help_text=_("Şifrənizi yenidən yazın"),
    )

    class Meta:
        model = MyUser

        fields = (
            "fullname",
            "email",
        )


        widgets = {
            "email": forms.EmailInput(
                attrs={

                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = (
            "fullname",
            "email"
        )

        for field in required_fields:
            if field in self.fields and not self.fields[field].required:
                self.fields[field].required = True

    def clean_fullname(self):
        isascii = lambda s: len(s) == len(s.encode())
        if not isascii(self.cleaned_data["fullname"]):
            raise forms.ValidationError("Yalnız ingilis hərfləri")
        return self.cleaned_data["fullname"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email.lower()

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            raise forms.ValidationError(self.error_messages["short_password"])
        else:
            return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"], code="password_mismatch",
            )
        return password_confirm

    def save(self, commit=True):
        user = super(BaseRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user