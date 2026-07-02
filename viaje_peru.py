import requests
import urllib.parse

# URLs de Graphhopper
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "952bbad1-0769-4c67-9b16-2a0054387e8d"
while True:
    print("\n" + "="*40)
    origen = input("Ingrese la Ciudad de Origen (o 's' para salir): ")
    if origen.lower() == "s":
        print("Saliendo del programa...")
        break

    destino = input("Ingrese la Ciudad de Destino (o 's' para salir): ")
    if destino.lower() == "s":
        print("Saliendo del programa...")
        break

    print("\nOpciones de transporte: 1. Auto (car) | 2. Bicicleta (bike) | 3. A pie (foot)")
    transporte_input = input("Ingrese el medio de transporte (car/bike/foot) o 's' para salir: ").lower()
    
    if transporte_input == 's':
        print("Saliendo del programa...")
        break
    elif transporte_input not in ['auto', 'bike', 'foot']:
        print("Opcion no válida. Se utilizará 'car' por defecto.")
        transporte_input = 'car'

    try:
        # Geocodificación de origen
        url_origen = geocode_url + urllib.parse.urlencode({"q": origen, "limit": "1", "key": key})
        datos_origen = requests.get(url_origen).json()
        lat_origen = datos_origen['hits'][0]['point']['lat']
        lng_origen = datos_origen['hits'][0]['point']['lng']

        # Geocodificación de destino
        url_destino = geocode_url + urllib.parse.urlencode({"q": destino, "limit": "1", "key": key})
        datos_destino = requests.get(url_destino).json()
        lat_destino = datos_destino['hits'][0]['point']['lat']
        lng_destino = datos_destino['hits'][0]['point']['lng']

        # Solicitud de ruta
        params_route = {
            "point": [f"{lat_origen},{lng_origen}", f"{lat_destino},{lng_destino}"],
            "locale": "es",  # Traduce las indicaciones al español
            "vehicle": transporte_input,
            "key": key
        }
        url_route = route_url + urllib.parse.urlencode(params_route, doseq=True)
        ruta = requests.get(url_route).json()

        if "paths" in ruta:
            # Extracción de datos
            distancia_m = ruta['paths'][0]['distance']
            tiempo_ms = ruta['paths'][0]['time']

            # Cálculos de distancia
            distancia_km = round(distancia_m / 1000, 2)
            distancia_mi = round(distancia_km * 0.621371, 2) # Factor de conversión km a millas

            # Cálculos de tiempo (de milisegundos a formato hh:mm:ss)
            tiempo_segundos = tiempo_ms / 1000
            horas = int(tiempo_segundos // 3600)
            minutos = int((tiempo_segundos % 3600) // 60)
            segundos = int(tiempo_segundos % 60)

            # Mostrar resultados requeridos
            print("\n" + "*"*40)
            print("=== RESUMEN DEL VIAJE ===")
            print(f"Distancia total: {distancia_km} km / {distancia_mi} millas")
            print(f"Duración del viaje: {horas} horas, {minutos} minutos, {segundos} segundos")
            print("*"*40 + "\n")

            print("=== NARRATIVA DEL VIAJE ===")
            for step in ruta['paths'][0]['instructions']:
                distancia_step_km = round(step['distance'] / 1000, 2)
                print(f"- {step['text']} ({distancia_step_km} km)")
        else:
            print("\nError: No se pudo encontrar una ruta terrestre entre estas ciudades con el transporte seleccionado.")

    except IndexError:
        print("\nError: Una de las ciudades no pudo ser geolocalizada. Verifica los nombres ingresados.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado al conectar con Graphhopper: {e}")
