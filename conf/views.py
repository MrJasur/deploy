from django.shortcuts import render
from books.models import Book, BookReview
from django.core.paginator import Paginator

def landing_page(request):                  
    return render(request, 'landing.html')

def home_page(request):
    book_review = BookReview.objects.all().order_by('-created_at')

    # paginator
    page_size = request.GET.get('page_size', 6)
    paginator = Paginator(book_review, page_size)
    page_num = request.GET.get('page', 1)

    page_obj = paginator.get_page(page_num)
    context = {
        'book_review':book_review,
        'page_obj':page_obj
    }
    return render(request, 'home.html', context)