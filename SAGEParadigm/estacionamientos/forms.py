# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from estacionamientos.controller import FindAllSubclasses

from estacionamientos.models import * # No tocar esta linea


class EstacionamientoForm(forms.Form):

    phone_validator = RegexValidator(
                            regex = '^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-?\d{7}',
                            message = 'Debe introducir un formato válido.'
                        )

    # nombre del dueno (no se permiten digitos)
    propietario = forms.CharField(
                    required = True,
                    label = "Propietario",
                    validators = [
                          RegexValidator(
                                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
                                message = 'Sólo debe contener letras.'
                        )
                    ]
                )

    nombre = forms.CharField(required = True, label = "Nombre")

    direccion = forms.CharField(required = True)

    telefono_1 = forms.CharField(required = False, validators = [phone_validator])
    telefono_2 = forms.CharField(required = False, validators = [phone_validator])
    telefono_3 = forms.CharField(required = False, validators = [phone_validator])

    email_1 = forms.EmailField(required = False)
    email_2 = forms.EmailField(required = False)

    rif = forms.CharField(
                    required = True,
                    label = "RIF",
                    validators = [
                          RegexValidator(
                                regex = '^[JVD]-?\d{8}-?\d$',
                                message = 'Introduzca un RIF con un formato válido.'
                        )
                    ]
                )

class EstacionamientoExtendedForm(forms.Form):


    puestos = forms.IntegerField(min_value = 0, label = 'Número de Puestos')

    tarifa_validator = RegexValidator(
                            regex = '^([0-9]+(\.[0-9]+)?)$',
                            message = 'Sólo debe contener dígitos.'
                        )

    horarioin = forms.TimeField(required = True, label = 'Horario Apertura')
    horarioout = forms.TimeField(required = True, label = 'Horario Cierre')

    horario_reserin = forms.TimeField(required = True, label = 'Horario Inicio Reserva')
    horario_reserout = forms.TimeField(required = True, label = 'Horario Fin Reserva')

    #tarifa = forms.CharField(required = True, validators = [tarifa_validator])
    
    lista_de_esquemas = FindAllSubclasses(EsquemaTarifario)
    choices_esquema = []
    for i in range(len(lista_de_esquemas)):
        choices_esquema.append((i,lista_de_esquemas[i][0].tipo(None)))
    esquema = forms.ChoiceField(
                                required = True,
                                choices = choices_esquema
    )
    

    
    def __init__(self, *args, **kwargs):
        super(EstacionamientoExtendedForm,self).__init__(*args, **kwargs)
        self.fields['puestos'].widget.attrs = {'class':'form-control', 'placeholder':'Número de Puestos'}
        self.fields['horarioin'].widget.attrs = {'class':'form-control', 'placeholder':'Horario Apertura'}
        self.fields['horarioout'].widget.attrs = {'class':'form-control', 'placeholder':'Horario Cierre'}
        self.fields['horario_reserin'].widget.attrs = {'class':'form-control', 'placeholder':'Horario Inicio Reserva'}
        self.fields['horario_reserout'].widget.attrs = {'class':'form-control', 'placeholder':'Horario Fin Reserva'}
        #self.fields['tarifa'].widget.attrs = {'class':'form-control', 'placeholder':'Tarifa'}
        self.fields['esquema'].widget.attrs = {'class':'form-control', 'ng-model':'form_select','data-ng-click':"default = '';", 'placeholder':'Tipo de tarifa'}
        
        for i in range(len(self.lista_de_esquemas)):
            campos = self.lista_de_esquemas[i][0].formCampos(None)
            for j in range(len(campos)):
                self.fields["field_%d_%d" % (i,j)] = campos[j][0]
                if campos[j][1]:
                    campos[j][2]['ng-show']=("form_select === '%d'" % i)
                    campos[j][2]['data-ng-model']=("default_%d_%d" % (i,j))
                    self.fields['esquema'].widget.attrs['data-ng-click']=self.fields['esquema'].widget.attrs['data-ng-click']+("default_%d_%d = %s;" % (i,j,str(campos[j][3])))
                    self.fields["field_%d_%d" % (i,j)].widget.attrs = campos[j][2]
                else:
                    self.fields['esquema'].widget.attrs['data-ng-click']=self.fields['esquema'].widget.attrs['data-ng-click']+("default_%d_%d = %s;" % (i,j,str(campos[j][2])))
                    self.fields["field_%d_%d" % (i,j)].widget.attrs = {'class':'form-control', 'ng-show':("form_select === '%d'" % i),'data-ng-model':("default_%d_%d" % (i,j))}

class EstacionamientoReserva(forms.Form):
    inicio = forms.DateTimeField(label = 'Horario Inicio Reserva')
    final = forms.DateTimeField(label = 'Horario Final Reserva')

class PagoTarjetaDeCredito(forms.Form):
    nombre = forms.CharField( required = True, 
                            label = "Nombre",
                            validators = [ RegexValidator( 
                                       regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]*$',
                                       message = 'El apellido no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos'
                                       )
                                    ]
                            )
    apellido = forms.CharField( required = True, 
                            label = "Apellido",
                            validators = [ RegexValidator( 
                                       regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]*$',
                                       message = 'El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos')
                                    ]
                            )
    cedulaTipo = forms.ChoiceField(required = True,
                                label = 'cedulaTipo',
                                choices = (
                                    ('V', 'V'),
                                    ('E', 'E')
                                )                       
                            )
    cedula = forms.CharField( required = True, 
                        label = "Cédula",
                        validators = [ RegexValidator( 
                                   regex = '^[0-9]+$',
                                   message = 'La cédula solo puede contener caracteres numéricos')
                                ]
                        )

    tarjetaTipo = forms.ChoiceField(required = True,
                                label = 'tarjetaTipo',
                                choices = (
                                    ('Vista', ' VISTA '),
                                    ('Mister', ' MISTER '),
                                    ('Xpress', ' XPRESS ')
                                ),
                                widget = forms.RadioSelect()
                            )
    tarjeta = forms.CharField(
                            required = True,
                            label = "Tarjeta de Credito",
                            validators = [
                                  RegexValidator(
                                        regex = '^[0-9]{16}$',
                                        message = 'Introduzca un numero de tarjeta válido.'
                                )
                            ]
                        )
