def evaluar_as(asn):
    # Rangos de AS Privados (16-bit y 32-bit)
    if (64512 <= asn <= 65534) or (4200000000 <= asn <= 4294967294):
        return "Privado"
    # Documentación o Reservados especiales
    elif asn == 0 or asn == 65535 or (65536 <= asn <= 65551) or asn == 4294967295:
        return "Reservado / Uso especial"
    else:
        return "Público"

def main():
    print("=== Verificador de Sistema Autónomo (ASN) BGP ===")
    try:
        asn_input = input("Ingrese el número de AS de BGP a verificar: ")
        asn = int(asn_input)
        
        # Validación de rango general de ASN
        if asn < 0 or asn > 4294967295:
            print("Error: El número de ASN no es válido (rango de 0 a 4294967295).")
        else:
            resultado = evaluar_as(asn)
            print(f"El AS {asn} es un Sistema Autónomo de tipo: {resultado}")
            
    except ValueError:
        print("Error: Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    main()
