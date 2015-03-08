# -*- coding: utf-8 -*-

from django.test import Client
from django.test import TestCase

from decimal import Decimal
from datetime import (
    datetime,
    time,
    timedelta,
    date,
)

from estacionamientos.controller import (
    HorarioEstacionamiento,
    validarHorarioReserva,
    marzullo,
    tasa_reservaciones, 
    calcular_porcentaje_de_tasa
)

from estacionamientos.forms import (
    EstacionamientoForm,
    EstacionamientoExtendedForm,
    ReservaForm,
    PagoForm,
)
from estacionamientos.models import (
    Estacionamiento,
    Reserva,
    TarifaMinuto,
    TarifaHora,
    TarifaHorayFraccion,
    TarifaFinDeSemana,
    TarifaHoraPico
)

###################################################################
#                    ESTACIONAMIENTO VISTA DISPONIBLE
###################################################################
class IntegrationTest(TestCase):
    
    # TDD
    def setUp(self):
        self.client = Client()
        
    def crear_estacionamiento(self, puestos,hora_apertura=time(0,0),hora_cierre=time(23,59)):
        e = Estacionamiento(
            propietario = "prop",
            nombre = "nom",
            direccion = "dir",
            rif = "rif",
            #nroPuesto = puestos,
            #apertura       = hora_apertura,
            #cierre         = hora_cierre,
        )
        e.save()
        return e

    # TDD
    def test_primera_vista_disponible(self):
        response = self.client.get('/estacionamientos/')
        self.assertEqual(response.status_code, 200)
    
    # malicia 
    def test_llamada_a_la_raiz_lleva_a_estacionamientos(self):
        response = self.client.get('', follow=True)
        self.assertEqual(response.status_code, 200)
        
    # integracion TDD
    def test_llamada_a_los_detalles_de_un_estacionamiento(self):
        self.crear_estacionamiento(1)
        response = self.client.get('/estacionamientos/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detalle-estacionamiento.html')
    
    # integracion malicia
    def test_llamada_a_los_detalles_sin_estacionamiento_creado(self):
        response = self.client.get('/estacionamientos/1/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
    
    # integracion TDD
    def test_llamada_a_reserva(self):
        e = Estacionamiento(
            propietario = "prop",
            nombre = "nom",
            direccion = "dir",
            rif = "rif",
            nroPuesto = 20,
            apertura = time(0,0),
            cierre = time(23,59),
        )
        e.save()
        response = self.client.get('/estacionamientos/1/reserva')
        self.assertEqual(response.status_code, 200)
        
    # integracion malicia 
    def test_llamada_a_reserva_sin_estacionamiento_creado(self):
        response = self.client.get('/estacionamientos/1/reserva')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        
    # integracion malicia
    def test_llamada_a_tasa_sin_parametros_especificados_aun(self):
        self.crear_estacionamiento(1)
        response = self.client.get('/estacionamientos/1/tasa')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'template-mensaje.html')
        
    # integracion esquina
    def test_llamada_a_la_generacion_de_grafica_empty_request(self):
        self.crear_estacionamiento(1)
        response = self.client.get('/estacionamientos/grafica/')
        self.assertEqual(response.status_code, 400)
        
    # integracion TDD
    def test_llamada_a_la_generacion_de_grafica_normal_request(self):
        self.crear_estacionamiento(1)
        response = self.client.get('/estacionamientos/grafica/?2015-03-10=10.5')
        self.assertEqual(response.status_code, 200)
    
    # integracion malicia
    def test_llamada_a_la_generacion_de_grafica_bad_request(self):
        self.crear_estacionamiento(1)
        response = self.client.get('/estacionamientos/grafica/?hola=chao')
        self.assertEqual(response.status_code, 400)
    
    # integracion malicia
    def test_llamada_a_la_reserva_por_sms_bad_request(self):
        self.crear_estacionamiento(1)
        response = self.client.get('/estacionamientos/sms?phone=04242221111&text=hola')
        self.assertEqual(response.status_code, 400)
       
    # integracion esquina
    def test_llamada_a_la_reserva_por_sms_empty_request(self):
        self.crear_estacionamiento(1)
        response = self.client.get('/estacionamientos/sms')
        self.assertEqual(response.status_code, 400)
        
    # integracion esquina
    def test_llamada_a_reserva_sin_parametros_especificados_aun(self):
        self.crear_estacionamiento(1)
        response = self.client.get('/estacionamientos/1/reserva')
        self.assertEqual(response.status_code, 403)
    
    # integracion TDD
    def test_llamada_a_consultar_reserva(self):
        response = self.client.get('/estacionamientos/consulta_reserva')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'consultar-reservas.html')
    
    # integracion TDD 
    def test_llamada_a_consultar_ingreso(self):
        response = self.client.get('/estacionamientos/ingreso')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'consultar-ingreso.html')
    
    # integracion malicia  
    def test_llamada_a_url_inexistente(self):
        response = self.client.get('/este/url/no/existe')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
    
    # integracion TDD
    def test_llamada_a_pago_get(self):
        e = Estacionamiento(
            propietario = "prop",
            nombre = "nom",
            direccion = "dir",
            rif = "rif",
            nroPuesto = 20,
            apertura = time(0,0),
            cierre = time(23,59),
        )
        e.save()
        response = self.client.get('/estacionamientos/1/pago')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pago.html')
    
    # integracion TDD  
    def test_llamada_a_pago_post(self):
        e = Estacionamiento(
            propietario = "prop",
            nombre = "nom",
            direccion = "dir",
            rif = "rif",
            nroPuesto = 20,
            apertura = time(0,0),
            cierre = time(23,59),
        )
        e.save()
        response = self.client.post('/estacionamientos/1/pago')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pago.html')
    
    # integracion malicia
    def test_llamada_a_pago_sin_parametros_especificados_aun(self):
        self.crear_estacionamiento(1)
        response = self.client.get('/estacionamientos/1/reserva')
        self.assertEqual(response.status_code, 403)
    
    # integracion malicia
    def test_llamada_a_pago_sin_estacionamiento_creado(self):
        response = self.client.get('/estacionamientos/1/pago')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

###################################################################
#                    ESTACIONAMIENTO_ALL FORM
###################################################################

