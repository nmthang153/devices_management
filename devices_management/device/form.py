import datetime
import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import devices, order, Project, supplement


class addForm(forms.Form):
    code = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Code'
        }
    ))
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Name'
        }
    ))
    type = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Type'
        }
    ))
    os_Type = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'OS Type'
        }
    ))
    version = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Version'
        }
    ))

    def save(self):
        devices.objects.create(code=self.cleaned_data['code'],
                               name=self.cleaned_data['name'],
                               type=self.cleaned_data['type'],
                               osType=self.cleaned_data['os_Type'],
                               version=self.cleaned_data['version'],
                               status='Free')

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            devices.objects.get(code=code)
        except ObjectDoesNotExist:
            return code
        raise forms.ValidationError("This code existed!")


class bookForm(forms.Form):
    code = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Code'
        }
    ))

    usefor = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Project'
        }
    ))

    order_to = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=forms.DateTimeInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'd/m/Y h:m'
        }
    ))
    order_from = datetime.datetime.now()

    def clean_code(self):
        code = self.cleaned_data['code']
        devi = devices.objects.get(code=code)
        if devi.status != 'Free':
            raise forms.ValidationError("This device not free")
        try:
            devi
        except ObjectDoesNotExist:
            raise forms.ValidationError("Code does not exist!")
        else:
            return code

    def save(self, uid):
        did = devices.objects.get(code=self.cleaned_data['code'])
        pid = Project.objects.get(name=self.cleaned_data['usefor'])
        order.objects.create(device_id=did.id,
                             user_id=uid,
                             orderFrom=self.order_from,
                             orderTo=self.cleaned_data['order_to'],
                             project_id=pid.id,
                             status='Requesting')
        devices.objects.filter(code=self.cleaned_data['code']).update(
            status='Requesting'
        )


class bookFormAdmin(forms.Form):
    code = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Code'
        }
    ))

    keeper = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Keeper'
        }
    ))
    usefor = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Project'
        }
    ))
    booked_to = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=forms.DateTimeInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'd/m/Y h:m'
        }
    ))
    booked_from = datetime.datetime.now()

    def clean_code(self):
        code = self.cleaned_data['code']
        devi = devices.objects.get(code=code)
        if devi.status != 'Free':
            raise forms.ValidationError("This device not free")
        try:
            devi
        except ObjectDoesNotExist:
            raise forms.ValidationError("Code does not exist!")

        else:
            return code

    def clean_keeper(self):
        keeper = self.cleaned_data['keeper']
        uid = User.objects.get(username=keeper)
        try:
            uid
        except ObjectDoesNotExist:
            raise forms.ValidationError("User does not exist!")
        else:
            return keeper

    def update(self):
        keeper = self.cleaned_data['keeper']
        uid = User.objects.get(username=keeper)
        pid = Project.objects.get(name=self.cleaned_data['usefor'])
        devices.objects.filter(code=self.cleaned_data['code']).update(keeper_id=uid.id,
                                                                      project_id=pid.id,
                                                                      status='Booked',
                                                                      bookedFrom=self.booked_from,
                                                                      bookedTo=self.cleaned_data['booked_to'])


class editForm(forms.Form):
    code = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Code'
        }
    ))
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Name'
        }
    ))
    type = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Type'
        }
    ))
    os_Type = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'OS Type'
        }
    ))
    version = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Version'
        }
    ))
    stt1 = 'Free'
    stt2 = 'Out of Stock'
    STT_CHOICE = (
        (stt1, u"Free"),
        (stt2, u"Out of Stock")
    )
    status = forms.ChoiceField(choices=STT_CHOICE)
    def edit(self, id):
        if self.cleaned_data['status']=='Free':
            devices.objects.filter(id=id).update(code=self.cleaned_data['code'],
                                                 name=self.cleaned_data['name'],
                                                 type=self.cleaned_data['type'],
                                                 osType=self.cleaned_data['os_Type'],
                                                 version=self.cleaned_data['version'],
                                                 keeper=None,
                                                 project=None,
                                                 bookedTo=None,
                                                 bookedFrom=None,
                                                 status=self.cleaned_data['status'])
        else:
            devices.objects.filter(id=id).update(code=self.cleaned_data['code'],
                                                 name=self.cleaned_data['name'],
                                                 type=self.cleaned_data['type'],
                                                 osType=self.cleaned_data['os_Type'],
                                                 version=self.cleaned_data['version'],
                                                 status=self.cleaned_data['status'])


class sttForm(forms.Form):
    bookedFrom = datetime.datetime.now()

    def updatestt(self, id, stt):
        order.objects.filter(id=id).update(status=stt)

    def confirm(self, oid):
        o = order.objects.get(id=oid)
        devices.objects.filter(id=o.device.id).update(status='Booked',
                                                      keeper=o.user.id,
                                                      bookedFrom=self.bookedFrom,
                                                      bookedTo=o.orderTo,
                                                      project=o.project.id)

    def reject(self, oid):
        o = order.objects.get(id=oid)
        devices.objects.filter(id=o.device.id).update(status='Free')


class suppForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Name'
        }
    ))
    type = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Type'
        }
    ))
    os_Type = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'OS Type'
        }
    ))
    version = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Version'
        }
    ))

    usefor = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Project'
        }
    ))

    quantity = forms.IntegerField(min_value=0, max_value=999999, initial=1, widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
        }
    ))

    create_at = datetime.datetime.now()

    def clean_project(self):
        prjname = self.cleaned_data['usefor']
        prj = Project.objects.get(name=prjname)
        try:
            prj
        except ObjectDoesNotExist:
            raise forms.ValidationError("Project does not exist!")

        else:
            return prjname

    def save(self, uid):
        pid = Project.objects.get(name=self.cleaned_data['usefor'])
        supplement.objects.create(name=self.cleaned_data['name'],
                                  type=self.cleaned_data['type'],
                                  osType=self.cleaned_data['os_Type'],
                                  version=self.cleaned_data['version'],
                                  user_id=uid,
                                  project_id=pid.id,
                                  quantity=self.cleaned_data['quantity'],
                                  createdAt=self.create_at)


class prjForm(forms.Form):
    project_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))
    close_at = forms.DateField(widget=forms.DateInput)

    def save(self):
        Project.objects.create(name=self.cleaned_data['project_name'],
                               close_at=self.cleaned_data['close_at'],
                               )
