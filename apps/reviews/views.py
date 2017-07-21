from django.shortcuts import render, HttpResponse
from ..log_reg.forms import LoginForm, RegistrationForm
from django.core.urlresolvers import reverse


# Create your views here.
def logreg(request):
    login_form = LoginForm()
    reg_form = RegistrationForm()
    request.session['err_back'] = reverse('review:logreg')
    request.session['reg_back'] = reverse('review:logreg')
    request.session['redirect'] = reverse('review:landing')
    if 'reg_form_err' in request.session:
        reg_form = RegistrationForm(request.session['reg_form_err'])
        reg_form.is_valid()
        del request.session['reg_form_err']
    if 'login_form_err' in request.session:
        login_form = LoginForm(request.session['login_form_err'])
        login_form.is_valid()
        del request.session['login_form_err']
    context = {
        'login_form': login_form,
        'reg_form': reg_form,
    }
    return render(request, 'reviews/logreg.html', context)

def landing(request):
    return HttpResponse('hello world')
