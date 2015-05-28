# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.forms.widgets import SplitDateTimeWidget

class PropietarioForm(forms.Form):

    phone_validator = RegexValidator(
        regex   = '^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-?\d{7}',
        message = 'Debe introducir un formato válido de teléfono.'
    )
    
    name_validator = RegexValidator(
        regex   = '^[A-Za-z0-9áéíóúüÜñÑÁÉÍÓÚ ]+$',
        message = 'La entrada debe ser un nombre en Español sin símbolos especiales.'
    )
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
    )

    # Nombre del dueno del estacionamiento (no se permiten digitos)
    nombre_prop = forms.CharField(
        required   = True,
        label      = "Nombre Completo",
        validators = [name_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Propietario'
            , 'pattern'     : name_validator.regex.pattern
            , 'message'     : name_validator.message
            }
        )
    )
    
    Cedula = forms.CharField(
        required = True,
        label = "Cedula de Identidad",
        validators = [id_validator],
        widget = forms.TextInput(attrs= 
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cedula de Identidad'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message  
            }
        )                   
    )    

    telefono_prop = forms.CharField(
        required   = False,
        label    = "Telefono Personal",
        validators = [phone_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Teléfono Personal'
            , 'pattern'     : phone_validator.regex.pattern
            , 'message'     : phone_validator.message
            }
        )
    )

    email_prop = forms.EmailField(
        required = False,
        label    = "Email Personal",
        widget   = forms.EmailInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'E-mail Personal'
            , 'message'     : 'La entrada debe ser un e-mail válido.'
            }
        )
    )