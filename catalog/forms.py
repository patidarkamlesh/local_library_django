from django import forms
import datetime
from django.core.exceptions import ValidationError


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        # If date is not in past
        if data < datetime.date.today():
            raise ValidationError("Invalid date - date in past")
        # If date is in allowed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError("Invalid date - renewal more than 4 weeks ahead")

        return data