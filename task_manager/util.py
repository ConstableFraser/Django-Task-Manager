
def set_status(field, status):
    class_style = {'valid': ' is-valid',
                   'invalid': 'is-invalid'
                   }

    attrs = field.widget.attrs
    attrs.setdefault("class", "")
    attrs["class"] += class_style[status]
