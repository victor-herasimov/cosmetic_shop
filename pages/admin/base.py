"""
Базові налаштування адмін-панелі для юридичних документів сайту.

Містить абстрактні або базові класи конфігурації Django Admin, які уніфікують
інтерфейс редагування офіційних угод та синглтон-моделей.
"""

from solo.admin import SingletonModelAdmin


class BaseLegalDocumentAdmin(SingletonModelAdmin):
    """
    Базова конфігурація адмін-панелі для моделей, що наслідують `BaseLegalDocument`.
    """

    save_on_top = True
    list_display = ["title"]
    list_display_links = ["title"]
    fields = ["title", "content", "updated", "created"]
    readonly_fields = ["updated", "created"]
