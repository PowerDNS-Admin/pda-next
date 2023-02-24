from django.forms import BaseForm


def set_form_fields_disabled(form: BaseForm, disabled: bool = True) -> None:
    """
    For a given form, disable (or enable) all fields.
    """
    for field in form.fields:
        form.fields[field].disabled = disabled
