# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.forms.widgets import SplitDateTimeWidget

class BilleteraElectronicaPagoForm(forms.Form):
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
    )
    
    pin_validator = RegexValidator(
        regex   = '^[0-9]{4}$',
        message = 'El PIN solo puede contener cuatro caracteres numéricos.'
    )
    
    id = forms.CharField(
        required   = True,
        label      = "ID",
        validators = [id_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'ID'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message
            }
        )
    )
    
    pin = forms.CharField(
        required   = True,
        label      = "PIN",
        validators = [pin_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'PIN'
            , 'pattern'     : pin_validator.regex.pattern
            , 'message'     : pin_validator.message
            }
        )
    )
    
    
    
    
class BilleteraElectronicaForm(forms.Form):
    card_name_validator = RegexValidator(
        regex   = '^[a-zA-Z0-9áéíóúüÜñÑÁÉÍÓÚ][a-zA-Z0-9áéíóúüÜñÑÁÉÍÓÚ ]*$',
        message = 'El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    card_surname_validator = RegexValidator(
        regex   = '^[a-zA-Z0-9áéíóúñüÜÑÁÉÍÓÚ][a-zA-Z0-9áéíóúüÜñÑÁÉÍÓÚ ]*$',
        message = 'El apellido no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
    )
    
    pin_validator = RegexValidator(
        regex   = '^[0-9]{4}$',
        message = 'El PIN solo puede contener cuatro caracteres numéricos.'
    )
    
    nombre = forms.CharField(
        required   = True,
        label      = "Nombre",
        validators = [card_name_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Nombre del Titular'
            , 'pattern'     : card_name_validator.regex.pattern
            , 'message'     : card_name_validator.message
            }
        )
    )

    apellido = forms.CharField(
        required   = True,
        label      = "Apellido",
        validators = [card_surname_validator],
        widget = forms.TextInput(attrs =
            { 'class'      : 'form-control'
            , 'placeholder' : 'Apellido del Titular'
            , 'pattern'     : card_surname_validator.regex.pattern
            , 'message'     : card_surname_validator.message
            }
        )
    )

    cedulaTipo = forms.ChoiceField(
        required = True,
        label    = 'cedulaTipo',
        choices  = (
            ('V', 'V'),
            ('E', 'E')
        ),
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )
    )

    cedula = forms.CharField(
        required   = True,
        label      = "Cédula",
        validators = [id_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cédula'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message
            }
        )
    )
    
    pin = forms.CharField(
        required   = True,
        label      = "PIN",
        validators = [pin_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'PIN'
            , 'pattern'     : pin_validator.regex.pattern
            , 'message'     : pin_validator.message
            }
        )
    )