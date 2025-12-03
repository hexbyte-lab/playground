from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Lesson(models.Model):
    CATEGORY_CHOICES = [
        ('basics', 'مبانی'),
        ('data_structures', 'ساختارهای داده'),
        ('algorithms', 'الگوریتم‌ها'),
        ('interviews', 'مصاحبه‌ها'),
        ('other', 'سایر'),
    ]
    
    
    title = models.CharField("عنوان", max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField("توضیحات")
    code_snippet = models.TextField("کد نمونه", blank=True)
    image = models.ImageField("عکس (اختیاری)", upload_to='lessons/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    category = models.CharField("دسته‌بندی", max_length=50, choices=CATEGORY_CHOICES, default='other')
    author = models.CharField("نویسنده", max_length=100, default='Rafi')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "درس"
        verbose_name_plural = "درس‌ها"

    def __str__(self):
        return self.title
