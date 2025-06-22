# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

# std imports
import uuid

# django imports
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from model_utils.models import TimeStampedModel

# local imports
from core.managers import StatusMixinManager


class StatusMixin(models.Model):
    is_active = models.BooleanField(_("active"), default=True, blank=False, null=False)
    is_deleted = models.BooleanField(
        _("deleted"), default=False, blank=False, null=False
    )
    objects = StatusMixinManager()
    
    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()
    
    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()
    
    def remove(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()
    
    def has_changed(self, field):
        model = self.__class__.__name__
        return getattr(self, field) != getattr(
            self, "_" + model + "__original_" + field
        )
    
    def save(self, *args, **kwargs):
        """
        Makes sure that the ``is_active`` is ``False`` when ``is_deleted`` is ``True``.
        """
        if self.is_deleted:
            self.is_active = False
        super(StatusMixin, self).save(*args, **kwargs)
    
    class Meta:
        abstract = True


class UUIDMixin(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True


class EmailMixin(models.Model):
    email = models.EmailField(_("Email"), max_length=70,blank=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        abstract = True


class MobileMixin(models.Model):
    country_code = models.CharField(_("Phone Country Code"), max_length=55, null=True, blank=True)
    mobile_validator = RegexValidator(regex=r"^[1-9]\d{9}$", message="Invalid Phone Number")
    phone_number = models.CharField(_("Phone Number"), validators=[mobile_validator], max_length=15)
    
    class Meta:
        abstract = True
