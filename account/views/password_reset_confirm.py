from django.contrib.auth.views import PasswordResetConfirmView
from django.http import HttpResponse
from django.shortcuts import render


class AsyncPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    template_form = "account/includes/set_password_form.html"

    def form_valid(self, form) -> HttpResponse:
        form.save()
        # Todo save across service
        response: HttpResponse = render(
            self.request, "account/includes/_password_reset_confirm_success.html"
        )
        response["HX-Trigger"] = "password_reset_confirm_success"
        return response

    def form_invalid(self, form) -> HttpResponse:
        print("form invalid")
        response: HttpResponse = render(
            self.request, self.template_form, {"form": form}
        )
        response["HX-Retarget"] = "#passwordResetConfirmForm"
        return response
