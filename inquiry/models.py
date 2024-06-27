from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class INQUIRY_CHOICE(models.IntegerChoices):

    GENERAL = (0, 'General') # general inquiry


class Inquiry(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = PhoneNumberField(blank=True, null=True)

    datetime = models.DateTimeField(auto_now=True)

    inquiry_type = models.PositiveSmallIntegerField(choices=INQUIRY_CHOICE.choices, default=INQUIRY_CHOICE.GENERAL,  blank=True)

    description = models.TextField(max_length=1500)

    class Meta:

        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"

    def __str__(self) -> str:
        return f'{self.email}'