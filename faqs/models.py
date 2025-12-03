from django.db import models

class FAQCategory(models.TextChoices):
    MARKETING_MATERIALS = "marketing_materials", "Marketing Materials"
    PROPERTY_VIEWINGS = "property_viewings", "Property Viewings"
    PROPERTY_MANAGEMENT = "property_management", "Property Management"
    COMMISSIONS = "commissions", "Commissions"
    TECHNICAL_SUPPORT = "technical_support", "Technical Support"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=FAQCategory.choices,
        default=FAQCategory.MARKETING_MATERIALS,
    )

    def __str__(self):
        return self.question