class SimpleFormTestCase(TestCase):

    # malicia
    def test_campos_vacios(self):
        form_data = {}
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_solo_un_campo_necesario(self):
        form_data = {
            'propietario': 'Pedro'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_dos_campos_necesarios(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_tres_campos_necesarios(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_todos_los_campos_necesarios(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_propietario_invalido_digitos_en_campo(self):
        form_data = {
            'propietario': 'Pedro132',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_propietario_invalido_simbolos_especiales(self):
        form_data = {
            'propietario': 'Pedro!',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_RIF_tamano_invalido(self):
        form_data = {
            'propietario': 'Pedro132',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-1234567'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_RIF_formato_invalido(self):
        form_data = {
            'propietario': 'Pedro132',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'Kaa123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_agregar_telefonos(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789',
            'telefono_1': '02129322878',
            'telefono_2': '04149322878',
            'telefono_3': '04129322878'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_formato_invalido_telefono(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789',
            'telefono_1': '02193228782'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_tamano_invalido_telefono(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789',
            'telefono_1': '0212322878'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_agregar_correos_electronicos(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789',
            'telefono_1': '02129322878',
            'telefono_2': '04149322878',
            'telefono_3': '04129322878',
            'email_1': 'adminsitrador@admin.com',
            'email_2': 'usua_rio@users.com'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_correo_electronico_invalido(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789',
            'telefono_1': '02129322878',
            'telefono_2': '04149322878',
            'telefono_3': '04129322878',
            'email_1': 'adminsitrador@a@dmin.com'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

###################################################################
# ESTACIONAMIENTO_EXTENDED_FORM
###################################################################

class ExtendedFormTestCase(TestCase):

    # malicia
    def test_estacionamiento_extended_form_un_campo(self):
        form_data = { 'puestos': 2}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_dos_campos(self):
        form_data = { 'puestos': 2,
                      'horarioin': time(hour = 6,  minute = 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_tres_campos(self):
        form_data = { 'puestos': 2,
                      'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # caso borde
    def test_estacionamiento_extended_form_cuatro_bien(self):
        form_data = { 'puestos': 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_estacionamiento_extended_form_todos_campos_bien(self):
        form_data = { 'puestos': 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaMinuto'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())
        
    # caso borde
    def test_estacionamiento_extended_form_puestos_1(self):
        form_data = { 'puestos': 1,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # caso borde
    def test_estacionamiento_extended_form_puestos_0(self):
        form_data = { 'puestos': 0,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_estacionamiento_extended_form_hora_inicio_igual_hora_cierre(self):
        form_data = { 'puestos': 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 6,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_string_en_campo_puesto(self):
        form_data = { 'puestos': 'hola',
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_string_hora_inicio(self):
        form_data = { 'puestos': 2,
                      'horarioin': 'holaa',
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_none_en_tarifa(self):
        form_data = { 'puestos': 2,
                      'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': None,
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())
        
######################################################################
# ESTACIONAMIENTO_EXTENDED pruebas controlador
######################################################################

class ExtendedFormControllerTestCase(TestCase):
    
    # TDD
    def test_HorariosValidos(self):
        HoraInicio = time(hour = 12, minute = 0, second = 0)
        HoraFin = time(hour = 18, minute = 0, second = 0)
        self.assertTrue(HorarioEstacionamiento(HoraInicio, HoraFin))

    # malicia
    def test_HorariosInvalido_HoraCierre_Menor_HoraApertura(self):
        HoraInicio = time(hour = 12, minute = 0, second = 0)
        HoraFin = time(hour = 11, minute = 0, second = 0)
        self.assertFalse(HorarioEstacionamiento(HoraInicio, HoraFin))

    # caso borde
    def test_HorariosInvalido_HoraCierre_Igual_HoraApertura(self):
        HoraInicio = time(hour = 12, minute = 0, second = 0)
        HoraFin = time(hour = 12, minute = 0, second = 0)
        self.assertFalse(HorarioEstacionamiento(HoraInicio, HoraFin))

    # caso borde
    def test_Limite_HorarioValido_Apertura_Cierre(self):
        HoraInicio = time(hour = 12, minute = 0, second = 0)
        HoraFin = time(hour = 12, minute = 0, second = 1)
        self.assertTrue(HorarioEstacionamiento(HoraInicio, HoraFin))

    # caso esquina
    def test_Limite_Superior_HorarioValido_Apertura_Cierre(self):
        HoraInicio = time(hour = 0, minute = 0, second = 0)
        HoraFin = time(hour = 23, minute = 59, second = 59)
        self.assertTrue(HorarioEstacionamiento(HoraInicio, HoraFin))

###################################################################
# ESTACIONAMIENTO_RESERVA_FORM
###################################################################

class ReservaFormTestCase(TestCase):
    
    # malicia
    def test_estacionamiento_reserva_vacio(self):
        form_data = {}
        form = ReservaForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_EstacionamientoReserva_UnCampo(self):
        form_data = {'inicio_1': time(hour = 6, minute = 0),
                     'final_1': time(hour = 15, minute = 0),
                     'final_0': date(year=2015,month=2,day=27)
        }
        form = ReservaForm(data = form_data)
        self.assertFalse(form.is_valid())

    # TDD
    def test_EstacionamientoReserva_TodosCamposBien(self):
        form_data = {'inicio_1': time(hour=6, minute=0),
                     'final_1' : time(hour=15, minute=0),
                     'final_0' : date(year=2015, month=2, day=27),
                     'inicio_0': date(year=2015, month=2, day=27)
                    }
        form = ReservaForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_EstacionamientoReserva_InicioString(self):
        form_data = {'inicio_1': 'teruel',
                     'final_1': time(hour = 15, minute = 0),
                     'final_0': date(year=2015,month=2,day=27),
                     'inicio_0': date(year=2015,month=2,day=27)
        }
        form = ReservaForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_EstacionamientoReserva_FinString(self):
        form_data = {'inicio_1': time(hour = 6, minute = 0),
                     'final_1': 'Reinoza',
                     'final_0': date(year=2015,month=2,day=27),
                     'inicio_0': date(year=2015,month=2,day=27)
        }
        form = ReservaForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_EstacionamientoReserva_InicioNone(self):
        form_data = {'inicio_1': None,
                     'final_1': time(hour = 15, minute = 0),
                     'final_0': date(year=2015,month=2,day=27),
                     'inicio_0': date(year=2015,month=2,day=27)
        }
        form = ReservaForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_EstacionamientoReserva_finalNone(self):
        form_data = {'inicio_1': time(hour = 6, minute = 0),
                     'final_1': time(hour = 15, minute = 0),
                     'final_0': None,
                     'inicio_0': date(year=2015,month=2,day=27)
        }
        form = ReservaForm(data = form_data)
        self.assertFalse(form.is_valid())

###################################################################
# Pago Tarjeta de Credito Form
###################################################################
class PagoTarjetaDeCreditoFormTestCase(TestCase):

    # borde
    def test_PagoTarjetaForm_Vacio(self):
        form_data = {}
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # borde
    def test_PagoTarjetaForm_UnCampo(self):
        form_data = {
            'nombre': 'Pedro',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_DosCampos(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': 'Perez',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_TresCampos(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_CuatroCampos(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_CincoCampos(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_SeisCampos(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '24277100',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertTrue(form.is_valid())

    #borde
    def test_PagoTarjetaForm_NombreInvalidoDigitos(self):
        form_data = {
            'nombre': 'Pedro1',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_NombreInvalidoSimbolos(self):
        form_data = {
            'nombre': 'Pedro*',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    #borde
    def test_PagoTarjetaForm_NombreInvalidoEspacio(self):
        form_data = {
            'nombre': ' Pedro',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_ApellidoInvalidoDigitos(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': 'Perez1',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_ApellidoInvalidoSimbolos(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': '¡Perez!',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())
    
       
    #borde
    def test_PagoTarjetaForm_ApellidoInvalidoEspacio(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': ' Perez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_CedulaTipoInvalido(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': 'Perez',
            'cedulaTipo': 'J',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_CedulaInvalida(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': 'V12345',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    #borde
    def test_Limite_Superior_Cedula(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '999999999',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertTrue(form.is_valid())
    
    #borde
    def test_Limite_Inferior_Cedula(self):
        form_data = {
            'nombre': 'Pedro',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '0',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = PagoForm(data = form_data)
        self.assertTrue(form.is_valid())

    #borde
    def test_PagoTarjetaForm_TipoTarjetaInvalido(self):
        form_data = {
            'nombre': 'Pedro1',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'tarjetaTipo': 'American',
            'tarjeta': '1234',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def test_PagoTarjetaForm_TarjetaInvalido(self):
        form_data = {
            'nombre': 'Pedro1',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
            'tarjeta': 'ab12345',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def test_PagoTarjetaForm_DosCamposErroneos(self):
        form_data = {
            'nombre': 'Pedro1',
            'apellido': 'Perez',
            'cedulaTipo': 'foo',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def test_PagoTarjetaForm_CuatroCamposErroneos(self):
        form_data = {
            'nombre': 'Pedro1',
            'apellido': 'Perez',
            'cedulaTipo': 'foo',
            'cedula': '12345sda6789',
            'tarjetaTipo': 'American',
            'tarjeta': '1234',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def test_PagoTarjetaForm_TodosCamposErroneos(self):
        form_data = {
            'nombre': 'Pedro1',
            'apellido': 'Perez2',
            'cedulaTipo': 'foo',
            'cedula': '12345678as9',
            'tarjetaTipo': 'American',
            'tarjeta': 'prueba',
        }
        form = PagoForm(data = form_data)
        self.assertFalse(form.is_valid())


##############################################################
# Estacionamiento Reserva Controlador
###################################################################

class ReservaFormControllerTestCase(TestCase):
# HorarioReserva, pruebas Unitarias
    # normal
    def test_HorarioReservaValido(self):
        hoy=datetime.now()
        ReservaInicio = datetime(hoy.year,hoy.month,hoy.day,15) + timedelta(days=1)
        ReservaFin = datetime(hoy.year,hoy.month,hoy.day,17) + timedelta(days=1)
        HoraApertura = time(hour = 12, minute = 0, second = 0)
        HoraCierre = time(hour = 18, minute = 0, second = 0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (True, ''))

    # borde
    def test_UnDiaDeReserva_Estacionamiento_No_24_horas(self):
        hoy=datetime.now()
        HoraApertura=time(6,0)
        HoraCierre=time(18,0)
        ReservaInicio=datetime(hoy.year,hoy.month,hoy.day,15) + timedelta(days=1)
        ReservaFin=datetime(hoy.year,hoy.month,hoy.day,15) + timedelta(days=2)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El horario de inicio de reserva debe estar en un horario válido.'))
    #Borde
    def test_reservaHorarioCompleto(self):
        hoy=datetime.now()
        HoraApertura=time(6,0)
        HoraCierre=time(18,0)
        ReservaInicio=datetime(hoy.year,hoy.month,hoy.day,6) + timedelta(days=1)
        ReservaFin=datetime(hoy.year,hoy.month,hoy.day,18) + timedelta(days=2)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El horario de inicio de reserva debe estar en un horario válido.'))

    def test_reservaHorarioCompletoYUnMinuto(self):
        hoy=datetime.now()
        HoraApertura=time(6,0)
        HoraCierre=time(18,0)
        ReservaInicio=datetime(hoy.year,hoy.month,hoy.day,6) + timedelta(days=1)
        ReservaFin=datetime(hoy.year,hoy.month,hoy.day,18,1) + timedelta(days=2)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El horario de inicio de reserva debe estar en un horario válido.'))


    #Normal
    def test_UnDiaDeReserva_Estacionamiento_24_horas(self):
        hoy=datetime.now()
        HoraApertura=time(0,0)
        HoraCierre=time(23,59)
        ReservaInicio=datetime(hoy.year,hoy.month,hoy.day,15) + timedelta(days=1)
        ReservaFin=datetime(hoy.year,hoy.month,hoy.day,15) + timedelta(days=2)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (True, ''))

    #Esquina
    def test_SieteDiasDeReserva(self):
        hoy=datetime.now().replace(hour = 0, minute = 0)
        HoraApertura=time(0,0)
        HoraCierre=time(23,59)
        ReservaInicio=hoy
        ReservaFin=hoy + timedelta(7) - timedelta(minutes=1)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (True, ''))

    def test_SieteDiasDeReservaYUnMinuto(self):
        hoy=datetime.now()
        HoraApertura=time(0,0)
        HoraCierre=time(23,59)
        ReservaInicio=hoy
        ReservaFin=hoy + timedelta(days=7,minutes=1)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'La reserva debe estar dentro de los próximos 7 días.'))

    # caso borde
    def test_HorarioReservaInvalido_InicioReservacion_Mayor_FinalReservacion(self):
        ReservaInicio = datetime.now()+timedelta(minutes=1)
        ReservaFin = datetime.now()
        HoraApertura = time(hour = 0, minute = 0, second = 0)
        HoraCierre = time(hour = 23, minute = 59, second = 59)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El horario de inicio de reservacion debe ser menor al horario de fin de la reserva.'))

    # caso borde
    def test_HorarioReservaInvalido_TiempoTotalMenor1h(self):
        ReservaInicio = datetime(year=2000,month=2,day=6,hour = 13, minute = 0, second = 0)
        ReservaFin = datetime(year=2000,month=2,day=6,hour = 13, minute = 59, second = 59)
        HoraApertura = time(hour = 12, minute = 0, second = 0)
        HoraCierre = time(hour = 18, minute = 0, second = 0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El tiempo de reserva debe ser al menos de 1 hora.'))

    # caso borde.
    def test_HorarioReservaInvalido_ReservaFinal_Mayor_HorarioCierre(self):
        HoraApertura = time(hour = 10, minute = 0, second = 0)
        HoraCierre = time(hour = 22, minute = 0, second = 0)
        hoy=datetime.today()
        ReservaInicio=datetime(hoy.year,hoy.month,hoy.day,17) + timedelta(days=1)
        ReservaFin=datetime(hoy.year,hoy.month,hoy.day,23) + timedelta(days=1)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El horario de fin de la reserva debe estar en un horario válido.'))

    # Caso borde
    def test_HorarioReservaInvalido_ReservaInicial_Menor_HorarioApertura(self):
        hoy=datetime.now()
        ReservaInicio = datetime(hoy.year,hoy.month,hoy.day,7) + timedelta(days=1)
        ReservaFin = datetime(hoy.year,hoy.month,hoy.day,15) + timedelta(days=1)
        HoraApertura=time(8,0)
        HoraCierre=time(18,0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El horario de inicio de reserva debe estar en un horario válido.'))

    # malicia
    def test_Reservacion_CamposVacios(self):
        form_data = {}
        form = ReservaForm(data = form_data)
        self.assertFalse(form.is_valid())

###############################################################################
# Marzullo
###############################################################################

class TestMarzullo(TestCase):
    '''
        Bordes:   7
        Esquinas: 6
        Malicia:  5

        Es importante definir el dominio de los datos que recibe Marzullo:

          cap. del est. +----------------------+
                        |                      |
                        |                      |
                        |                      |
                /\      |                      |
        cant. vehiculos |                      |
                \/      |                      |
                        |                      |
                        |                      |
                        |                      |
                      0 +----------------------+
                        |       <reserva>      |
                        |                      hora de cierre
                        |
                        hora de apertura

        Para los casos de prueba, manejamos un estacionamiento con apertura
        a las 6am y cierre a las 6pm, con capacidades que varían en cada caso.
        De esta forma, el dominio se vuelve:

          cap. del est. +--+--+--+--+--+--+--+--+--+--+--+--+
                        |  |  |  |  |  |  |  |  |  |  |  |  |
                        |  |  |  |  |  |  |  |  |  |  |  |  |
                        |  |  |  |  |  |  |  |  |  |  |  |  |
                /\      |  |  |  |  |  |  |  |  |  |  |  |  |
        cant. vehiculos |  |  |  |  |  |  |  |  |  |  |  |  |
                \/      |  |  |  |  |  |  |  |  |  |  |  |  |
                        |  |  |  |  |zz|zz|zz|zz|zz|zz|  |  |
                        |  |  |  |yy|yy|yy|yy|  |  |  |  |  |
                        |xx|xx|xx|xx|xx|  |  |  |  |  |  |  |
                      0 +--+--+--+--+--+--+--+--+--+--+--+--+
                        |  |  |  |  |  |  |  |  |  |  |  |  |
                        06 07 08 09 10 11 12 13 14 15 16 17 18

        Donde las series de xs, ys y zs representan tres reservaciones,
        X, Y y Z, que van, respectivamente, de 6am a 11am, de 9am a 1pm, y de
        10am a 4pm. Podemos ver que la reservación X constituye un caso borde
        para Marzullo, puesto que su inicio coincide exactamente con la hora en
        la que abre el estacionamiento. Si decimos además que la capacidad
        del estacionamiento es 3, este caso se convierte en una esquina, puesto
        que el borde count=capacidad se alcanza entre las horas 10am y 11am.
    '''
    def crear_estacionamiento(self, puestos):
        e = Estacionamiento(
            propietario = "prop",
            nombre = "nom",
            direccion = "dir",
            rif = "rif",
            nroPuesto = puestos,
            apertura       = "06:00",
            cierre         = "18:00",
        )
        e.save()
        return e

    def testOneReservationMax(self): #borde, ocupación = capacidad
        e = self.crear_estacionamiento(1)
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,9), datetime(2015,1,20,15)))

    def testOneReservationEarly(self): #borde, inicio = aprtura
        e = self.crear_estacionamiento(2)
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,6), datetime(2015,1,20,10)))

    def testOneReservationLate(self): #borde, fin = cierre
        e = self.crear_estacionamiento(2)
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,15), datetime(2015,1,20,18)))

    def testOneReservationFullDay(self): #esquina, inicio = aprtura y fin = cierre
        e = self.crear_estacionamiento(1)
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,6), datetime(2015,1,20,18)))

    def testSmallestReservation(self): #borde, fin - inicio = 1hora
        e = self.crear_estacionamiento(1)
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,8), datetime(2015,1,20,9)))

    def testAllSmallestReservations(self): #malicia, fin - inicio = 1hora, doce veces
        e = self.crear_estacionamiento(1)
        for i in range(12):
            Reserva(estacionamiento = e, inicioReserva = datetime(2015, 1, 20, 6+i), finalReserva = datetime(2015, 1, 20, 7+i)).save()
        for i in range(12):
            self.assertFalse(marzullo(e.id, datetime(2015,1,20,6+i), datetime(2015,1,20,7+i)))

    def testFullPlusOne(self): #malicia, fin - inicio = 1hora, doce veces + una reserva FullDay
        e = self.crear_estacionamiento(1)
        for i in range(12):
            Reserva(estacionamiento = e, inicioReserva = datetime(2015, 1, 20, 6+i), finalReserva = datetime(2015, 1, 20, 7+i)).save()
        self.assertFalse(marzullo(e.id, datetime(2015, 1, 20, 6), datetime(2015, 1, 20, 18)))

    def testNoSpotParking(self): #borde, capacidad = 0
        e = self.crear_estacionamiento(0)
        self.assertFalse(marzullo(e.id, datetime(2015,1,20,9), datetime(2015,1,20,15)))

    def testTenSpotsOneReservation(self): #malicia
        e = self.crear_estacionamiento(10)
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,9), datetime(2015,1,20,15)))

    def testAddTwoReservation(self): #esquina, dos reservaciones con fin = cierre estac.
        e = self.crear_estacionamiento(10)
        Reserva(estacionamiento = e, inicioReserva = datetime(2015, 1, 20, 9), finalReserva = datetime(2015, 1, 20, 18)).save()
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,12), datetime(2015,1,20,18)))

    def testAddTwoReservation2(self): #esquina, dos reservaciones con incio = apertura estac.
        e = self.crear_estacionamiento(10)
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 6), finalReserva=datetime(2015, 1, 20, 15)).save()
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,6), datetime(2015,1,20,14)))

    def testAddThreeReservations(self): #malicia, reserva cubre todo el horario, y ocupación = capacidad
        e = self.crear_estacionamiento(3)
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  9), finalReserva=datetime(2015, 1, 20, 15)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 15)).save()
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,6), datetime(2015,1,20,18)))

    def testFiveSpotsFiveReservation(self): #borde, ocupación = capacidad
        e = self.crear_estacionamiento(5)
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  9), finalReserva=datetime(2015, 1, 20, 15)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 15)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 12), finalReserva=datetime(2015, 1, 20, 15)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 15)).save()
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,10), datetime(2015,1,20,18)))

    def testFiveSpotsSixReservation(self): #borde, ocupacion = capacidad antes de intentar hacer reservas nuevas
        e = self.crear_estacionamiento(5)
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  9), finalReserva=datetime(2015, 1, 20, 17)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 17)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 12), finalReserva=datetime(2015, 1, 20, 17)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 12), finalReserva=datetime(2015, 1, 20, 17)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 17)).save()
        self.assertFalse(marzullo(e.id, datetime(2015,1,20,9), datetime(2015,1,20,18)))
        self.assertFalse(marzullo(e.id, datetime(2015,1,20,9), datetime(2015,1,20,15)))

    def testFiveSpotsSixReservationNoOverlapping(self): #Dos esquinas, 1. count = capacidad, inicio=apertura
                                                        #              2. count = capacidad, fin=cierre
        e = self.crear_estacionamiento(5)
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  9), finalReserva=datetime(2015, 1, 20, 17)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 17)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 12), finalReserva=datetime(2015, 1, 20, 17)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 12), finalReserva=datetime(2015, 1, 20, 17)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 17)).save()
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,6), datetime(2015,1,20,10)))
        #La reserva de arriba NO se concreta, puesto que sólo se verificó si era válida, sin agregar su objeto
        self.assertFalse(marzullo(e.id, datetime(2015,1,20,9), datetime(2015,1,20,18)))
        #De todos modos, la segunda falla, porque count = capacidad+1 a partir de las 12m

    def testManyReservationsMaxOverlapping(self): #esquina, count = capacidad en una hora (10am - 11am), algunas reservas tienen inicio = apertura
        e = self.crear_estacionamiento(10)
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  6), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  7), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  8), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  9), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  7), finalReserva=datetime(2015, 1, 20, 11)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  8), finalReserva=datetime(2015, 1, 20, 12)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  9), finalReserva=datetime(2015, 1, 20, 13)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  6), finalReserva=datetime(2015, 1, 20,  9)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  6), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  6), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20,  6), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 15)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 15)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 15)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 15)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 15)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 10), finalReserva=datetime(2015, 1, 20, 15)).save()
        self.assertTrue(marzullo(e.id, datetime(2015,1,20,10), datetime(2015,1,20,15)))

    def testManyReservationsOneOverlap(self): #malicia, count = (capacidad+1) en la hora (9am - 10am), algunas reservas tienen inicio = apertura
        e = self.crear_estacionamiento(10)
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 6), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 7), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 8), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 9), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 7), finalReserva=datetime(2015, 1, 20, 11)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 8), finalReserva=datetime(2015, 1, 20, 12)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 9), finalReserva=datetime(2015, 1, 20, 13)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 6), finalReserva=datetime(2015, 1, 20,  9)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 6), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 6), finalReserva=datetime(2015, 1, 20, 10)).save()
        Reserva(estacionamiento = e, inicioReserva=datetime(2015, 1, 20, 6), finalReserva=datetime(2015, 1, 20, 10)).save()
        self.assertFalse(marzullo(e.id, datetime(2015,1,20,9), datetime(2015,1,20,10)))
        
