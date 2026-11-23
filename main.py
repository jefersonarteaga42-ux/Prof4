"""
Punto de entrada principal de Software FJ.
Simula 12 operaciones completas (validas e invalidas) demostrando
resiliencia, polimorfismo y registro en archivo de logs sin detener ejecucion.
"""

from models import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from manager import SistemaSoftwareFJ
from exceptions import SoftwareFJError


def ejecutar_simulacion():
    sistema = SistemaSoftwareFJ()

    print("\n--- INICIANDO SIMULACION DE 12 OPERACIONES EN SOFTWARE FJ ---\n")

    # OPERACION 1: Registro valido de Cliente 1
    try:
        c1 = Cliente("CLI-001", "Laura Gomez", "laura.gomez@empresa.com", "3104567890")
        sistema.registrar_cliente(c1)
    except SoftwareFJError as e:
        sistema.logger.error(f"Op 1 fallida: {e}")

    # OPERACION 2: Registro valido de Cliente 2
    try:
        c2 = Cliente("CLI-002", "Carlos Mendoza", "cmendoza@tech.co", "3009876543")
        sistema.registrar_cliente(c2)
    except SoftwareFJError as e:
        sistema.logger.error(f"Op 2 fallida: {e}")

    # OPERACION 3 (INVALIDA): Registro de cliente con correo malformado
    try:
        c_invalido = Cliente("CLI-003", "Andres Ruiz", "correo_sin_arroba.com", "3150001122")
        sistema.registrar_cliente(c_invalido)
    except SoftwareFJError as e:
        sistema.logger.error(f"[OP 3 CONTROLADA] Error al instanciar cliente invalido: {e}")

    # OPERACION 4: Registro de Servicio 1 (ReservaSala)
    try:
        s1 = ReservaSala("SRV-001", "Sala Scrum Agil", 80000, capacidad=12, disponible=True)
        sistema.registrar_servicio(s1)
    except SoftwareFJError as e:
        sistema.logger.error(f"Op 4 fallida: {e}")

    # OPERACION 5: Registro de Servicio 2 (AlquilerEquipo)
    try:
        s2 = AlquilerEquipo("SRV-002", "Servidor Dedicado GPU", 120000, deposito_seguridad=50000, disponible=True)
        sistema.registrar_servicio(s2)
    except SoftwareFJError as e:
        sistema.logger.error(f"Op 5 fallida: {e}")

    # OPERACION 6: Registro de Servicio 3 (AsesoriaEspecializada - No disponible)
    try:
        s3 = AsesoriaEspecializada("SRV-003", "Arquitectura Cloud AWS", 150000, nivel_senior=True, disponible=False)
        sistema.registrar_servicio(s3)
    except SoftwareFJError as e:
        sistema.logger.error(f"Op 6 fallida: {e}")

    # OPERACION 7: Reserva valida de Sala por 5 horas (aplica descuento por volumen + IVA)
    sistema.crear_y_confirmar_reserva("RES-001", "CLI-001", "SRV-001", duracion_horas=5)

    # OPERACION 8: Reserva valida de Equipo con descuento comercial del 10%
    sistema.crear_y_confirmar_reserva("RES-002", "CLI-002", "SRV-002", duracion_horas=3, descuento=0.10)

    # OPERACION 9 (INVALIDA): Intento de reservar un servicio no disponible (SRV-003)
    sistema.crear_y_confirmar_reserva("RES-003", "CLI-001", "SRV-003", duracion_horas=2)

    # OPERACION 10 (INVALIDA): Intento de reserva con recargo negativo (encadenamiento de excepcion)
    sistema.crear_y_confirmar_reserva("RES-004", "CLI-002", "SRV-001", duracion_horas=2, recargo_extra=-15000)

    # OPERACION 11: Procesar exitosamente la reserva RES-001
    sistema.procesar_reserva("RES-001")

    # OPERACION 12 (INVALIDA): Intentar cancelar una reserva que ya fue PROCESADA (RES-001)
    sistema.cancelar_reserva("RES-001")

    print("\n--- SIMULACION FINALIZADA. REVISA 'sistema_software_fj.log' ---\n")


if __name__ == "__main__":
    ejecutar_simulacion()
