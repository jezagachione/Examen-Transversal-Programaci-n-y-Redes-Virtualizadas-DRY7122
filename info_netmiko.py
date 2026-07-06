from netmiko import ConnectHandler
import sys

# Datos de conexion al CSR1000v
csr1000v = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.105',  # 
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'cisco123!',     
}

# 1. Comandos de configuracion OSPF IPv4 e IPv6 con Area 0 e Interfaces Pasivas
comandos_ospf = [
    # Habilitar enrutamiento IPv6
    'ipv6 unicast-routing',
    
    # OSPFv2 (IPv4) - Proceso 1, Router-ID 1.1.1.1, Area 0
    'router ospf 1',
    ' router-id 1.1.1.1',
    ' passive-interface default',
    ' no passive-interface Loopback44',
    ' network 0.0.0.0 255.255.255.255 area 0',
    ' exit',
    
    # OSPFv3 (IPv6) - Proceso 1, Router-ID 2.2.2.2, Area 0 en Loopback44
    'ipv6 router ospf 1',
    ' router-id 2.2.2.2',
    ' passive-interface default',
    ' no passive-interface Loopback44',
    ' exit',
    'interface Loopback44',
    ' ipv6 ospf 1 area 0',
    ' exit'
]

def main():
    print("--- Conectando a CSR1000v mediante Netmiko ---")
    try:
        net_connect = ConnectHandler(**csr1000v)
        net_connect.enable()
        print("✅ Conexión exitosa al router.\n")

        # 1. Configurar OSPF clásico IPv4/IPv6
        print("-> Configurando OSPF IPv4 e IPv6 con Área 0 e Interfaces Pasivas...")
        salida_config = net_connect.send_config_set(comandos_ospf)
        net_connect.save_config()  # Guardar cambios (write memory)
        print("✅ Configuración OSPF aplicada y guardada correctamente.\n")
        print("="*60)

        # 2. Demostrar el resultado con: show running-config | section ospf
        print("RESULTADO DEMOSTRACIÓN: show running-config | section ospf")
        print("="*60)
        salida_ospf = net_connect.send_command('show running-config | section ospf')
        print(salida_ospf)
        print("\n" + "="*60)

        # 3. Obtener información de las IP y estado de las interfaces
        print("RESULTADO: Información y estado de interfaces (show ip int brief)")
        print("="*60)
        salida_int = net_connect.send_command('show ip interface brief')
        print(salida_int)
        print("\n" + "="*60)

        # 4. Obtener el show version
        print("RESULTADO: Información de versión del sistema (show version)")
        print("="*60)
        salida_ver = net_connect.send_command('show version')
        # Imprimimos solo las primeras 25 líneas para no inundar la pantalla
        print("\n".join(salida_ver.splitlines()[:25]))
        print("\n[... Salida recortada para visualización ...]\n")
        print("="*60)

        # 5. Obtener el running-config completo y guardarlo en un archivo
        print("RESULTADO: Obtener el running-config")
        print("="*60)
        salida_run = net_connect.send_command('show running-config')
        
        # Como el running-config es largo, lo guardamos en un archivo local
        with open('netmiko_running_config.txt', 'w') as f:
            f.write(salida_run)
        print("✅ Running-config obtenido exitosamente y guardado en 'netmiko_running_config.txt'")
        print("="*60)

        net_connect.disconnect()

    except Exception as e:
        print(f"❌ Error al ejecutar script con Netmiko:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
