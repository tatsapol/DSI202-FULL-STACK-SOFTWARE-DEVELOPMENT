from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    pic=models.ImageField(null=True, blank=True)
    user = models.OneToOneField( User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=5)
    mobile = models.CharField(max_length=20,blank=True)
    email = models.EmailField()
    

    def __str__(self):
        return "%s"%(self.user)

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('update_profile_signal: create a profile')

class Item(models.Model):
    title = models.CharField(max_length=100)
    unit = models.CharField(max_length=5)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2) #999.99
    image=models.ImageField(null=True, blank=True) #from week05
    description=models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return "%s , %s "%(self.title, self.unit)


class Order_Item(models.Model):
    profile = models.ForeignKey( Profile, on_delete=models.CASCADE)
    item = models.ForeignKey( Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return "profile:%s, item:%s, quantity:%s, unit: %s, unit_price:%s"%(self.profile.name,self.item, self.quantity, self.item.image, self.item.unit_price)

class Record_Order(models.Model):
    profile = models.ForeignKey( Profile, on_delete=models.CASCADE)
    item = models.ForeignKey( Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return "profile:%s, item:%s, quantity:%s, unit: %s, unit_price:%s"%(self.profile.name,self.item, self.quantity, self.item.image, self.item.unit_price)
