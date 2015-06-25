# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from logging import PlaceHolder
from django.forms.widgets import DateInput

class EstacionamientoForm(forms.Form):

    phone_validator = RegexValidator(
        regex   = '^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-?\d{7}',
        message = 'Debe introducir un formato válido de teléfono.'
    )
    
    name_validator = RegexValidator(
        regex   = '^[-A-Za-z0-9!"#$%&()*,./:;?@\\\[\]_`{|}¡©®°µ·¸¿ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\' ]+$',
        message = 'La entrada debe ser un nombre en Español sin símbolos especiales.'
    )
    
    rif_validator = RegexValidator(
        regex   = '^[JVD]-\d{8}-?\d$',
        message = 'Introduzca un RIF con un formato válido de la forma X-xxxxxxxxx.'
    )
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
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

    # CI del dueno del estacionamiento (no se permiten digitos)
    CI_prop = forms.CharField(
        required = True,
        label = "Cedula",
        validators = [id_validator],
        widget = forms.TextInput(attrs= 
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cedula de Identidad'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message  
            }
        )                   
    ) 

    nombre = forms.CharField(
        required = True,
        label    = "Nombre del Estacionamiento",
        validators = [name_validator],
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Nombre del Estacionamiento'
            , 'pattern'     : name_validator.regex.pattern
            , 'message'     : name_validator.message
            }
        )
    )

    direccion = forms.CharField(
        required = True,
        label    = "Direccion",
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Dirección'
            , 'message'     : 'La entrada no puede quedar vacía.'
            }
        )
    )

    telefono_1 = forms.CharField(
        required   = False,
        label    = "Telefono Oficina 1",
        validators = [phone_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Teléfono 1'
            , 'pattern'     : phone_validator.regex.pattern
            , 'message'     : phone_validator.message
            }
        )
    )

    telefono_2 = forms.CharField(
        required   = False,
        label    = "Telefono Oficina 2",
        validators = [phone_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Teléfono 2'
            , 'pattern'     : phone_validator.regex.pattern
            , 'message'     : phone_validator.message
            }
        )
    )

    email_1 = forms.EmailField(
        required = False,
        label    = "Email Oficina",
        widget   = forms.EmailInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'E-mail 1'
            , 'message'     : 'La entrada debe ser un e-mail válido.'
            }
        )
    )

    rif = forms.CharField(
        required   = True,
        label      = "RIF",
        validators = [rif_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'RIF: X-xxxxxxxxx'
            , 'pattern'     : rif_validator.regex.pattern
            , 'message'     : rif_validator.message
            }
        )
    )

    
class EditarEstacionamientoForm(forms.Form):
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
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
    
    CI_prop = forms.CharField(
        required = True,
        label = "Cedula",
        validators = [id_validator],
        widget = forms.TextInput(attrs= 
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cedula de Identidad'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message  
            }
        )                   
    )

