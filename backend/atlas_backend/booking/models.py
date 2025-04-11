from django.db import models
""" Workspace Models """


class Workspace(models.Model):
    name = models.CharFiels(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharFiel
