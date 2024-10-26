# utils/mixins.py or core/mixins.py

from rest_framework import viewsets

class ContextMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context