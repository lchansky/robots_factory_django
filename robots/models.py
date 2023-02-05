from datetime import datetime
import re

from django.db import models
from django.core.exceptions import ValidationError


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    def custom_validation(self):
        if not re.match(r'^[A-Z0-9]{2}-[A-Z0-9]{2}$', self.serial):
            raise ValidationError('Model and Version must be 2 and 2 chars, like 11-XX or R3-D4 or RR-RR')
        if self.serial != f'{self.model}-{self.version}':
            raise ValidationError('Wrong serial name! It must be like "model-version"!')
        if self.created > datetime.now(self.created.tzinfo):
            raise ValidationError('Field "created" must be littler than current time')

    def clean(self, *args, **kwargs):
        self.custom_validation()
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.serial and isinstance(self.model, str) and isinstance(self.version, str):
            self.serial = self.model + '-' + self.version
        self.full_clean()
        super().save(*args, **kwargs)
