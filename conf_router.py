
from ncclient import manager
import sys

# Parámetros de conexión del CSR1000v
ROUTER_HOST = "192.168.56.105"  
ROUTER_USER = "cisco"
ROUTER_PASS = "cisco123!"
ROUTER_PORT = 830

# 1. Modelo XML YANG para cambiar el Hostname (Apellidos de integrantes)
# MODIFICA LOS APELLIDOS ABAJO:
payload_hostname = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>Zagachione-Torres</hostname>
  </native>
</config>
"""

# 2. Modelo XML YANG para crear la Loopback 111 con IP 111.111.111.111/32
payload_loopback = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>111</name>
        <ip>
          <address>
            <primary>
              <address>111.111.111.111</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

def main():
    print(f"--- Conectando al router CSR1000v ({ROUTER_HOST}) mediante NETCONF ---")
    try:
        # Estableciendo la sesión NETCONF
        with manager.connect(
            host=ROUTER_HOST,
            port=ROUTER_PORT,
            username=ROUTER_USER,
            password=ROUTER_PASS,
            hostkey_verify=False,
            device_params={'name': 'iosxe'}
        ) as m:
            print(" Conexión NETCONF exitosa.")

            # Aplicar cambio de Hostname
            print("Enviando configuración para cambiar el Hostname...")
            respuesta_host = m.edit_config(target="running", config=payload_hostname)
            if "<ok/>" in str(respuesta_host):
                print("Hostname actualizado correctamente.")
            
            # Aplicar creación de Loopback 111
            print("Enviando configuración de la interfaz Loopback 111...")
            respuesta_loop = m.edit_config(target="running", config=payload_loopback)
            if "<ok/>" in str(respuesta_loop):
                print(" Interfaz Loopback 111 (111.111.111.111/32) creada correctamente.")

            print("\n¡Configuración completada con éxito en la running-config!")

    except Exception as e:
        print(f" Error al conectar o configurar mediante NETCONF:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
