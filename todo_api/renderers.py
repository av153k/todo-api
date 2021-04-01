import json

from rest_framework.renderers import JSONRenderer


class ToDoJsonRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)

        if errors is None:
            return super(ToDoJsonRenderer, self).render(data)

        return json.dumps({
            self.object_label: data
        })
