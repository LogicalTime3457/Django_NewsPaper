from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals


# red = redis.Redis(
#     host = 'redis-19217.c100.us-east-1-4.ec2.cloud.redislabs.com',
#     port = 19217,
#     password = 'xVSkwcgkfDCI4fAVoR3W5GKgbhGknBbX'
# )

