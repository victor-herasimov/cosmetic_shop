from .models import Strip


class StripServise:
    def get_all(self) -> list[Strip]:
        return Strip.objects.all()
