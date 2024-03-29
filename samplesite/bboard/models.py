from django.db import models


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рубрика"
        verbose_name_plural = "Рубрики"
        ordering = ["name"]


class Bb(models.Model):
    rubric = models.ForeignKey(Rubric, null=True, on_delete=models.PROTECT, verbose_name="Рубрика")
    title = models.CharField(max_length=50)
    content = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    
    def get_rubric(self):
        return self.rubric.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-published"]
