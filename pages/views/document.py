"""
Модуль для відображення статичних та юридичних документів сайту.
"""

from django.http import Http404
from django.views.generic import DetailView
from solo.models import SingletonModel
from pages.models import PrivacyPolicy, ReturnPolicy, DeliveryAndPayPolicy, PublicOffer
from pages.services import DocumentService


class DocumentView(DetailView):
    """
    Представлення для динамічного відображення синглтон-документів (політик).

    Клас обробляє запити до статичних юридичних чи інформаційних сторінок.
    Залежно від значення `doc_slug`, отриманого з URL, він визначає потрібну
    модель-синглтон, запитує її єдиний екземпляр через сервісний шар
    і передає в шаблон.
    """

    MODELS_MAP: dict[str, type[SingletonModel]] = {
        "privacy": PrivacyPolicy,
        "return": ReturnPolicy,
        "delivery": DeliveryAndPayPolicy,
        "public": PublicOffer,
    }
    template_name = "pages/document.html"
    context_object_name = "document"

    def get_object(self, queryset=None) -> SingletonModel:
        """
        Повертає єдиний екземпляр (Singleton) обраного документа.

        Метод зчитує параметр `doc_slug` з URL. Якщо slug валідний,
        викликається `DocumentService`, який повертає поточний активний
        запис цієї політики з бази даних.

        Args:
            queryset (QuerySet, optional): Необов'язковий базовий запит.
                Ігнорується, оскільки вибірка йде через Singleton-сервіс,
                але збережено для сумісності з сигнатурою Django DetailView.

        Returns:
            SingletonModel: Екземпляр моделі політики (напр., PrivacyPolicy),
                який буде доступний у шаблоні як `object` або `context_object_name`.

        Raises:
            Http404: Якщо переданий `doc_type` відсутній у карті `MODELS_MAP`.
        """
        doc_type: str = self.kwargs.get("doc_type")

        model_class: type[SingletonModel] = self.MODELS_MAP.get(doc_type)
        if model_class is None:
            raise Http404("Такого документа не існує.")
        return DocumentService(model_class).get()
