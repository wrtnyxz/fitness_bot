from django.db import models

class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(unique=True, verbose_name="ID")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self):
        return str(self.chat_id)

class UserLog(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, verbose_name="Юзер")
    action = models.CharField(max_length=255, verbose_name="Действие")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время")

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"