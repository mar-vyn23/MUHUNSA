from django.db import models
from accounts.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(default="", max_length=30)
    desc = models.TextField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category

class Blog(models.Model):
    slug = models.SlugField(unique=True, null=False, blank=False, max_length=100)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    content = RichTextField()
    thumbnail = models.ImageField(upload_to="thumbnails/%Y/%m/%d/")
    views = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name="blogs")
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    published_on = models.DateTimeField(auto_now_add=True)
    pdf_upload = models.FileField(upload_to="documents/%Y/%m/%d/", validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])], null=True)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="blogs", null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

class Comment(models.Model):
    comment = models.TextField()
    likes = models.IntegerField(default=0)
    blog = models.ForeignKey(to=Blog, on_delete=models.SET_NULL, related_name="comments", null=True)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="comments", null=True)
    published_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.comment

class Reply(models.Model):
    reply = models.TextField()
    likes = models.IntegerField(default=0)
    comment = models.ForeignKey(to=Comment, on_delete=models.SET_NULL, related_name="replies", null=True, blank=True)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="replies", null=True)
    published_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.reply

class Bookmark(models.Model):
    blog = models.ForeignKey(to=Blog, on_delete=models.SET_NULL, related_name="bookmarks", null=True, blank=True)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="bookmarks", null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Bookmark({self.id}, {self.creater.username})"

class BlogLike(models.Model):
    blog = models.ForeignKey(to=Blog, on_delete=models.SET_NULL, related_name="likes", null=True, blank=True)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="likes", null=True, blank=True)

    def __str__(self):
        return f"BlogLike({self.id}, {self.creator.username})"
    

# photo gallery
class Photo(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Pub(models.Model):
    name = models.CharField(max_length=255, default='Unnamed')
    pdf_upload = models.FileField(upload_to="pubs/%Y/%m/%d/", validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])], null=True)
    modified_date = models.DateTimeField(auto_now=True)
    size = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if it's a new instance
            if self.file:
                # Calculate and set the file size
                self.size = self.file.size
                
        # Set the modified_date to the current East African Time
        self.modified_date = timezone.localtime(timezone.now())
        
        super().save(*args, **kwargs)