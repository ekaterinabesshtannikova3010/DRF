from rest_framework import serializers


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not value.startswith("https://www.youtube.com/"):
            raise serializers.ValidationError("Ссылки на сторонние ресурсы, кроме youtube.com, не допускаются.")
