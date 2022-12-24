from django.contrib import admin
from .models import Category, Task, Profile

# 確認したいモデルを登録する。admin.site.register(クラス名)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Profile)
