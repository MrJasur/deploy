from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from books.models import Book, BookReview
from users.models import CustomUserModel

# Create your tests here.
class BookViewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUserModel.objects.create(username='Coder', first_name='Jasurbek')
        self.user.set_password('abc123')
        self.user.save()
        self.client.login(username='Coder', password='abc123')


    def test_book_review_detail(self):
        book = Book.objects.create(title="Harry Potter", description='written by Joane Rowling', isbn='123456')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good book")


        response = self.client.get(reverse('api:review_detail', kwargs={'id':br.id}))
        
        # review
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], 'very good book')
        # book
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Harry Potter')
        self.assertEqual(response.data['book']['description'], 'written by Joane Rowling')
        self.assertEqual(response.data['book']['isbn'], '123456')
        # user
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], 'Jasurbek')
        self.assertEqual(response.data['user']['username'], 'Coder')


    def test_book_review_list(self):
        user_two = CustomUserModel.objects.create(username='Coder2', first_name='Jasurbek')
        book = Book.objects.create(title="Harry Potter", description='written by Joane Rowling', isbn='123456')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good book")
        br2 = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good book too")

        response = self.client.get(reverse('api:review_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        # ikkinchi qoldirilgan review data[0] bn assertEqul ligini tekshiramiz
        #chunki biz View da order_by('-created_at') dan foydalnagnamiz
        self.assertEqual(response.data['results'][0]['id'], br2.id)
        self.assertEqual(response.data['results'][0]['stars_given'], br2.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br2.comment)
        # birinchi qoldirilgan review
        self.assertEqual(response.data['results'][1]['id'], br.id)
        self.assertEqual(response.data['results'][1]['stars_given'], br.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], br.comment)


    def test_delete_review(self):
        book = Book.objects.create(title="Harry Potter", description='written by Joane Rowling', isbn='123456')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good book")

        response = self.client.delete(reverse('api:review_detail', kwargs={'id':br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())


    # Update
    def test_patch_review(self):
        book = Book.objects.create(title="Harry Potter", description='written by Joane Rowling', isbn='123456')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good book")

        response = self.client.patch(reverse('api:review_detail', kwargs={'id': br.id}), data={'stars_given': 4})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)

    
    def test_put_review(self):
        book = Book.objects.create(title="Harry Potter", description='written by Joane Rowling', isbn='123456')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good book")

        response = self.client.put(reverse('api:review_detail', kwargs={'id':br.id}), 
        data = {
            'stars_given':4,
            'comment':'nice book',
            'user_id':self.user.id,
            'book_id':book.id
            }
        )
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'nice book')


    def test_create_view(self):
        book = Book.objects.create(title="Harry Potter", description='written by Joane Rowling', isbn='123456')
        data = {
            'stars_given':3,
            'comment':'good book',
            'user_id':self.user.id,
            'book_id':book.id
        }

        response = self.client.post(reverse('api:review_list'), data=data)
        br=BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 3)
        self.assertEqual(br.comment, 'good book')
