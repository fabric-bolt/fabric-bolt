from django import forms

from fabric_bolt.launch_window import models


class LaunchWindowCreateForm(forms.ModelForm):
    class Meta:
        model = models.LaunchWindow


class LaunchWindowUpdateForm(LaunchWindowCreateForm):
    pass