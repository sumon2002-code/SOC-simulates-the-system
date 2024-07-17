from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget , CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()



def _get_fields(obj):
    fields = [_ for _ in obj._fields]
    return [getattr(obj , _ ) for _ in fields]