import json

from todo_api.renderers import ToDoJsonRenderer


class UserJsonRenderer(ToDoJsonRenderer):
    object_label = 'user'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        token = data.get('token', None)

        return super(UserJsonRenderer, self).render(data)
