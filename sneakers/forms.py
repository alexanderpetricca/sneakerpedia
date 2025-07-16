from django import forms

from sneakers.models import Sneaker


class CreateSneakerForm(forms.ModelForm):
    class Meta:
        model = Sneaker
        fields = (
            'name',
            'summary',
            'designer',
            'year_released',
            'related_sneakers',
            'primary_image',
        )


class UpdateSneakerForm(forms.ModelForm):
    class Meta:
        model = Sneaker
        fields = (
            'name',
            'summary',
            'designer',
            'year_released',
            'related_sneakers',
            'primary_image',
        )


class DeleteSneakerForm(forms.Form):
    """
    An empty form used on the delete confirmation page.
    No fields but can hold non-field errors that occur
    during the soft-delete process.
    """
    pass