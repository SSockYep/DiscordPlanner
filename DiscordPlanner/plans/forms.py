from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class NewPlanForm(forms.Form):
    guild = forms.ChoiceField(
        label="서버 선택", widget=forms.Select)
    plan_name = forms.CharField(label='계획 이름')
    datetime = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': False,
            }
        ),
        label='예정 시각'
    )
    attendee_num = forms.DecimalField(label="참가인원(선택)", required=False)

    def __init__(self, *args, **kwargs):
        super(NewPlanForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
