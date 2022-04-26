from django.db import models


class User(models.Model):
    id_of_user = models.AutoField(primary_key=True)
    email_of_user = models.CharField(max_length=70, blank=True, null=True)
    password_of_user = models.CharField(max_length=250, blank=True, null=True)
    fio_of_user = models.CharField(max_length=100, blank=True, null=True)
    id_of_role = models.ForeignKey('RoleOfUser', models.DO_NOTHING, db_column='id_of_role', blank=True, null=True)

    class Meta:
        managed = False
        db_table = '_user_'


class Post(models.Model):
    id_of_post = models.AutoField(primary_key=True)
    text_of_post = models.CharField(max_length=400, blank=True, null=True)
    datetime_of_post = models.DateTimeField(blank=True, null=True)
    id_of_author = models.ForeignKey(User, models.DO_NOTHING, db_column='id_of_author', blank=True, null=True)
    id_of_status = models.ForeignKey('Status', models.DO_NOTHING, db_column='id_of_status', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'


class RoleOfUser(models.Model):
    id_of_role = models.AutoField(primary_key=True)
    name_of_role = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role_of_user'


class Status(models.Model):
    id_of_status = models.AutoField(primary_key=True)
    name_of_status = models.CharField(max_length=70, blank=True, null=True)

    def __str__(self):
        return self.name_of_status

    class Meta:
        managed = False
        db_table = 'status'
