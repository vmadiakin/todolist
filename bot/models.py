import random

from django.db import models

CODE_VOCABULARY = "qwertyuasdfghkzxvbnm123456789"


class TgUser(models.Model):
    tg_id = models.BigIntegerField(verbose_name="tg id", unique=True)
    tg_chat_id = models.BigIntegerField(verbose_name="tg chat id")
    username = models.CharField(
        max_length=512, verbose_name="tg username", null=True, blank=True, default=None
    )
    user = models.ForeignKey(
        "core.User",
        models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name="связанный пользователь",
    )
    verification_code = models.CharField(
        max_length=32, verbose_name="код подтверждения"
    )

    class Meta:
        verbose_name = "tg пользователь"
        verbose_name_plural = "tg пользователи"

    def set_verification_code(self):
        code = "".join([random.choice(CODE_VOCABULARY) for _ in range(12)])
        self.verification_code = code
