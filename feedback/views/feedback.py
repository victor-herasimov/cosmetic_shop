from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from feedback.forms import FeedbackForm
from feedback.services import FeedbackService


class FeedbackCreateView(View):
    """
    Class-Based View для обробки та збереження форм зворотного зв'язку через HTMX.

    Приймає виключно POST-запити. У разі успішної валідації повертає порожню
    відповідь із тригером для фронтенду. Якщо форма невалідна — повертає HTML
    форми з помилками та HTTP-статусом 422.
    """

    feedback_service_class = FeedbackService
    template_name = "feedback/includes/feedback_form.html"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обробляє POST-запит із даними форми зворотного зв'язку.

        Args:
            request (HttpRequest): Об'єкт поточного HTTP-запиту.

        Returns:
            HttpResponse: Порожня відповідь із заголовком 'HX-Trigger' при успіху
            або відрендерений фрагмент форми з помилками (статус 422).
        """
        form: FeedbackForm = FeedbackForm(request.POST)

        if form.is_valid():
            feedback_service: FeedbackService = self.feedback_service_class()
            feedback_service.create(form.cleaned_data)
            response: HttpResponse = render(
                request, self.template_name, {"feedback_form": FeedbackForm()}
            )
            response["HX-Trigger"] = "successFeedback"
            return response

        return render(
            request,
            self.template_name,
            {"feedback_form": form},
            # status=422,
        )
