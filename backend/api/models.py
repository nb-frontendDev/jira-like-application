from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import uuid


def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.user_profile.id) + str(".") + str(ext)])


class Profile(models.Model):
    # OneToOneField(1対1の関係)
    user_profile = models.OneToOneField(
        User, related_name='user_profile',
        # CASCADE使用。モデルが削除されると削除される
        on_delete=models.CASCADE
    )
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)
    
    def __str__(self):
        return self.user_profile.username


class Category(models.Model):
    item = models.CharField(max_length=100)

    def __str__(self):
        return self.item


class Task(models.Model):
    # status変数で使用
    STATUS = (
        ('1', 'Not started'),
        ('2', 'On going'),
        ('3', 'Done'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    task = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    criteria = models.CharField(max_length=100)
    # choices=STATUSで3つの選択肢のから選択できる。STATUS変数内に格納。defaultは１=Notstarted
    status = models.CharField(max_length=40, choices=STATUS, default='1')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # estimateは数字を扱うのでIntegerFieldを使用。MinValueValidatordeで0以上の整数のみを受け付ける
    estimate = models.IntegerField(validators=[MinValueValidator(0)])
    # ForeignKeyを使用し、Userモデルと紐付け。
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    # ForeignKeyを使用し、Userモデルと紐付け。
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible')
    # DateTimeField使用。auto_now_addでその時刻データをデータベースへ保管
    created_at = models.DateTimeField(auto_now_add=True)
    # DateTimeField使用。aauto_nowは更新した時刻をデータ保管
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task