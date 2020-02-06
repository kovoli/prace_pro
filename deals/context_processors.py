from .models import Category


# ---------- Список категорий  -----------------------
def menu(context):  # аргумент context передается в контекст прцесс
    categories = Category.objects.root_nodes()  # Извлекаю все категории
    return {'categories': categories}  # Передаю словарь с содержание категорий
