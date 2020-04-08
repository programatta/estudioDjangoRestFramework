class AWSCustomDefaultField(object):
    def set_context(self, serializer_field):
        self.request = serializer_field.context['request']


class AWSDefaultFieldCurrentUser(AWSCustomDefaultField):
    def __call__(self):
        return self.request.user.id
