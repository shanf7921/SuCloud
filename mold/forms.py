from django import forms
from mold.models import Mold


class MoldForm(forms.ModelForm):
    class Meta:
        model = Mold
        fields = ("m_num", "m_name", "m_count", "m_life", "m_product", "m_status", "m_user")

