import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.contrib import admin

from .models import Category, Tag, Blog


admin.site.register([Category, Tag, Blog])
