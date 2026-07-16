from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from .models import Category, Item, Review
from main.EthiopianDate import gregorian_to_ethiopian, ethiocal
from django.db.models import Q
def shop(request):
    items = Item.objects.all()
    categories = Category.objects.all()
    for item in items:
        g_day = item.created_at.day
        g_month = item.created_at.month
        g_year = item.created_at.year

        eth_day, eth_month, eth_year = gregorian_to_ethiopian(g_day, g_month, g_year)
        weekday_name = ethiocal(eth_day, eth_month, eth_year)

        item.ethiopian_date = f"{eth_day}/{eth_month}/{eth_year}"
        item.ethiopian_weekday = weekday_name
    context = {
        'items': items,
        'categories': categories,}
    return render(request, 'shop/index.html', context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    reviews = Review.objects.filter(item_name=item)
    showreviews = Review.objects.filter(item_name=item)
    reviewed = None
    if request.user.is_authenticated:
        reviewed = Review.objects.filter(user= request.user, item_name = item).first()
    if request.method == 'POST':
        if request.user.is_authenticated:
            rating = request.POST.get('rating')
            review_text = request.POST.get('review')
            if rating and review_text:
                try:
                    Review.objects.create(
                        user=request.user,
                        item_name=item,
                        rating=int(rating),
                        review=review_text
                    )
                except:
                    return HttpResponse('You have reviewed this item.')
                return redirect('success')
        else:
            return redirect('login') 
    print(item.item_category)
    return render(request, 'shop/detail.html', {
        'items': item,
        'reviews': reviews,
        'showreviews':showreviews,
        'reviewed':reviewed,
    })

def search(request):
    query = request.GET.get('q')
    items = Item.objects.all()
    if query:
        items = items.filter(
            Q(item_name__icontains=query) |
            Q(description__icontains=query) |
            Q(item_category__category_name__icontains=query)
        ).distinct()
    # print(items)
    return render(request, 'main/search.html', {
        'items': items,
        'query': query,
    })
def success(request):
    return render(request, 'main/success.html')