from main.models import Strip


class StripService:
    def get_all(self) -> list[Strip]:
        return Strip.objects.all()
