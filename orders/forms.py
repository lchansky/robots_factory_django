from django import forms


class OrderNewForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=255,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    robot_serial = forms.CharField(
        label='Серийный номер робота',
        min_length=5,
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Например: "R2-D2"',
    )

