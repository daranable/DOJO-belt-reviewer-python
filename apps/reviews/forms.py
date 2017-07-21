from django import forms
from django.forms import ModelForm
from .models import Author, Book, Review
from django.core import validators
import re

class ReviewForm(forms.Form):
    # class Meta:
    #     model = Review
    #     fields = ['review', 'book', 'rating']
    #     widgets = {
    #         'review': forms.Textarea(attrs={'class': 'mdl-textfield__input'}),
    #         'book': forms.HiddenInput(),
    #     }
    #     labels = {
    #         'book': '',
    #     }
    review= forms.CharField(
        widget=forms.Textarea(attrs={'class': 'mdl-textfield__input'}),
        validators=[
            validators.MinLengthValidator(20)
        ]
    )
    rating= forms.ChoiceField(
        widget=forms.Select(),
        choices=([0,0],[1,1],[2,2],[3,3],[4,4],[5,5])
    )

    def clean(self):
        cleaned_data = super(ReviewForm, self).clean()
        print cleaned_data

    def save(self):
        book = self.data['book']
        user = self.data['user']
        Review.objects.create(review=self.cleaned_data.get('review'), rating=self.cleaned_data.get('rating'), book=book, user=user)

class AddBookReview(forms.Form):
    name= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
        label='Book Title',
        validators=[validators.MinLengthValidator(2)]
    )
    author= forms.ModelChoiceField(
        label='Existing Author',
        queryset=Author.objects.all(),
        required=False,
    )
    newauthor= forms.CharField(
        label="or add new Author",
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
        validators=[
            validators.MinLengthValidator(5),
        ],
        required=False,
    )
    review= forms.CharField(
        widget=forms.Textarea(attrs={'class': 'mdl-textfield__input'}),
        validators=[
            validators.MinLengthValidator(20)
        ]
    )
    rating= forms.ChoiceField(
        widget=forms.Select(),
        choices=([0,0],[1,1],[2,2],[3,3],[4,4],[5,5])
    )

    def clean(self):
        cleaned_data = super(AddBookReview, self).clean()
        authfield = cleaned_data.get('author')
        newauth = cleaned_data.get('newauthor')

        if not authfield and newauth and len(newauth) < 5:
            self.add_error('author', 'Must specify author')
            self.add_error('newauthor', 'Must specify author')
        if newauth and len(newauth) and not re.match(r'^\w+ \w+$', newauth):
            self.add_error('newauthor', 'Author name must have first and last names')

    def save(self):
        author = self.cleaned_data.get('author')
        if not author:
            newauth = self.cleaned_data.get('newauthor')
            newauth = newauth.split(' ')
            first_name = newauth[0]
            last_name = newauth[1]
            try:
                author = Author.objects.get(first_name=first_name, last_name=last_name)
            except:
                author = Author.objects.create(first_name=first_name, last_name=last_name)
        book = self.cleaned_data.get('name')
        book_obj = None

        try:
            book_obj = Book.objects.create(name=book, author=author)
        except:
            book_obj = Book.objects.get(name=book)
        rating = self.cleaned_data.get('rating')
        review = self.cleaned_data.get('review')
        review = Review.objects.create(rating=rating, review=review, book=book_obj, user=self.data['user'])
        return review
