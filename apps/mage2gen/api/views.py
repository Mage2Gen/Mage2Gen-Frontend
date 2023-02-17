from apps.mage2gen.models import Module
from mage2gen3 import Snippet
from rest_framework import (
    viewsets,
    mixins,
    response,
    status
)
from .serializers import GeneratorSerializer


class GeneratorView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = GeneratorSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Module.objects.filter(user=self.request.user).order_by("-created_at")
        return []

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.pk)


class SnippetsViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        snippets = self.get_snippets()
        snippet_name = kwargs.get('snippet_name')
        if snippet_name and snippet_name in snippets:
            snippets = snippets[snippet_name]
        return response.Response(snippets, status=status.HTTP_200_OK)

    def param_input(self, param):
        if not isinstance(param, str):
            default_value = param.default if hasattr(param, 'default') and param.default else ''
            required = True if hasattr(param, 'required') and param.required else ''

            if param.yes_no:
                required = True
                default_value = 1 if param.default else 0

            return {
                'message': param.name_label(),
                'name': param.name,
                'default': default_value,
                'required': str(required),
                'type': 'input' if param.yes_no else 'boolean'
            }
        return False

    def get_snippets(self):
        snippets = {}
        for snippet in Snippet.snippets():
            params = []
            for param in snippet.params():
                input = self.param_input(param)
                if input:
                    params.append(input)
            extra_params = []
            for param in snippet.extra_params():
                input = self.param_input(param)
                if input:
                    extra_params.append(input)
            snippets[snippet.name().lower()] = {
                'code': snippet.name().lower(),
                'label': snippet.label(),
                'name': snippet.name(),
                'extra_params': extra_params,
                'params': params,
            }
        return snippets