###################################################################
# Casos de prueba de la tasa de resevación
###################################################################

class TestTasaEstacionamiento(TestCase):
    
    def crear_estacionamiento(self, puestos,hora_apertura=time(0,0),hora_cierre=time(23,59)):
        e = Estacionamiento(
            propietario = "prop",
            nombre = "nom",
            direccion = "dir",
            rif = "rif",
            nroPuesto = puestos,
            apertura       = hora_apertura,
            cierre         = hora_cierre,
        )
        e.save()
        return e
    
    # Esquina 
    def test_estacionamiento_sin_reservas(self): # Esquina
        e=self.crear_estacionamiento(1)
        ahora=datetime.now()
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        salida=dict(zip(lista_fechas,lista_valores))
        self.assertEqual(tasa_reservaciones(e.id),salida)
    
    def test_estacionamiento_reserva_una_hora_sin_cambio_fecha(self): # Normal TDD
        e=self.crear_estacionamiento(1)
        ahora=datetime.now().replace(second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[1]=60
        salida=dict(zip(lista_fechas,lista_valores))
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
        Reserva(estacionamiento= e,inicioReserva=fecha_inicio,finalReserva=fecha_fin).save()
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
        
    def test_estacionamiento_reserva_una_hora_cambio_fecha_mediaNoche(self): # Esquina
        e=self.crear_estacionamiento(1)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[1]=45
        lista_valores[2]=1
        salida=dict(zip(lista_fechas,lista_valores))
        fecha_inicio=(ahora+timedelta(1)).replace(hour=23,minute=15,second=0)
        fecha_fin=fecha_inicio+timedelta(minutes=46)
        Reserva(estacionamiento= e,inicioReserva=fecha_inicio,finalReserva=fecha_fin).save()
        x=tasa_reservaciones(e.id)
        self.assertEqual(x,salida)
        
    def test_reserva_inicio_antes_de_inicioVentana_fin_despues_inicioVentana(self): # Esquina
        e=self.crear_estacionamiento(1)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[0]=1
        salida=dict(zip(lista_fechas,lista_valores))
        fecha_inicio=ahora-timedelta(1)
        fecha_fin=ahora.replace(hour=0,minute=1)
        Reserva(estacionamiento= e,inicioReserva=fecha_inicio,finalReserva=fecha_fin).save()
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
        
    def test_estacionamiento_reserva_un_dia_sola_casilla_menos_un_minuto(self): # Normal TDD
        e=self.crear_estacionamiento(1)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[1]=60*24-1
        salida=dict(zip(lista_fechas,lista_valores))
        fecha_inicio=ahora+timedelta(1)
        fecha_fin=ahora+timedelta(days=1,hours=23,minutes=59)
        Reserva(estacionamiento= e,inicioReserva=fecha_inicio,finalReserva=fecha_fin).save()
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
    def test_estacionamiento_reserva_un_dia_sola_casilla(self): # Borde
        e=self.crear_estacionamiento(1)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[1]=60*24
        salida=dict(zip(lista_fechas,lista_valores))
        fecha_inicio=ahora+timedelta(1)
        fecha_fin=ahora+timedelta(days=2)
        Reserva(estacionamiento= e,inicioReserva=fecha_inicio,finalReserva=fecha_fin).save()
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
    def test_estacionamiento_reserva_un_dia_dos_casillas(self): #Borde
        e=self.crear_estacionamiento(1)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[1]=780
        lista_valores[2]=660
        salida=dict(zip(lista_fechas,lista_valores))
        fecha_inicio=ahora+timedelta(days=1,hours=11)
        fecha_fin=ahora+timedelta(days=2,hours=11)
        Reserva(estacionamiento= e,inicioReserva=fecha_inicio,finalReserva=fecha_fin).save()
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
    def test_estacionamiento_reserva_un_dia_mas_un_minuto(self): #Borde
        e=self.crear_estacionamiento(1)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[1]=60*24
        lista_valores[2]=1
        salida=dict(zip(lista_fechas,lista_valores))
        fecha_inicio=ahora+timedelta(1)
        fecha_fin=ahora+timedelta(days=2,seconds=60)
        Reserva(estacionamiento= e,inicioReserva=fecha_inicio,finalReserva=fecha_fin).save()
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
    def test_estacionamiento_reserva_siete_dias(self): # Esquina
        e=self.crear_estacionamiento(1)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[60*24 for i in range(8)]
        lista_valores[7]=0
        salida=dict(zip(lista_fechas,lista_valores))
        fecha_inicio=ahora
        fecha_fin=ahora+timedelta(days=7)
        Reserva(estacionamiento= e,inicioReserva=fecha_inicio,finalReserva=fecha_fin).save()
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
    def test_estacionamiento_reserva_siete_dias_antes_media_noche(self): #Esquina
        e=self.crear_estacionamiento(1)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[60*24 for i in range(8)]
        lista_valores[0]=1
        lista_valores[7]=60*24-1
        salida=dict(zip(lista_fechas,lista_valores))
        fecha_inicio=ahora.replace(hour=23,minute=59)
        fecha_fin=ahora.replace(hour=23,minute=59)+timedelta(days=7)
        Reserva(estacionamiento= e,inicioReserva=fecha_inicio,finalReserva=fecha_fin).save()
        x=tasa_reservaciones(e.id)
        self.assertEqual(x,salida)
        
    def test_estacionamiento_reserva_una_hora_dos_puestos(self): # Borde
        e=self.crear_estacionamiento(2)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[0]=90
        salida=dict(zip(lista_fechas,lista_valores))
        Reserva(estacionamiento= e,inicioReserva=ahora,finalReserva=ahora+timedelta(seconds=2700)).save()
        Reserva(estacionamiento= e,inicioReserva=ahora+timedelta(seconds=2700),finalReserva=ahora+timedelta(seconds=5400)).save()
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
    def test_dos_reservaciones_mismo_dia(self): # Borde
        e=self.crear_estacionamiento(2)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[0]=1440*2
        salida=dict(zip(lista_fechas,lista_valores))
        Reserva(estacionamiento= e,inicioReserva=ahora,finalReserva=ahora+timedelta(1)).save()
        Reserva(estacionamiento= e,inicioReserva=ahora,finalReserva=ahora+timedelta(1)).save()
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
    def test_reserva_6_dias_misma_hora(self): # Normal TDD
        e=self.crear_estacionamiento(2)
        ahora=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[1440 for i in range(8)]
        lista_valores[0]=0
        lista_valores[1]=0
        lista_valores[2]=18*60
        lista_valores[7]=6*60
        salida=dict(zip(lista_fechas,lista_valores))
        Reserva(estacionamiento= e,inicioReserva=ahora.replace(hour=6)+timedelta(2),finalReserva=ahora.replace(hour=6)+timedelta(7)).save()
        x=tasa_reservaciones(e.id)
        print(x)
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
    def test_reservaciones_de_una_hora_24_horas(self): # Esquina
        CAPACIDAD = 10
        HORAS_SEMANA = 168
        UNA_HORA = timedelta(hours=1)
        ahora = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        e = self.crear_estacionamiento(CAPACIDAD)
        for i in range(CAPACIDAD):
            hora_reserva = ahora
            for j in range(HORAS_SEMANA):
                Reserva(estacionamiento=e,inicioReserva=hora_reserva,finalReserva=hora_reserva+UNA_HORA).save()
                hora_reserva += UNA_HORA
                
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[60*CAPACIDAD*24 for i in range(8)]
        lista_valores[7]=0
        salida=dict(zip(lista_fechas,lista_valores))
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
    def test_reservaciones_de_una_hora_6_a_18_horas(self): # Esquina
        CAPACIDAD = 10
        HORAS_DIA = 12
        UNA_HORA = timedelta(hours=1)
        ahora = datetime.now().replace(hour=6,minute=0,second=0,microsecond=0)
        e = self.crear_estacionamiento(CAPACIDAD,time(6,0),time(18,0))
        for i in range(CAPACIDAD):
            hora_reserva = ahora
            for j in range(7):
                for k in range(HORAS_DIA):
                    Reserva(estacionamiento=e,inicioReserva=hora_reserva,finalReserva=hora_reserva+UNA_HORA).save()
                    hora_reserva += UNA_HORA
                hora_reserva=ahora+timedelta(j+1)
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[60*CAPACIDAD*HORAS_DIA for i in range(8)]
        lista_valores[7]=0
        salida=dict(zip(lista_fechas,lista_valores))
        self.assertEqual(tasa_reservaciones(e.id),salida)
        
                
        
###################################################################
    # Casos de prueba para calcular tarifas        
##################################################################

    def test_estacionamiento_vacio(self):
        e=self.crear_estacionamiento(2)
        ahora=datetime.now()
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        ocupacion1=dict(zip(lista_fechas,lista_valores))
        calcular_porcentaje_de_tasa(hora_apertura=e.apertura,hora_cierre=e.cierre,capacidad=2, ocupacion=ocupacion1)
        self.assertEqual(dict(zip(lista_fechas,[Decimal(0) for i in range(8)])),ocupacion1)

    def test_estacionamiento_siempre_abierto_mitad_capacidad_primer_dia(self):
        e=self.crear_estacionamiento(2)
        ahora=datetime.now()
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[0]=1440
        ocupacion1=dict(zip(lista_fechas,lista_valores))
        calcular_porcentaje_de_tasa(hora_apertura=e.apertura,hora_cierre=e.cierre,capacidad=2, ocupacion=ocupacion1)
        lista_valores2=[Decimal(0) for i in range(8)]
        lista_valores2[0]=Decimal(50)
        self.assertEqual(dict(zip(lista_fechas,lista_valores2)),ocupacion1)
    
    def test_estacionamiento_horario_restringido_mitad_capacidad_primer_dia(self):
        e=self.crear_estacionamiento(2,time(6,0),time(18,45))
        ahora=datetime.now()
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[0]=765
        ocupacion1=dict(zip(lista_fechas,lista_valores))
        calcular_porcentaje_de_tasa(hora_apertura=e.apertura,hora_cierre=e.cierre,capacidad=2, ocupacion=ocupacion1)
        lista_valores2=[Decimal(0) for i in range(8)]
        lista_valores2[0]=Decimal(50)
        self.assertEqual(dict(zip(lista_fechas,lista_valores2)),ocupacion1)
        
    def test_estacionamiento_horario_restringido_toda_capacidad_primer_dia(self):
        e=self.crear_estacionamiento(2,time(6,0),time(18,45))
        ahora=datetime.now()
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[0]=765*2
        ocupacion1=dict(zip(lista_fechas,lista_valores))
        calcular_porcentaje_de_tasa(hora_apertura=e.apertura,hora_cierre=e.cierre,capacidad=2, ocupacion=ocupacion1)
        lista_valores2=[Decimal(0) for i in range(8)]
        lista_valores2[0]=Decimal(50)*2
        self.assertEqual(dict(zip(lista_fechas,lista_valores2)),ocupacion1)
    
    def test_horario_restringido_toda_capacidad_primer_dia_y_un_minuto(self):
        e=self.crear_estacionamiento(2,time(6,0),time(18,45))
        ahora=datetime.now()
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[0]=765*2
        lista_valores[1]=1
        ocupacion1=dict(zip(lista_fechas,lista_valores))
        calcular_porcentaje_de_tasa(hora_apertura=e.apertura,hora_cierre=e.cierre,capacidad=2, ocupacion=ocupacion1)
        lista_valores2=[Decimal(0) for i in range(8)]
        lista_valores2[0]=Decimal(50)*2
        lista_valores2[1]=Decimal(100)/Decimal(765*2)
        lista_valores2[1] = lista_valores2[1].quantize(Decimal('1.0'))
        self.assertEqual(dict(zip(lista_fechas,lista_valores2)),ocupacion1)
    
    def test_horario_restringido_toda_capacidad_primer_dia_exceso_1_minuto(self):
        e=self.crear_estacionamiento(2,time(6,0),time(18,45))
        ahora=datetime.now()
        lista_fechas=[(ahora+timedelta(i)).date() for i in range(8)]
        lista_valores=[0 for i in range(8)]
        lista_valores[0]=765*2+1
        ocupacion1=dict(zip(lista_fechas,lista_valores))
        calcular_porcentaje_de_tasa(hora_apertura=e.apertura,hora_cierre=e.cierre,capacidad=2, ocupacion=ocupacion1)
        lista_valores2=[Decimal(0) for i in range(8)]
        lista_valores2[0]=Decimal(765*2+1)*100/Decimal(765*2)
        lista_valores2[0] = lista_valores2[0].quantize(Decimal('1.0'))
        self.assertEqual(dict(zip(lista_fechas,lista_valores2)),ocupacion1)
        

###################################################################
# Casos de prueba de tipos de tarifa
###################################################################

class RateTestCase(TestCase):

    #Pruebas para tarifa de hora y fraccion

    def test_tarifa_hora_y_fraccion_una_hora(self):
        initial_time = datetime(2015,2,18,13,0)
        final_time = datetime(2015,2,18,14,0)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),2)

    def test_tarifa_hora_y_fraccion_una_dos_horas(self):
        initial_time = datetime(2015,2,18,13,0)
        final_time = datetime(2015,2,18,15,0)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),4)

    def test_tarifa_hora_y_fraccion_media_hora(self):
        initial_time = datetime(2015,2,18,13,15)
        final_time = datetime(2015,2,18,13,45)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),2)

    def test_tarifa_hora_y_fraccion_una_hora_mas_media_hora(self):
        initial_time = datetime(2015,2,18,13,0)
        final_time = datetime(2015,2,18,14,30)
        rate = TarifaHorayFraccion(tarifa = 20)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),30)

    def test_tarifa_hora_y_fraccion_una_hora_fraccion_15_minutos(self):
        initial_time = datetime(2015,2,18,19,0)
        final_time = datetime(2015,2,18,20,15)
        rate = TarifaHorayFraccion(tarifa = 1)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),1.5)

    def test_tarifa_hora_y_fraccion_una_hora_mas_media_hora_mas_1_minuto(self):
        initial_time = datetime(2015,2,18,15,15)
        final_time = datetime(2015,2,18,16,46)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),4)
        
    def test_tarifa_hora_y_fraccion_un_dia(self): # Normal
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,0)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),48)

    def test_tarifa_hora_y_fraccion_un_dia_menos_un_minuto(self): # Borde
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,18,23,59)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),48)

    def test_tarifa_hora_y_fraccion_un_dia_mas_un_minuto(self): # Borde
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,1)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),49)

    def test_tarifa_hora_y_fraccion_un_dia_mas_media_hora(self):
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,30)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),49)

    def test_tarifa_hora_y_fraccion_un_dia_mas_media_hora_mas_un_minuto(self):
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,31)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),50)

    def test_tarifa_hora_y_fraccion_un_dia_antes_de_la_medianoche_mas_un_minuto(self):
        initial_time = datetime(2015,2,18,23,59)
        final_time = datetime(2015,2,20,0,0)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),49)

    def test_tarifa_hora_y_fraccion_un_dia_treinta_minutos_antes_de_la_medianoche_mas_treinta_minutos(self):
        initial_time = datetime(2015,2,18,23,30)
        final_time = datetime(2015,2,20,0,0)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),49)

    def test_tarifa_hora_y_fraccion_un_dia_treinta_minutes_antes_de_la_medianoche_mas_treinta_y_un_minutos(self):
        initial_time = datetime(2015,2,18,23,30)
        final_time = datetime(2015,2,20,0,1)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),50)

    def test_tarifa_hora_y_fraccion_dos_dias(self):
        initial_time = datetime(2015,2,18,6,30)
        final_time = datetime(2015,2,20,6,30)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),96)

    def test_tarifa_hora_y_fraccion_dos_dias_mas_un_minuto(self):
        initial_time = datetime(2015,2,18,6,30)
        final_time = datetime(2015,2,20,6,31)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),97)

    def test_tarifa_hora_y_fraccion_siete_dias(self): # Esquina
        initial_time = datetime(2015,2,18,6,30)
        final_time = datetime(2015,2,25,6,30)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),7*24*2)

    # Pruebas para la tarifa por minuto

    def test_tarifa_minuto_un_minuto(self): # Borde
        initial_time = datetime(2015,2,18,15,1)
        final_time = datetime(2015,2,18,15,2)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),1)

    def test_tarifa_minuto_dos_minutos(self): # TDD
        initial_time = datetime(2015,2,18,15,1)
        final_time = datetime(2015,2,18,15,3)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),2)

    def test_tarifa_minuto_una_hora(self): # Borde
        initial_time = datetime(2015,2,18,15,0)
        final_time = datetime(2015,2,18,16,0)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),60)


    def test_tarifa_minuto_un_dia_menos_un_minuto(self): # Borde
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,18,23,59)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),1439)

    def test_tarifa_minuto_un_dia(self): # Borde
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,0)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),1440)

    def test_tarifa_minuto_un_dia_mas_un_minuto(self): # TDD
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,1)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),1441)

    def test_tarifa_minuto_un_dia_antes_de_la_medianoche_mas_un_minuto(self): # Borde
        initial_time = datetime(2015,2,18,23,59)
        final_time = datetime(2015,2,20,0,0)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),1441)

    def test_tarifa_minuto_siete_dias(self): # Esquina
        initial_time = datetime(2015,2,18,23,59)
        final_time = datetime(2015,2,25,23,59)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time),7*24*60)

    # Pruebas para la clase tarifa hora

    def test_tarifa_hora_una_hora(self): # TDD
        rate = TarifaHora(tarifa = 800)
        initial_datetime = datetime(2015,2,18,13,0)
        final_datetime = datetime(2015,2,18,14,0)
        value = rate.calcularPrecio(initial_datetime, final_datetime)
        self.assertEquals(value, 800)

    def test_tarifa_hora_mas_de_una_hora(self): # TDD
        rate = TarifaHora(tarifa = 800)
        initial_datetime = datetime(2015,2,18,6,8)
        final_datetime = datetime(2015,2,18,7,9)
        value = rate.calcularPrecio(initial_datetime, final_datetime)
        self.assertEquals(value, 1600)

    def test_tarifa_hora_menos_de_una_hora(self): # Borde
        rate = TarifaHora(tarifa = 800)
        initial_datetime = datetime(2015,2,18,11,0)
        final_datetime = datetime(2015,2,18,11,15)
        value = rate.calcularPrecio(initial_datetime, final_datetime)
        self.assertEquals(value, 800)

    def test_tarifa_hora_dia_completo_menos_un_minuto(self): # Borde
        rate=TarifaHora(tarifa=1)
        initial_time=datetime(2015,2,18,0,0)
        final_time=datetime(2015,2,18,23,59)
        value = rate.calcularPrecio(initial_time, final_time)
        self.assertEqual(value, 24)

    def test_tarifa_hora_dia_completo(self): # Borde
        rate=TarifaHora(tarifa=1)
        initial_time=datetime(2015,2,18,0,0)
        final_time=datetime(2015,2,19,0,0)
        value = rate.calcularPrecio(initial_time, final_time)
        self.assertEqual(value, 24)

    def test_dia_completo_mas_un_minuto(self):
        rate=TarifaHora(tarifa=1)
        initial_time=datetime(2015,2,18,0,0)
        final_time=datetime(2015,2,19,0,1)
        value = rate.calcularPrecio(initial_time, final_time)
        self.assertEqual(value, 25)

    def test_tarifa_hora_siete_dias(self):
        rate=TarifaHora(tarifa=1)
        initial_time=datetime(2015,2,18,0,0)
        final_time=datetime(2015,2,25,0,0)
        value = rate.calcularPrecio(initial_time, final_time)
        self.assertEqual(value, 24*7)

    # Casos de decimales

    def test_tarifa_hora_decimal(self):
        rate=TarifaHora(tarifa=0.3)
        initial_time=datetime(2015,2,20,15,0)
        final_time=datetime(2015,2,20,18,0)
        value = rate.calcularPrecio(initial_time, final_time)
        self.assertEqual(value, Decimal('0.9'))

    def test_tarifa_minuto_decimal(self):
        rate=TarifaMinuto(tarifa=0.3)
        initial_time=datetime(2015,2,20,15,0)
        final_time=datetime(2015,2,20,18,30)
        value = rate.calcularPrecio(initial_time, final_time)
        self.assertEqual(value, Decimal('1.05'))

    def test_tarifa_hora_y_fraccion_decimal(self):
        rate=TarifaHorayFraccion(tarifa=0.3)
        initial_time=datetime(2015,2,20,15,0)
        final_time=datetime(2015,2,20,17,25)
        value = rate.calcularPrecio(initial_time, final_time)
        self.assertEqual(value, Decimal('0.75'))
        
    def test_tarifa_pico_decimal(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=0.1,tarifa2=0.3,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,15)
        finReserva = datetime(2015,1,1,20)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,Decimal('1.10'))
        
    def test_tarifa_fin_de_semana_decimal(self):
        tarifa = TarifaFinDeSemana(tarifa=0.1,tarifa2=0.3)
        inicioReserva = datetime(2015,3,6,22)
        finReserva = datetime(2015,3,7,3)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,Decimal('1.10'))

