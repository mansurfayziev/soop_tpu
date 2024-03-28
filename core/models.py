from django.db import models

class RoomNumber(models.Model):
    username = models.CharField(max_length=255)
    number = models.IntegerField()

    def __str__(self):
        return f'{self.username} ({self.number})'

class Violation(models.Model):
    room = models.IntegerField(blank=False)
    fio = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField( null=True, blank=True)
    soop_fio =models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.room}'


class Akt(models.Model):
    room = models.IntegerField(blank=False)
    fio = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField( null=True, blank=True)
    soop_fio =models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.room}'




