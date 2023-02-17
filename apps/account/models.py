from django.db import models
from django.conf import settings
from apps.mage2gen.models import BaseModel 

class License(BaseModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='licenses', null=True, blank=True, on_delete=models.SET_NULL)
	license_short_text = models.TextField(default='')
	license_text = models.TextField(default='')