###################################################################
# Tarifa por minuto con hora pico
###################################################################

class HoraPicoTestCase(TestCase):

    def test_tarifa_hora_pico_valle_de_una_hora(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=120,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,4)
        finReserva = datetime(2015,1,1,5)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,60)

    def test_tarifa_hora_pico_valle_valle_por_media_hora(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=120,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,4,30)
        finReserva = datetime(2015,1,1,5)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,30)

    def test_tarifa_hora_pico_valle_valle_por_cuarto_de_hora(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=120,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,4,45)
        finReserva = datetime(2015,1,1,5)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,15)

    def test_tarifa_hora_pico_valle_pico_por_una_hora(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=120,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,7)
        finReserva = datetime(2015,1,1,8)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,120)

    def test_tarifa_hora_pico_valle_pico_por_media(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=100,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,7,30)
        finReserva = datetime(2015,1,1,8)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,50)

    def test_tarifa_hora_pico_valle_pico_por_15_minutos(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=100,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,7,45)
        finReserva = datetime(2015,1,1,8)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,25)

    def test_tarifa_hora_pico_valle_una_hora_mitad_y_mitad(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=100,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,5,30)
        finReserva = datetime(2015,1,1,6,30)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,80)

    def test_tarifa_hora_pico_valle_una_hora_15_minutos_y_3_cuartos_de_hora(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=100,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,5,45)
        finReserva = datetime(2015,1,1,6,45)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,90)

    def test_tarifa_hora_pico_valle_dos_horas_diferentes_dias(self):
        inicio = time(0,0)
        fin = time(12,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=100,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,23)
        finReserva = datetime(2015,1,2,1)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,160)

    ###################
    #      Bordes
    ###################

    def test_tarifa_hora_pico_valle_borde_inferior_de_valle(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=100,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,5)
        finReserva = datetime(2015,1,1,6)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,60)

    def test_tarifa_hora_pico_valle_borde_superior_de_pico(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=100,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,18)
        finReserva = datetime(2015,1,1,19)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,60)

    def test_tarifa_hora_pico_valle_borde_inferior_de_pico(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=100,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,6)
        finReserva = datetime(2015,1,1,7)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,100)

    def test_tarifa_hora_pico_valle_pico_debajo_de_un_borde(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=100,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,17)
        finReserva = datetime(2015,1,1,18)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,100)

    def test_tarifa_hora_pico_valle_valle_de_un_minuto(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=120,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,5,59)
        finReserva = datetime(2015,1,1,6,59)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,119)

    def test_tarifa_hora_pico_valle_pico_de_un_minuto(self):
        inicio = time(6,0)
        fin = time(18,0)
        tarifa = TarifaHoraPico(tarifa=60,tarifa2=120,inicioEspecial=inicio,finEspecial=fin)
        inicioReserva = datetime(2015,1,1,5,1)
        finReserva = datetime(2015,1,1,6,1)
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,61)

