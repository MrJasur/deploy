from rest_framework import serializers
from books.models import Book, BookReview, CustomUserModel


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ('id', 'first_name', 'last_name', 'email', 'username')

class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    book = BookSerializer(read_only = True)

    user_id = serializers.IntegerField(write_only = True)
    book_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = BookReview
        fields = ('id', 'stars_given', 'comment', 'book', 'user', 'user_id', 'book_id')


# agar Serializer ni ozidan foydalanganimizda quyidagi dek code yozar edik

# class BookReviewSerializer(serializers.Serializer):
#     stars_given = serializers.IntegerField(min_value=1, max_value=5)
#     comment = serializers.CharField()
#     book = BookSerializer()
#     user = UserSerializer()