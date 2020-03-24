import inspect

import django
from django.contrib import admin

from . import models


excludes = [
    'User',
]


def get_models(models_module, excludes: list = None):
    model_classes = filter(lambda c: isinstance(c[1], django.db.models.base.ModelBase), inspect.getmembers(models_module, inspect.isclass))
    model_classes = filter(lambda c: not c[1]._meta.abstract, model_classes)
    model_classes = filter(lambda c: c[0] not in excludes, model_classes)
    model_classes = list(map(lambda c: c[1], model_classes))
    return model_classes


for model in get_models(models, excludes=excludes):
    admin.site.register(model)

#admin.site.register(Document)
#admin.site.register(Payment)
#admin.site.register(UserClient)
#admin.site.register(Membership)
#admin.site.register(Category)
#admin.site.register(Data)
#admin.site.register(Field)
