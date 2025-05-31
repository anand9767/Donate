from django.db import models

# Create your models here.


class DeleteAccountRequest(models.Model):
    reasonForDelete = models.TextField()
    requestStatus = models.BooleanField(default=False)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'api_deleteaccountrequest'
