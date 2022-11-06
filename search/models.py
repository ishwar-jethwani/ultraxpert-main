from django.db import models

# Create your models here.
class Search(models.Model):
    """Model Search For Searching Details"""
    query = models.CharField(max_length=5000,verbose_name="search by user",blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self) -> str:
        return self.query
    class Meta:
        ordering = ["-timestamp"]