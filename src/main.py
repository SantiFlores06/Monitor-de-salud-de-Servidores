import yaml
import os
from monitors import MonitorFactory # Importamos el Factory

# ... (La función cargar_configuracion() se queda igual) ...
def cargar_configuracion(ruta_archivo):
    # ... código de lectura YAML ...
    pass # Asumimos que esta función ya la tenés

if __name__ == "__main__":
    ruta_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yaml')
    configuracion = cargar_configuracion(ruta_config)
    
    if configuracion:
        print("Iniciando Monitoreo con Arquitectura Factory...\n")
        
        # Iteramos sobre la lista de servidores del YAML
        for server_data in configuracion['servers']:
            try:
                # 1. El Factory nos da el objeto correcto sin que nosotros sepamos qué clase es
                monitor = MonitorFactory.crear_monitor(
                    tipo_servidor=server_data.get('type', 'linux_ssh'), # Por defecto linux_ssh
                    ip=server_data['ip'],
                    usuario=server_data['user'],
                    puerto=server_data.get('port', 22)
                )
                
                # 2. Polimorfismo en acción: No importa qué monitor sea, todos responden a esto
                if monitor.conectar():
                    metricas = monitor.obtener_metricas()
                    print(f"    Métricas: {metricas}")
                    monitor.cerrar()
                    
            except ValueError as e:
                print(f"[!] Error de configuración: {e}")
            print("-" * 30)