from django.db import models


class User(models.Model):
    uid = models.IntegerField(verbose_name='유저ID', primary_key=True)
    name = models.CharField(verbose_name="이름", max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'UserTable'
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Guild(models.Model):
    gid = models.IntegerField(verbose_name='길드ID', primary_key=True)
    name = models.CharField(verbose_name="이름", max_length=128)
    user = models.ManyToManyField(User, related_name='유저')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'GuildTable'
        verbose_name = 'guild'
        verbose_name_plural = 'guilds'
