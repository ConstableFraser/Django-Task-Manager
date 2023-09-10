
def validate_username(username):
    def check_letter(ch: str) -> bool:
        return any([ch.isdigit(),
                    ch.isalpha(),
                    ch in ('@', '.', '+', '-', '_')
                    ])
    return all([check_letter(s) for s in username])


def set_status(field, status):
    class_style = {'valid': ' is-valid',
                   'invalid': 'is-invalid'
                   }

    attrs = field.widget.attrs
    attrs.setdefault("class", "")
    attrs["class"] += class_style[status]