class EstacionamientoExtendedForm(forms.Form):
    
    def clean(self):
        
        cleaned_data = super(EstacionamientoExtendedForm, self).clean()
        puestosLivianos = cleaned_data.get("puestosLivianos")
        puestosPesados = cleaned_data.get("puestosPesados")
        puestosMotos = cleaned_data.get("puestosMotos")

        if puestosLivianos and puestosPesados and puestosMotos:
            
            # Only do something if both fields are valid so far.
            if (puestosLivianos + puestosPesados + puestosMotos <= 0):
                
                raise forms.ValidationError("Debe haber al menos un puesto en el estacionamiento")
            
        
    puestosLivianos = forms.IntegerField(
        required  = True,
        min_value = 0,
        label     = 'Número de Puestos',
        widget    = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Número de Puestos livianos'
            , 'min'         : "0"
            , 'pattern'     : '^[0-9]+'
            , 'message'     : 'La entrada debe ser un número entero no negativo.'
            }
        )
    )

    puestosPesados = forms.IntegerField(
        required  = True,
        min_value = 0,
        label     = 'Número de Puestos',
        widget    = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Número de Puestos pesados'
            , 'min'         : "0"
            , 'pattern'     : '^[0-9]+'
            , 'message'     : 'La entrada debe ser un número entero no negativo.'
            }
        )
    )

    puestosMotos = forms.IntegerField(
        required  = True,
        min_value = 0,
        label     = 'Número de Puestos para Motos',
        widget    = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Número de Puestos Motos'
            , 'min'         : "0"
            , 'pattern'     : '^[0-9]+'
            , 'message'     : 'La entrada debe ser un número entero no negativo.'
            }
        )
    )
    
    puestosDiscapacitados = forms.IntegerField(
        required  = True,
        min_value = 0,
        label     = 'Número de Puestos para Discapacitados',
        widget    = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Número de Puestos Discapacitados'
            , 'min'         : "0"
            , 'pattern'     : '^[0-9]+'
            , 'message'     : 'La entrada debe ser un número entero no negativo.'
            }
        )
    )
    
    horarioin = forms.TimeField(
        required = True,
        label    = 'Horario Apertura',
        widget   = forms.TextInput(attrs =
            { 'class':'form-control'
            , 'placeholder' : 'Horario Apertura'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }
        )
    )

    horarioout = forms.TimeField(
        required = True,
        label    = 'Horario Cierre',
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horario Cierre'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }
        )
    )

    choices_esquema = [
        ('TarifaHora', 'Por hora'),
        ('TarifaMinuto', 'Por minuto'),
        ('TarifaHorayFraccion', 'Por hora y fracción'),
        ('TarifaHoraPico', 'Diferenciada por horario pico'),
        ('TarifaFinDeSemana', 'Diferenciada para fines de semana')
    ]

    esquema = forms.ChoiceField(
        required = True,
        choices  = choices_esquema,
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )
    )

    #Inicio de la hora pico, día no feriado
    inicioTarifa2 = forms.TimeField(
        required = False,
        label    = 'Inicio Horario Especial',
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horario Pico Inicio'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }
        )
    )

    #Fin de la hora pico, día no feriado
    finTarifa2 = forms.TimeField(
        required = False,
        label    = 'Fin Horario Especial',
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horario Pico Fin '
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }
        )
    )
    
    choices_esquema_feriado = [
        ('TarifaHora', 'Por hora en los Dias feriado'),
        ('TarifaMinuto', 'Por minuto en los Dias feriado'),
        ('TarifaHorayFraccion', 'Por hora y fracción en los Dias feriado'),
        ('TarifaHoraPico', 'Diferenciada por horario pico en los Dias feriado'),
        ('TarifaFinDeSemana', 'Diferenciada para fines de semana en los Dias feriado')
    ]

    esquemaFeriado = forms.ChoiceField(
        required = True,
        choices  = choices_esquema_feriado,
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )
    )
    
    #Inicio de la hora pico, día feriado
    inicioTarifaFeriado2 = forms.TimeField(
        required = False,
        label    = 'Inicio Horario Especial',
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horario Pico Inicio para los Dias Feriados'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }
        )
    )

    #Fin de la hora pico, día no feriado
    finTarifaFeriado2 = forms.TimeField(
        required = False,
        label    = 'Fin Horario Especial',
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horario Pico Fin para los Dias Feriados'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }
        )
    )
    
    horizonte = forms.IntegerField(
        required    = True,
        label       = "Horizonte de reservacion",
        widget      = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horizonte'
            , 'min'         : "1"
            , 'max'         : "999"
            , 'pattern'     : '^[0-9]+'
            , 'message'     : 'La entrada debe ser un número entero no negativo.'
            }
        )
    )
    
    choices_frontera = [
        ('PrecioTarifaMasTiempo', 'Cálculo de la frontera por tarifa con más tiempo'),
        ('PrecioTarifaMasCara', 'Cálculo de la frontera usando la tarifa más cara'),
        ('PrecioProporcional', 'Cálculo de la frontera de manera proporcional'),
    ]

    fronteraTarifa = forms.ChoiceField(
        required = True,
        choices  = choices_frontera,
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )
    )
    
