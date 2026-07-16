from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class Category(models.Model):
    category_id = models.AutoField(name = 'CategoryId', primary_key=True)
    category_name = models.CharField(name='category_name', max_length=50, null=False, blank=False)
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return f'{self.category_name}'


class Item(models.Model):
    item_name = models.CharField(name='item_name', max_length=50, blank=False,null=False)
    item_category = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    item_image = models.ImageField(upload_to='item_images',name = 'item_image', null=True , blank=True)
    inventory = models.IntegerField(name='inventory',blank=False, null=False,default= 0)
    choice = [('male','male'),('female','female'),('both','both'),]
    gender = models.CharField(choices=choice, null=False, blank=False,default=choice[0][0])
    price = models.FloatField(name='price', null=False, blank=False, default= 0)
    # created_by = models.ForeignKey(User, related_name='item', on_delete=models.CASCADE)  // later on if a user can sell an item in the site
    is_sold = models.BooleanField(default=False)
    # in_stock = models.IntegerField(name='in_stock', default= 0,null=False, blank=False)
    description = models.TextField(name='description', max_length=255, null=True, blank = True)
    class Meta:
        verbose_name_plural = 'Items'
    def __str__(self):
        return self.item_name

# class Inventory(models.Model):
#     item_name = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='inventories')
#     in_stock = models.IntegerField(name='instock', blank=False, null=False)
#     class Meta:
#         verbose_plural_name = 'inventories'
#     def __str__(self):
        # return self.item_name

class Review(models.Model):
    review_choices =[
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='reviews')
    item_name = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    rating = models.SmallIntegerField(choices=review_choices, validators=[MinValueValidator(1),MaxValueValidator(5)])
    review = models.TextField(name='review')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','item_name')
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.user} for {self.item_name} ({self.rating})"