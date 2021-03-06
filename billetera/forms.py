# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.forms.widgets import SplitDateTimeWidget
from decimal import *

class BilleteraLogin(forms.Form):
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
    

class BilleteraElectronicaForm(forms.Form):
    card_name_validator = RegexValidator(
        regex   = '^[a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'][a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'  ]*$',
        message = 'El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    card_surname_validator = RegexValidator(
        regex   = '^[a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'][a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'  ]*$',
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
        widget = forms.PasswordInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'PIN'
            , 'pattern'     : pin_validator.regex.pattern
            , 'message'     : pin_validator.message
            }
        )
    )

class PagoRecargaForm(forms.Form):
    
    monto2_validator = RegexValidator(
        regex   = '^([0-9]+(\.[0-9]+)?)$',
        message = 'Sólo debe contener dígitos.'
    )
    
    monto_validator = RegexValidator(
        regex   = '^[0-9]{5}[.][0-9]{2}$',
        message = 'El monto debe ser un número decimal mayor 0.01 y menor 10000.00.'
    )
    card_name_validator = RegexValidator(
        regex   = '^[a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'][a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'  ]*$',
        message = 'El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    card_surname_validator = RegexValidator(
        regex   = '^[a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'][a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'  ]*$',
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
        
    ID_Billetera = forms.CharField(
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

    monto = forms.DecimalField(
        required = True,
        label = "Monto a recargar",
        min_value = Decimal("0.01"),
        max_value = Decimal("10000.00"),
        validators = [monto_validator,monto2_validator],
        decimal_places = 2,
        widget    = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Monto'
            , 'min'         : "0.01"
            , 'max'         : "10000.00"
            , 'decimal'     : '2'
            , 'pattern'     : monto_validator.regex.pattern
            , 'message'     : monto_validator.message
            }
        )
    )
    
class BilleteraRecargaForm(forms.Form):
    
    monto_validator = RegexValidator(
        regex   = '^[0-9]{5}[.][0-9]{2}$',
        message = 'El monto debe ser un número decimal mayor 0.01 y menor 10000.00.'
    )
    
    card_name_validator = RegexValidator(
        regex   = '^[a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'][a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'  ]*$',
        message = 'El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    card_surname_validator = RegexValidator(
        regex   = '^[a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'][a-zA-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\'  ]*$',
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

    monto = forms.DecimalField(
        required = True,
        label = "Monto a recargar",
        min_value = Decimal("0.01"),
        max_value = Decimal("10000.00"),
        decimal_places = 2,
        widget    = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Monto'
            , 'min'         : '0.01'
            , 'max'         : '10000.00'
            , 'decimal'     : '2'
            , 'pattern'     : monto_validator.regex.pattern
            , 'message'     : monto_validator.message
            }
        )
    )

class CambiarPinForm(forms.Form):
    
    pin_validator = RegexValidator(
        regex   = '^[0-9]{4}$',
        message = 'El PIN solo puede contener cuatro caracteres numéricos.'
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
    
    pin_verificar = forms.CharField(
        required   = True,
        label      = "PIN",
        validators = [pin_validator],
        widget = forms.PasswordInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Ingrese de Nuevo su Pin'
            , 'pattern'     : pin_validator.regex.pattern
            , 'message'     : pin_validator.message
            }
        )
    )