###################################################################
# Tarifa diferenciada para fines de semana
###################################################################

class FinDeSemanaTestCase(TestCase):
    # Bordes:   6 * 11
    # Esquinas: 2
    # Malicia:  2 * 10

    # Semana 2015-03-(09..15):
    # Lu Ma Mi Ju Vi Sá Do
    # 09 10 11 12 13 14 15
    # Semana 2015-03-(16..15):
    # Lu Ma Mi Ju Vi Sá Do
    # 16 17 18 19 20 21 22
    def test_tarifa_fin_de_semana_n_horas_desde_la_medianoche_antes_del_lunes(self): #(11) bordes
        for n in range(11):
            tarifa = TarifaFinDeSemana(tarifa=2,tarifa2=5)
            inicioReserva = datetime(2015,3,9,0,0) #medianoche domingo-lunes
            finReserva = inicioReserva + timedelta(hours=n+1) # n+1 horas más tarde
            valor = tarifa.calcularPrecio(inicioReserva,finReserva)
            self.assertEqual(valor,2*(n+1))

    def test_tarifa_fin_de_semana_n_horas_hasta_la_medianoche_antes_del_sabado(self): #(11) bordes
        for n in range(11):
            tarifa = TarifaFinDeSemana(tarifa=2,tarifa2=5)
            finReserva = datetime(2015,3,14,0,0) #medianoche viernes-sábado
            inicioReserva = finReserva - timedelta(hours=n+1) # n+1 horas más temprano
            valor = tarifa.calcularPrecio(inicioReserva,finReserva)
            self.assertEqual(valor,2*(n+1))

    def test_tarifa_fin_de_semana_n_horas_desde_la_medianoche_antes_del_sabado(self): #(11) bordes
        for n in range(11):
            tarifa = TarifaFinDeSemana(tarifa=2,tarifa2=5)
            inicioReserva = datetime(2015,3,14,0,0) #medianoche viernes-sábado
            finReserva = inicioReserva + timedelta(hours=n+1) # n+1 horas más tarde
            valor = tarifa.calcularPrecio(inicioReserva,finReserva)
            self.assertEqual(valor,5*(n+1))

    def test_tarifa_fin_de_semana_n_horas_hasta_la_medianoche_antes_del_lunes(self): #(11) bordes
        for n in range(11):
            tarifa = TarifaFinDeSemana(tarifa=2,tarifa2=5)
            finReserva = datetime(2015,3,9,0,0) #medianoche domingo-lunes
            inicioReserva = finReserva - timedelta(hours=n+1) # n+1 horas más temprano
            valor = tarifa.calcularPrecio(inicioReserva,finReserva)
            self.assertEqual(valor,5*(n+1))

    def test_tarifa_fin_de_semana_semana_de_trabajo_completa(self): #esquina
        tarifa = TarifaFinDeSemana(tarifa=2,tarifa2=5)
        inicioReserva = datetime(2015,3,9,0,0) #medianoche domingo-lunes
        finReserva = datetime(2015,3,14,0,0) #medianoche viernes-sábado
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,2*24*5)

    def test_tarifa_fin_de_semana_fin_de_semana_completo(self): #esquina
        tarifa = TarifaFinDeSemana(tarifa=2,tarifa2=5)
        inicioReserva = datetime(2015,3,14,0,0) #medianoche viernes-sábado
        finReserva = datetime(2015,3,16,0,0) #medianoche domingo-lunes
        valor = tarifa.calcularPrecio(inicioReserva,finReserva)
        self.assertEqual(valor,5*24*2)

    def test_tarifa_fin_de_semana_n_horas_domingo_lunes(self): #(11) bordes
        for n in range(11):
            tarifa = TarifaFinDeSemana(tarifa=2,tarifa2=5)
            inicioReserva = datetime(2015,3,15,14,0) + timedelta(hours=n) #domingo en la tarde
            finReserva = inicioReserva + timedelta(hours=10) # diez horas más tarde
            valor = tarifa.calcularPrecio(inicioReserva,finReserva)
            self.assertEqual(valor, 5*(10-n) + 2*n)

    def test_tarifa_fin_de_semana_n_horas_viernes_sabado(self): #(11) bordes
        for n in range(11):
            tarifa = TarifaFinDeSemana(tarifa=2,tarifa2=5)
            inicioReserva = datetime(2015,3,13,14,0) + timedelta(hours=n) #viernes en la tarde
            finReserva = inicioReserva + timedelta(hours=10) # diez horas más tarde
            valor = tarifa.calcularPrecio(inicioReserva,finReserva)
            self.assertEqual(valor, 2*(10-n) + 5*n)

    def test_tarifa_fin_de_semana_n_horas_domingo_lunes_empezando_a_un_cuarto_de_hora(self): #(10) malicia
        for n in range(10):
            tarifa = TarifaFinDeSemana(tarifa=2,tarifa2=5)
            inicioReserva = datetime(2015,3,15,14,15) + timedelta(hours=n) #domingo en la tarde
            finReserva = inicioReserva + timedelta(hours=10) # diez horas más tarde
            valor = tarifa.calcularPrecio(inicioReserva,finReserva)
            self.assertEqual(valor, 5*(9.75-n) + 2*(n+.25))

    def test_tarifa_fin_de_semana_n_horas_viernes_sabado_empezando_a_un_cuarto_de_hora(self): #(10) malicia
        for n in range(10):
            tarifa = TarifaFinDeSemana(tarifa=2,tarifa2=5)
            inicioReserva = datetime(2015,3,13,14,15) + timedelta(hours=n) #viernes en la tarde
            finReserva = inicioReserva + timedelta(hours=10) # diez horas más tarde
            valor = tarifa.calcularPrecio(inicioReserva,finReserva)
            self.assertEqual(valor, 2*(9.75-n) + 5*(n+.25))
