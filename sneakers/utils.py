
def get_active_filters(form) -> dict:

    form_is_valid = form.is_valid()

    active_filters = {
        form.fields[k].label or k: v
        for k, v in form.cleaned_data.items()
        if v not in (None, '', [], {}, ()) and k in form.fields
    } if form_is_valid else {}

    return active_filters    