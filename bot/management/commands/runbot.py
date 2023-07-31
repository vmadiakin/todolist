from django.conf import settings
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory


class Command(BaseCommand):
    help = "run bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        tg_user.set_verification_code()
        tg_user.save(update_fields=["verification_code"])
        self.tg_client.send_message(
            msg.chat.id, f"[Код подтверждения] {tg_user.verification_code}"
        )

    def fetch_tasks(self, msg: Message, tg_user: TgUser):
        gls = Goal.objects.filter(user=tg_user.user)
        if gls.count() > 0:
            resp_msg = [f"#{item.id} {item.title}" for item in gls]
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))
        else:
            self.tg_client.send_message(msg.chat.id, "[У вас еще нет ни одной цели :(]")

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if not msg.text:
            return
        if "/goals" in msg.text:
            self.fetch_tasks(msg, tg_user)
        elif "/create" in msg.text:
            self.handle_create_command(msg, tg_user)
        else:
            self.tg_client.send_message(msg.chat.id, "[Неизвестная команда]")

    def handle_create_command(self, msg: Message, tg_user: TgUser):
        tg_user.state = self.STATE_WAITING_CATEGORY
        tg_user.save(update_fields=["state"])

        user_categories = GoalCategory.objects.filter(user=tg_user.user)

        if user_categories.exists():
            categories_text = "\n".join([category.title for category in user_categories])
            self.tg_client.send_message(msg.chat.id, "[Выберите категорию:]\n" + categories_text)
        else:
            self.tg_client.send_message(msg.chat.id, "[У вас еще нет категорий. Создайте новую категорию.]")

    def handle_category_input(self, msg: Message, tg_user: TgUser):
        category_input = msg.text.strip()

        existing_categories = GoalCategory.objects.filter(user=tg_user.user, title=category_input)

        if not existing_categories.exists():
            self.tg_client.send_message(msg.chat.id, "[Несуществующая категория. Попробуйте еще раз.]")
            return

        tg_user.goal_category = existing_categories.first()
        tg_user.state = self.STATE_WAITING_GOAL_NAME
        tg_user.save(update_fields=["goal_category", "state"])

        self.tg_client.send_message(msg.chat.id, "[Введите название новой цели:]")

    def handle_goal_name_input(self, msg: Message, tg_user: TgUser):
        goal_name = msg.text.strip()

        new_goal = Goal.objects.create(user=tg_user.user, title=goal_name, category=tg_user.goal_category)

        tg_user.state = self.STATE_DEFAULT
        tg_user.goal_category = None
        tg_user.save(update_fields=["state", "goal_category"])

        self.tg_client.send_message(msg.chat.id, f"[Цель создана: #{new_goal.id} {new_goal.title}]")

    def handle_cancel_command(self, msg: Message, tg_user: TgUser):
        tg_user.state = self.STATE_DEFAULT
        tg_user.goal_category = None
        tg_user.save(update_fields=["state", "goal_category"])

        self.tg_client.send_message(msg.chat.id, "[Операция отменена пользователем.]")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_id=msg.from_.id,
            defaults={
                "tg_chat_id": msg.chat.id,
                "username": msg.from_.username,
            },
        )
        if created:
            self.tg_client.send_message(msg.chat.id, f"[Приветствую вас, {msg.from_.username}]")

        if tg_user.user:
            if tg_user.state == self.STATE_WAITING_CATEGORY:
                self.handle_category_input(msg, tg_user)
            elif tg_user.state == self.STATE_WAITING_GOAL_NAME:
                self.handle_goal_name_input(msg, tg_user)
            elif "/cancel" in msg.text:
                self.handle_cancel_command(msg, tg_user)
            else:
                self.handle_verified_user(msg, tg_user)
        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle(self, *args, **kwargs):
        self.STATE_DEFAULT = 0
        self.STATE_WAITING_CATEGORY = 1
        self.STATE_WAITING_GOAL_NAME = 2

        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)
