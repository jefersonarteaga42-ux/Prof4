"""
Modulo gestor central de Software FJ.
Administra listas internas de clientes, servicios y reservas en memoria,
aplicando bloques try/except/else/finally y logging exhaustivo.
"""

from typing import List, Optional
from models import Cliente, Servicio, Reserva
from exceptions import SoftwareFJError, DatosInvalidosError, ReservaInvalidaError
from logger_config import configurar_logger


class SistemaSoftwareFJ:
    """Controlador principal que mantiene la integridad operativa en memoria."""

    def __init__(self):
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []
        self.logger = configurar_logger()
        self.logger.info("=== Sistema Integral Software FJ iniciado en memoria ===")

    def registrar_cliente(self, cliente: Cliente) -> bool:
        """Registra un cliente validando duplicados con try/except/else/finally."""
        exito = False
        try:
            if any(c.id_entidad == cliente.id_entidad for c in self._clientes):
                raise DatosInvalidosError(f"Ya existe un cliente registrado con ID '{cliente.id_entidad}'.")
            self._clientes.append(cliente)
        except SoftwareFJError as e:
            self.logger.error(f"[REGISTRO CLIENTE FALLIDO] {type(e).__name__}: {e}")
        else:
            exito = True
            self.logger.info(f"[CLIENTE REGISTRADO] {cliente.obtener_resumen()}")
        finally:
            self.logger.debug(f"Auditoria clientes: total en memoria = {len(self._clientes)}")
        return exito

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Agrega un servicio al catalogo interno."""
        try:
            if any(s.id_entidad == servicio.id_entidad for s in self._servicios):
                raise DatosInvalidosError(f"Ya existe un servicio con ID '{servicio.id_entidad}'.")
            self._servicios.append(servicio)
        except SoftwareFJError as e:
            self.logger.error(f"[REGISTRO SERVICIO FALLIDO] {type(e).__name__}: {e}")
            return False
        else:
            self.logger.info(f"[SERVICIO REGISTRADO] {servicio.obtener_resumen()}")
            return True

    def buscar_cliente(self, id_cliente: str) -> Cliente:
        for c in self._clientes:
            if c.id_entidad == id_cliente.strip().upper():
                return c
        raise DatosInvalidosError(f"Cliente con ID '{id_cliente}' no encontrado en el sistema.")

    def buscar_servicio(self, id_servicio: str) -> Servicio:
        for s in self._servicios:
            if s.id_entidad == id_servicio.strip().upper():
                return s
        raise DatosInvalidosError(f"Servicio con ID '{id_servicio}' no encontrado en el catalogo.")

    def crear_y_confirmar_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion_horas: float,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        recargo_extra: Optional[float] = None
    ) -> Optional[Reserva]:
        """
        Orquesta la creacion y confirmacion de una reserva con manejo completo
        de excepciones y encadenamiento de errores.
        """
        reserva_creada = None
        try:
            if any(r.id_entidad == id_reserva.strip().upper() for r in self._reservas):
                raise ReservaInvalidaError(f"El ID de reserva '{id_reserva}' ya existe.")

            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)

            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion_horas)
            nueva_reserva.confirmar(impuesto=impuesto, descuento=descuento, recargo_extra=recargo_extra)
            self._reservas.append(nueva_reserva)
            reserva_creada = nueva_reserva

        except SoftwareFJError as e:
            self.logger.error(f"[RESERVA RECHAZADA - {id_reserva}] {type(e).__name__}: {e}")
        except Exception as e:
            self.logger.critical(f"[ERROR INESPERADO EN RESERVA - {id_reserva}] {e}", exc_info=True)
        else:
            self.logger.info(f"[RESERVA EXITOSA] {reserva_creada.obtener_resumen()}")
        finally:
            self.logger.debug(f"Auditoria reservas: total registradas = {len(self._reservas)}")

        return reserva_creada

    def procesar_reserva(self, id_reserva: str) -> bool:
        try:
            reserva = next((r for r in self._reservas if r.id_entidad == id_reserva.strip().upper()), None)
            if not reserva:
                raise ReservaInvalidaError(f"No existe la reserva '{id_reserva}'.")
            reserva.procesar()
        except SoftwareFJError as e:
            self.logger.error(f"[PROCESAMIENTO FALLIDO - {id_reserva}] {e}")
            return False
        else:
            self.logger.info(f"[RESERVA PROCESADA] {reserva.obtener_resumen()}")
            return True

    def cancelar_reserva(self, id_reserva: str) -> bool:
        try:
            reserva = next((r for r in self._reservas if r.id_entidad == id_reserva.strip().upper()), None)
            if not reserva:
                raise ReservaInvalidaError(f"No existe la reserva '{id_reserva}'.")
            reserva.cancelar()
        except SoftwareFJError as e:
            self.logger.error(f"[CANCELACION FALLIDA - {id_reserva}] {e}")
            return False
        else:
            self.logger.info(f"[RESERVA CANCELADA] {reserva.obtener_resumen()}")
            return True
