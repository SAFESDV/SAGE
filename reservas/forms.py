# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.forms.widgets import SplitDateTimeWidget

class CustomSplitDateTimeWidget(SplitDateTimeWidget):

    def format_output(self, rendered_widgets):
        return '<p></p>'.join(rendered_widgets)

class ReservaForm(forms.Form):
    
    inicio = forms.SplitDateTimeField(
        required = True,
        label = 'Horario Inicio Reserva',
        widget= CustomSplitDateTimeWidget(attrs=
            { 'class'       : 'form-control'
            , 'type'        : 'date'
            , 'placeholder' : 'Hora Inicio Reserva'
            }
        )
    )

    final = forms.SplitDateTimeField(
        required = True,
        label    = 'Horario Final Reserva',
        widget   = CustomSplitDateTimeWidget(attrs=
            { 'class'       : 'form-control'
            , 'type'        : 'date'
            , 'placeholder' : 'Hora Final Reserva'
            }
        )
    )
    
    tipo_vehiculo = forms.ChoiceField(
        required = True,
        label    = 'Tipo de vehículo',
        choices  = (
            ('Liviano', 'Liviano'),
            ('Pesado', 'Pesado'),
            ('Moto', 'Moto')
        ),
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )                                  
    )
    
class CancelarReservaForm(forms.Form):
    
    transaccion_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'El numero de transaccion solo puede contener caracteres numéricos.'
    )
    
    cedula_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
    )
    
    numTransac = forms.CharField(
        required   = True,
        label      = "Transacción",
        validators = [transaccion_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Transacción'
            , 'pattern'     : transaccion_validator.regex.pattern
            , 'message'     : transaccion_validator.message
            }
        )
    )                            
    
    cedula = forms.CharField(
        required   = True,
        label      = "Cédula",
        validators = [cedula_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cédula'
            , 'pattern'     : cedula_validator.regex.pattern
            , 'message'     : cedula_validator.message
            }
        )
    ) 
