import uuid, os

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify

from core.utils import get_current_year
from sneakers.validators import validate_filetype, validate_filesize


class Brand(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, 
        primary_key=True, 
        unique=True, 
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    country = models.CharField(max_length=100, null=True, blank=True)
    year_founded = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(get_current_year())
        ],
        null=True,
        blank=True,
    )


    def __str__(self):
        return self.name


class Sneaker(models.Model):

    def _generate_file_path(self, filename: str) -> str:
        """
        Generates a unique, sanitized file path for uploaded images.
        Example: sneakers/2025/07/14/air-jordan-1-a1b2c3d4.jpg
        """

        extension = os.path.splitext(filename)[1]
        safe_base_name = slugify(self.name) if self.name else 'sneaker'
        unique_id = uuid.uuid4().hex[:8]

        new_filename = f"{safe_base_name}-{unique_id}{extension.lower()}"

        today = timezone.now()
        return os.path.join(
            'sneakers',
            today.strftime('%Y'),
            today.strftime('%m'),
            today.strftime('%d'),
            new_filename
        )


    id = models.UUIDField(
        default=uuid.uuid4, 
        primary_key=True, 
        unique=True, 
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
    )
    name = models.CharField(max_length=100)
    summary = models.TextField(max_length=200)
    designer = models.CharField(max_length=150, null=True, blank=True)
    year_released = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(get_current_year())
        ]
    )

    related_sneakers = models.ManyToManyField('self', blank=True)

    primary_image = models.ImageField(
        upload_to=_generate_file_path,
        validators=[validate_filetype, validate_filesize],
        null=True,
        blank=True
    )


    class Meta:
        verbose_name = 'Sneaker'
        verbose_name_plural = 'Sneakers'


    def __str__(self):
        return self.name
