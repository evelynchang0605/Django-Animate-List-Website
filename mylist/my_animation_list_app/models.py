from django.db import models

# Create your models here.
class Animate(models.Model):
    title_text = models.CharField(max_length=200)
    zone_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    animate_photo = models.ImageField(upload_to='media/images/', default='media/images/oshinoko_img.jpeg')
    animate_description = models.TextField(blank=True)

    def __str__(self):
        return self.title_text

class Recommend(models.Model):
    title = models.ForeignKey(Animate, on_delete=models.CASCADE)
    recommend_text = models.CharField(max_length=200, default='1')
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.recommend_text
