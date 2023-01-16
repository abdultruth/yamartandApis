from unicodedata import category


from .models import Cartegory


def menu_links(request):
    links = Cartegory.objects.all()
    return dict(links=links)
