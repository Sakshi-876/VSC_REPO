from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.student.user.username})"

class Payment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, default='Unpaid')
    due_date = models.DateField()
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.amount} ({self.status})"

class VisitorLog(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=100)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    purpose = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.visitor_name} visiting {self.student.user.username}"
