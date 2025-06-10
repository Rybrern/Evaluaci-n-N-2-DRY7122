import requests
import sys 

# Configuración de la API
API_KEY = '5b3ce3597851110001cf62488f23c2a4677a45feb240e70290895a7a' 
BASE_URL = 'https://api.openrouteservice.org/v2/directions/driving-car'

def obtener_coordenadas(ciudad):
    """Obtiene las coordenadas de una ciudad usando OpenRouteService Geocoding"""
    geocode_url = f"https://api.openrouteservice.org/geocode/search?api_key={API_KEY}&text={ciudad}"
    try:
        response = requests.get(geocode_url)
        data = response.json()
        if data['features']:
            lon, lat = data['features'][0]['geometry']['coordinates']
            return [lon, lat]
        else:
            print(f"No se encontraron coordenadas para {ciudad}")
            return None
    except Exception as e:
        print(f"Error al obtener coordenadas: {e}")
        return None

def calcular_ruta(origen, destino):
    """Calcula la ruta entre dos puntos usando OpenRouteService"""
    coords_origen = obtener_coordenadas(origen)
    coords_destino = obtener_coordenadas(destino)
    
    if not coords_origen or not coords_destino:
        return None
    
    params = {
        'api_key': API_KEY,
        'start': f"{coords_origen[0]},{coords_origen[1]}",
        'end': f"{coords_destino[0]},{coords_destino[1]}"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error al calcular la ruta: {e}")
        return None

def formatear_tiempo(segundos):
    """Convierte segundos a formato horas:minutos:segundos"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = int(segundos % 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def calcular_combustible(distancia_km):
    """Calcula el combustible requerido (asumiendo 8 litros cada 100 km)"""
    consumo_por_km = 8 / 100
    return distancia_km * consumo_por_km

def main():
    print("Bienvenido al calculador de rutas y combustible")
    print("Ingrese las ciudades (o 'q' para salir)")
    
    while True:
        origen = input("\nCiudad de Origen: ").strip()
        if origen.lower() == 'q':
            print("Saliendo del programa...")
            sys.exit(0)
            
        destino = input("Ciudad de Destino: ").strip()
        if destino.lower() == 'q':
            print("Saliendo del programa...")
            sys.exit(0)
        
        ruta_data = calcular_ruta(origen, destino)
        if not ruta_data or 'features' not in ruta_data or not ruta_data['features']:
            print("No se pudo calcular la ruta. Verifique los nombres de las ciudades.")
            continue
        
        # Extraer información de la ruta
        distancia = ruta_data['features'][0]['properties']['segments'][0]['distance'] / 1000  # en km
        duracion = ruta_data['features'][0]['properties']['segments'][0]['duration']  # en segundos
        combustible = calcular_combustible(distancia)
        
        # Mostrar resultados
        print("\n--- Resultados del Viaje ---")
        print(f"Ruta: {origen} -> {destino}")
        print(f"Distancia: {distancia:.2f} km")
        print(f"Duración del viaje: {formatear_tiempo(duracion)}")
        print(f"Combustible requerido: {combustible:.2f} litros (estimado)")
        print("\nNarrativa del viaje:")
        print(f"Para viajar desde {origen} hasta {destino}, deberás recorrer {distancia:.2f} kilómetros.")
        print(f"El tiempo estimado de viaje es de {formatear_tiempo(duracion)}.")
        print(f"Necesitarás aproximadamente {combustible:.2f} litros de combustible para completar este trayecto.")

if __name__ == "__main__":
    main()