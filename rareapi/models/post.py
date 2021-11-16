from django.db import models

class Post(models.Model):
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    publication_date = models.DateField()
    image_url = models.URLField()
    content = models.CharField(max_length=100)
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="tags")