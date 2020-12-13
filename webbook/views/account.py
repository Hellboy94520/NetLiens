from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site


from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView

from ..models import User, Announcement, Category, Localisation
from ..forms import PublicUserForm, SignUpForm, send_mail as SendEmail

#TODO: To delete when ErrorPages will be implement when activation link is incorrect
from django.http import HttpResponse

# -----------------------------
# Token
# -----------------------------
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode

# -----------------------------
# View
# -----------------------------
@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    """
        View to manage account
    """

# -----------------------------
class SignupView(View):
    """
        View to create an account
    """
    form_class = SignUpForm
    template_name = 'account/signup.html'
    success_url = "/account/signup/done/"
    email_template_name = "account/email_signup_content.html"
    subject_template_name = "account/email_signup_subject.txt"
    from_email = None
    title = _('Signup')

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            current_site = get_current_site(request)
            opts = {
            'use_https': request.is_secure(),
            'site_domain': current_site.domain,
            'site_name': current_site.name,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'from_email': self.from_email
            }
            form.save(**opts)
            return redirect(self.success_url)
        return render(request, self.template_name, locals())

# -----------------------------
class SignupConfirmation(TemplateView):
    """
        View to activate account
    """
    template_name = None
    email_template_name = None
    subject_template_name = None

    def get_user(self, uidb64):
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        l_user = get_object_or_404(User, pk=uid)
        return l_user

    def get(self, request, *args, **kwargs):
        # - Activate account
        assert 'uidb64' in kwargs and 'token' in kwargs, Http404()
        l_user = self.get_user(kwargs['uidb64'])
        if not default_token_generator.check_token(l_user, kwargs['token']):
            raise Http404()
        l_user.is_active = True
        l_user.save()
        # - Send Email
        opts = {
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'context': { 'user': l_user },
            'from_email': None,
            'to_email': l_user.email
        }
        SendEmail(**opts)

        return super(SignupConfirmation, self).get(request, *args, **kwargs)


# -----------------------------
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from ..forms import PasswordChangeForm
class PasswordChangeView(DjangoPasswordChangeView):
    email_template_name = None
    subject_template_name = None
    form_class = PasswordChangeForm

    def form_valid(self, form):
        l_response = super(DjangoPasswordChangeView, self).form_valid(form)
        opts = {
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'from_email': None,
            'to_email': form.user.email
        }
        form.send_email(**opts)
        return l_response


# -----------------------------
from django.contrib.auth.views import PasswordResetConfirmView as DjangoPasswordResetConfirmView
from ..forms import SetPasswordForm
class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    email_template_name = None
    subject_template_name = None
    form_class = SetPasswordForm

    def form_valid(self, form):
        l_response = super(DjangoPasswordResetConfirmView, self).form_valid(form)
        opts = {
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'from_email': None,
            'to_email': form.user.email
        }
        form.send_email(**opts)
        return l_response

# -----------------------------
@method_decorator(login_required, name='dispatch')
class UpdateView(TemplateView):
    """
        View to update account
    """
    form_class = PublicUserForm

    def get(self, request, *args, **kwargs):
        form = PublicUserForm(instance=request.user)
        return render(request, self.template_name, locals())
    
    def post(self, request, *args, **kwargs):
        form = PublicUserForm(
            request.POST,
            instance=request.user
        )
        if form.is_valid():
            user = form.save()
            return redirect('/')
        return render(request, self.template_name, locals())

# -----------------------------
@method_decorator(login_required, name='dispatch')
class AnnouncementView(TemplateView):
    """
        View to manage announcement
    """
    def get_nl_tab(self, request):
        nl_status = [ [ 0, request.user.nl0-Announcement.objects.filter(owner=request.user, nl=0).count(), request.user.nl0 ],
            [ 1, request.user.nl1-Announcement.objects.filter(owner=request.user, nl=1).count(), request.user.nl1 ],
            [ 2, request.user.nl2-Announcement.objects.filter(owner=request.user, nl=2).count(), request.user.nl2 ],
            [ 3, request.user.nl3-Announcement.objects.filter(owner=request.user, nl=3).count(), request.user.nl3 ],
            [ 4, request.user.nl4-Announcement.objects.filter(owner=request.user, nl=4).count(), request.user.nl4 ],
            [ 5, request.user.nl5-Announcement.objects.filter(owner=request.user, nl=5).count(), request.user.nl5 ],
            [ 6, request.user.nl6-Announcement.objects.filter(owner=request.user, nl=6).count(), request.user.nl6 ],
            [ 7, request.user.nl7-Announcement.objects.filter(owner=request.user, nl=7).count(), request.user.nl7 ],
        ]
        return nl_status

    def get(self, request, *args, **kwargs):
        nl_status = self.get_nl_tab(request)
        return render(request, self.template_name, locals())

# -----------------------------
from ..forms import AnnouncementUserSettingForm
@method_decorator(login_required, name='dispatch')
class AnnouncementCreationView(FormView):
    """
        View to create an announcement
    """
    form_class = AnnouncementUserSettingForm

    def get_form_kwargs(self):
        kwargs = super(AnnouncementCreationView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        announcement = form.save()
        self.success_url = self.success_url.replace("<str:announcement_url>", announcement.url)
        return super(AnnouncementCreationView, self).form_valid(form)

    # Check if NL available. If not, return to purchase
    def get(self, request, *args, **kwargs):
        if not self.request.user.has_nl:
            print(AnnouncementPurchaseView)
            #return redirect(AnnouncementPurchase.get_urlconf(), locals())
        return super(AnnouncementCreationView, self).get(request, args, kwargs)


# -----------------------------
from ..forms import AnnouncementUserDataForm
@method_decorator(login_required, name='dispatch')
class AnnouncementCreationDataView(FormView):
    """
        View to create an announcement with it data
    """
    form_class = AnnouncementUserDataForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid(get_object_or_404(Announcement, url=kwargs['announcement_url'])):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        l_announcement = form.save()
        return super(AnnouncementCreationDataView, self).form_valid(form)

# -----------------------------
# from ..forms import AnnouncementUserDataForm
# @method_decorator(login_required, name='dispatch')
# class AnnouncementUpdateView(FormView):
#     """
#         View to create an announcement
#     """
#     form_class = AnnouncementLanguageForm

    # def _get_env(self, *args, **kwargs):
    #     return get_object_or_404(Announcement, url=kwargs['announcement_url'])

    # def get(self, request, *args, **kwargs):
    #     super(AnnouncementUpdateView, self).get(request, args, kwargs)

    # def get_form_kwargs(self):
    #     kwargs = super(AnnouncementCreationView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

class AnnouncementPurchaseView(TemplateView):
    """
        View to buy NL
    """
    pass