from django.test import TestCase

# Create your tests here.
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BBS.settings")
    import django
    django.setup()
    from app01 import models
    title = models.UserInfo.objects.filter(username="alias").values("blog__site_title")

    print(title)