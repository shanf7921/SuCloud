from django import forms

from alarm.models import ParamError


class RuleForm(forms.ModelForm):
    class Meta:
        model = ParamError
        fields = ("t_device", "e_time", "e_tem", "e_place", "e_pressure", "e_remind")