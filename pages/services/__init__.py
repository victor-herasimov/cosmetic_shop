"""
Пакет сервісного шару (Service Layer) додатка.

Об'єднує та експортує класи-сервіси, які інкапсулюють бізнес-логіку
та взаємодію з даними, ізолюючи контролери (views) від прямої роботи з ORM.
"""

from .document import DocumentService

__all__ = ["DocumentService"]
