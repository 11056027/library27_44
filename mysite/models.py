from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200,null=True)
    author=models.CharField(max_length=50)
    chapter = models.TextField()
    pub_date = models.DateTimeField()
    content = models.TextField()
    imgcode=models.URLField(max_length=200, null=True, blank=True)
    place=models.CharField(max_length=5,choices=[("藏書中","藏書中"),("外借中","外借中")],default="藏書中")
    

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    password_confirm = models.CharField(max_length=255)

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="custom_users",  
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_users",
    )

    def __str__(self):
        return self.username

class CustomGroup(Group):
    user_set = models.ManyToManyField(
        CustomUser,
        related_name="custom_groups", 
        blank=True,
        help_text="The users that belong to this group.",
        verbose_name="users",
    )
    
class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)