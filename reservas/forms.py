# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.forms.widgets import SplitDateTimeWidget

class CustomSplitDateTimeWidget(SplitDateTimeWidget):

    def format_output(self, rendered_widgets):
        return '<p></p>'.join(rendered_widgets)

class ReservaForm(forms.Form):
    
    card_name_validator = RegexValidator(
        regex   = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]*$',
        message = 'El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    card_surname_validator = RegexValidator(
        regex   = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]*$',
        message = 'El apellido no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
    )
    
    nombre = forms.CharField(
        required   = True,
        label      = "Nombre",
        validators = [card_name_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Nombre'
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
            , 'placeholder' : 'Apellido'
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
            ('Moto', 'Moto'),
            ('Discapacitados', 'Discapacitados')
        ),
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )                                  
    )
    
class BuscarReservaForm(forms.Form):
    
    transaccion_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'El numero de transaccion solo puede contener caracteres numéricos.'
    )
    
    cedula_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
    )
     
    
    numReser = forms.CharField(
        required   = True,
        label      = "Reserva",
        validators = [transaccion_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'ID Reserva'
            , 'pattern'     : transaccion_validator.regex.pattern
            , 'message'     : transaccion_validator.message
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
        validators = [cedula_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cédula'
            , 'pattern'     : cedula_validator.regex.pattern
            , 'message'     : cedula_validator.message
            }
        )
    ) 
   
    
class MoverReservaNuevaForm(forms.Form):
    
    nuevoInicio = forms.SplitDateTimeField(
        required = True,
        label = 'Horario Inicio Reserva',
        widget= CustomSplitDateTimeWidget(attrs=
            { 'class'       : 'form-control'
            , 'type'        : 'date'
            , 'placeholder' : 'Hora Inicio Reserva'
            }
        )
    )                 

class MoverReservaBilletera(forms.Form):
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'El ID solo puede contener caracteres numéricos.'
    )
    
    pin_validator = RegexValidator(
        regex   = '^[0-9]{4}$',
        message = 'El PIN solo puede contener cuatro caracteres numéricos.'
    )
    
    id = forms.CharField(
        required   = True,
        label      = "ID de la Billetera a recargar",
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
        widget = forms.PasswordInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'PIN'
            , 'pattern'     : pin_validator.regex.pattern
            , 'message'     : pin_validator.message
            }
        )
    )                 
   
class PagoForm(forms.Form):
    
    card_name_validator = RegexValidator(
        regex   = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]*$',
        message = 'El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    card_surname_validator = RegexValidator(
        regex   = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]*$',
        message = 'El apellido no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
    )
    
    card_validator = RegexValidator(
        regex   = '^[0-9]{16}$',
        message = 'Introduzca un número de tarjeta válido de 16 dígitos.'
    )
    
    nombre = forms.CharField(
        required   = True,
        label      = "Nombre del Tarjetahabiente",
        validators = [card_name_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Nombre del Tarjetahabiente'
            , 'pattern'     : card_name_validator.regex.pattern
            , 'message'     : card_name_validator.message
            }
        )
    )
    

    apellido = forms.CharField(
        required   = True,
        label      = "Apellido del Tarjetahabiente",
        validators = [card_surname_validator],
        widget = forms.TextInput(attrs =
            { 'class'      : 'form-control'
            , 'placeholder' : 'Apellido del Tarjetahabiente'
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

    tarjetaTipo = forms.ChoiceField(
        required = True,
        label    = 'tarjetaTipo',
        choices  = (
            ('Vista',  ' VISTA '),
            ('Mister', ' MISTER '),
            ('Xpress', ' XPRESS '),
        ),
        widget   = forms.RadioSelect()#attrs={'onChange':"this.form.submit()"})
    )

    tarjeta = forms.CharField(
        required   = True,
        label      = "Tarjeta de Credito",
        validators = [card_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Tarjeta de Credito'
            , 'pattern'     : card_validator.regex.pattern
            , 'message'     : card_validator.message
            }
        )
    )    