class EsquemaTarifarioLiviano(forms.Form):

    tarifa_validator = RegexValidator(
        regex   = '^([0-9]+(\.[0-9]+)?)$',
        message = 'Sólo debe contener dígitos.'
    )
    #Tarifas para diferentes tipos de vehiculos en dias no feriados
    
    tarifaLivianos = forms.DecimalField(
        required   = True,
        validators = [tarifa_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Tarifa Normal Liviano'
            , 'pattern'     : '^([0-9]+(\.[0-9]+)?)$'
            , 'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    tarifaLivianos2 = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa Especial Liviano',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )
        
    #Tarifas para diferentes tipos de vehiculos en dias feriados 
    tarifaLivianosF = forms.DecimalField(
        required   = True,
        validators = [tarifa_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Tarifa Feriado Liviano'
            , 'pattern'     : '^([0-9]+(\.[0-9]+)?)$'
            , 'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    tarifaLivianos2F = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa Especial Feriado Liviano',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

class EsquemaTarifarioPesado(forms.Form):

    tarifa_validator = RegexValidator(
        regex   = '^([0-9]+(\.[0-9]+)?)$',
        message = 'Sólo debe contener dígitos.'
    )

    tarifaPesados  = forms.DecimalField(
        required   = True,
        validators = [tarifa_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Tarifa Normal Pesado'
            , 'pattern'     : '^([0-9]+(\.[0-9]+)?)$'
            , 'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    tarifaPesados2 = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa Normal Feriado Pesado',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    
    tarifaPesadosF  = forms.DecimalField(
        required   = True,
        validators = [tarifa_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Tarifa Especial Pesado'
            , 'pattern'     : '^([0-9]+(\.[0-9]+)?)$'
            , 'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    tarifaPesados2F = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa Especial Feriado Pesado',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

class EsquemaTarifarioMoto(forms.Form):

    tarifa_validator = RegexValidator(
        regex   = '^([0-9]+(\.[0-9]+)?)$',
        message = 'Sólo debe contener dígitos.'
    )
    
    tarifaMotos = forms.DecimalField(
        required   = True,
        validators = [tarifa_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Tarifa Normal Motos'
            , 'pattern'     : '^([0-9]+(\.[0-9]+)?)$'
            , 'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    tarifaMotos2 = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa Especial Motos',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    tarifaMotosF = forms.DecimalField(
        required   = True,
        validators = [tarifa_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Tarifa Normal Feriado Motos'
            , 'pattern'     : '^([0-9]+(\.[0-9]+)?)$'
            , 'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    tarifaMotos2F = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa Especial Feriado Motos',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

class EsquemaTarifarioDiscapacitados(forms.Form):

    tarifa_validator = RegexValidator(
        regex   = '^([0-9]+(\.[0-9]+)?)$',
        message = 'Sólo debe contener dígitos.'
    )
    #Tarifas para diferentes tipos de vehiculos en dias no feriados
    
    tarifaDiscapacitados = forms.DecimalField(
        required   = True,
        validators = [tarifa_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Tarifa Normal Discapasitados'
            , 'pattern'     : '^([0-9]+(\.[0-9]+)?)$'
            , 'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    tarifaDiscapacitados2 = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa Especial Discapasitados',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )
        
    #Tarifas para diferentes tipos de vehiculos en dias feriados 
    tarifaDiscapacitadosF = forms.DecimalField(
        required   = True,
        validators = [tarifa_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Tarifa Normal Feriado Discapasitados'
            , 'pattern'     : '^([0-9]+(\.[0-9]+)?)$'
            , 'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    tarifaDiscapacitados2F = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa Especial Feriado Discapasitados',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )
    
class RifForm(forms.Form):
    
    rif_validator = RegexValidator(
        regex   = '^[JVD]-\d{8}-?\d$',
        message = 'Introduzca un RIF con un formato válido de la forma X-xxxxxxxxx.'                              
    )
    
    rif = forms.CharField(
        required   = True,
        label      = "RIF",
        validators = [rif_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'RIF: X-xxxxxxxxx'
            , 'pattern'     : rif_validator.regex.pattern
            , 'message'     : rif_validator.message
            }
        )
    )

class CedulaForm(forms.Form):
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
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
    
class ElegirFechaForm(forms.Form):
    
    dias_feriados = [
        ('AñoNuevo', '1 de Enero - Año Nuevo'),
        ('DeclaracionIndependencia', '19 de Abril - Declaracion de la Independencia'),
        ('DiaTrabajador', '1 de Mayo - Dia del Trabajador'),
        ('BatallaCarabobo', '24 de Junio - Batalla de Carabobo'),
        ('DiaIndependencia', '5 de Julio - Dia de Independencia'),
        ('NatalicioSimonBolivar', '24 de Julio - Natalicio de Simon Bolivar'),
        ('DiaResistenciaIndigena', '12 de Octubre - Dia de la Resistencia Indigena'),
        ('VisperaNavidad', '24 de Diciembre - Vispera de Navidad'),
        ('Navidad', '25 de Diciembre - Navidad'),
        ('FinAño', '31 de Diciembre - Fin de Año')
        ]

    esquema_diasFeriados= forms.MultipleChoiceField(
        required = False,
        choices  = dias_feriados,
        widget   = forms.CheckboxSelectMultiple()
    )

class AgregarFeriadoForm(forms.Form):
    
    descripcion_validator = RegexValidator(
        regex   = '^[-A-Za-z0-9!"#$%&()*,./:;?@\\\[\]_`{|}¡©®°µ·¸¿ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿ\' ]+$',
        message = 'La descripción del Día feriado debe estar escrita en Español y sin símbolos especiales.'
    )
    
    fecha = forms.DateField(
        required = True,
        label = 'Fecha del Día Feriado',
        widget = forms.DateInput( attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Fecha del Día Feriado'
             }
        )
     )
    
    descripcion = forms.CharField(
        required = True,
        label = 'Descripción del Día Feriado',
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Descripción del Día Feriado'
            , 'pattern'     : descripcion_validator.regex.pattern
            , 'message'     : descripcion_validator.message
            }
        )
    )

