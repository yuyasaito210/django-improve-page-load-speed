from .views_texts import global_texts, home_texts


def i18n(request):
    data = {}
    data.update(global_texts())
    return data