from turtle import title
from django.urls import reverse
from django.test import TestCase
from .models import  Book
from users.models import CustomUserModel

# Create your tests here.
class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No books found.')

    def test_book_list(self):
        book1 = Book.objects.create(title='Book1', description="Descrition1", isbn='1234561')
        book2 = Book.objects.create(title='Book2', description="Descrition2", isbn='1234562')
        book3 = Book.objects.create(title='Book3', description="Descrition3", isbn='1234563')

        response = self.client.get(reverse("books:list") + "?page_size=2")

        books = [book1, book2]
        for x in books:
            self.assertContains(response, x.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")
        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title='Book1', description="Descrition1", isbn='1234561')
        response = self.client.get(reverse('books:detail', kwargs={'id':book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)


    def test_search_book(self):
        book1 = Book.objects.create(title='Book1', description="Descrition1", isbn='1234561')
        book2 = Book.objects.create(title='Book2', description="Descrition2", isbn='1234562')
        book3 = Book.objects.create(title='Book3', description="Descrition3", isbn='1234563')

        response = self.client.get(reverse('books:list') + "?q=Book1")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=Book2')
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)


        response = self.client.get(reverse('books:list') + '?q=Book3')
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='123123')
        user = CustomUserModel.objects.create(
            username = 'Coder',
            first_name = 'Jasurbek',
            last_name = 'Odilov',
            email = 'abc@gmail.com',
        )
        user.set_password('abc123')
        user.save()
        self.client.login(
            username='Coder',
            password='abc123',
            )

        self.client.post(reverse('books:reviews', kwargs={'id':book.id}), data={
            'stars_given':3,
            'comment':'Nice book',
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'Nice book')
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)
