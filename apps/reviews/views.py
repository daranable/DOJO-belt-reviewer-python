from django.shortcuts import render, HttpResponse, redirect
from ..log_reg.forms import LoginForm, RegistrationForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from .forms import ReviewForm, AddBookReview
from .models import Book, Author, Review
from ..log_reg.models import User
from django.db.models import Count

def get_user(request):
    return User.objects.get(id=request.session['user']['id'])

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
    if 'user' not in request.session:
        return redirect(reverse('review:logreg'))
    request.session['logout_redirect'] = reverse('review:logreg')
    context = {
        'all_books': Book.objects.all(),
        'recent_reviews': Review.objects.all().order_by('-created_at')[:3],
    }
    return render(request, 'reviews/landing.html', context)

def add_all(request):
    if 'user' not in request.session:
        return redirect(reverse('review:logreg'))
    book_form = AddBookReview()
    if request.method == 'POST':
        data = {}
        for k, v in request.POST.iteritems():
            data[k] = v
        data['user'] = get_user(request)
        book_form = AddBookReview(data)
        if book_form.is_valid():
            review = book_form.save()
            messages.success(request, 'Successfully added new book and review.')
            return redirect(reverse('review:book', kwargs={'id':review.book.id}))
    context = {
        'form': book_form,
        'select_fields': ('author', 'rating')
    }
    return render(request, 'reviews/addall.html', context)

def show_book(request, id):
    if 'user' not in request.session:
        return redirect(reverse('review:logreg'))
    book = Book.objects.get(id=id)
    review_form = ReviewForm()
    if request.method == 'POST':
        data = {}
        for k, v in request.POST.iteritems():
            data[k] = v
            if k == 'rating':
                data[k] = int(v.encode())
        data['book'] = book
        data['user'] = get_user(request)
        print data
        review_form = ReviewForm(data)
        if review_form.is_valid():
            review_form.save()
            messages.success(request, 'Review added')
            return redirect(reverse('review:book', kwargs={'id': book.id}))
    context = {
        'form': review_form,
        'book': book,
        'select_fields': ('rating'),
    }
    return render(request, 'reviews/book.html', context)

def show_user(request, id):
    if 'user' not in request.session:
        return redirect(reverse('review:logreg'))
    user = User.objects.get(id=id)
    reviewed_books = Book.objects.filter(reviews__user=user).annotate(Count('name'))
    context = {
        'user': user,
        'books': reviewed_books,
        'review_count': len(user.reviews.all()),
    }
    return render(request, 'reviews/profile.html', context)
