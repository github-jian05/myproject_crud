from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.urls import reverse
from django.conf import settings


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Add a unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Add a unique related_name
        blank=True,
    )

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=255, blank=True)
    contact_info = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Commission(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    commissioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Custom User model reference
        on_delete=models.CASCADE,
        related_name='commissions_created'
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def get_absolute_url(self):
        # Generates the appropriate detail URL for this Commission instance
        return reverse('commission-detail', args=[self.pk])
    # Other fields...from django.contrib.auth.mixins import LoginRequiredMixin


class Request(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed')],
        default='pending'
    )

    def __str__(self):
        return f"Request by {self.student.username} for {self.commission.title}"


class Review(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.commission.title}"
