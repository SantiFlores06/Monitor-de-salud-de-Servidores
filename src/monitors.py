from abc import ABC, abstractmethod
import paramiko

# --- 1. La Interfaz (Contrato) ---
class IServidorMonitor(ABC):
    """Interfaz base para cualquier tipo de monitor de servidor."""
    
    @abstractmethod
    def conectar(self, credenciales=None):
        pass

    @abstractmethod
    def obtener_metricas(self):
        pass

    @abstractmethod
    def cerrar(self):
        pass

# --- 2. Implementación Concreta: SSH para Linux ---
class MonitorSSHLinux(IServidorMonitor):
    """Implementación específica para monitorear servidores Linux vía SSH."""
    
    def __init__(self, ip, usuario, puerto=22):
        self.ip = ip
        self.usuario = usuario
        self.puerto = puerto
        self.cliente = None

    def conectar(self, credenciales=None):
        try:
            self.cliente = paramiko.SSHClient()
            self.cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            print(f"[*] [SSH] Conectando a {self.usuario}@{self.ip}:{self.puerto}...")
            # En un entorno real, 'credenciales' podría ser la ruta a una clave privada RSA
            self.cliente.connect(
                hostname=self.ip,
                port=self.puerto,
                username=self.usuario,
                password=credenciales, 
                timeout=5
            )
            print(f"[+] [SSH] Conexión exitosa a {self.ip}")
            return True
        except Exception as e:
            print(f"[-] [SSH] Error conectando a {self.ip}: {e}")
            return False

    def obtener_metricas(self):
        if not self.cliente:
            return None
        # ... (Aquí iría la lógica de comandos bash que vimos antes) ...
        print(f"[*] [SSH] Extrayendo métricas de {self.ip} (Simulado)")
        return {"cpu": 45.5, "ram": 60.2, "disco": 75.0} # Datos simulados por ahora

    def cerrar(self):
        if self.cliente:
            self.cliente.close()
            print(f"[*] [SSH] Conexión cerrada ({self.ip}).")

# --- 3. El Factory Method ---
class MonitorFactory:
    """Fábrica que decide qué tipo de monitor instanciar basado en el tipo."""
    
    @staticmethod
    def crear_monitor(tipo_servidor, ip, usuario, puerto):
        if tipo_servidor.lower() == "linux_ssh":
            return MonitorSSHLinux(ip, usuario, puerto)
        # Aquí es donde el principio Open/Closed brilla. 
        # Si mañana agregamos Windows, solo agregamos un 'elif' aquí:
        # elif tipo_servidor.lower() == "windows_wmi":
        #     return MonitorWindowsWMI(ip, usuario)
        else:
            raise ValueError(f"Tipo de servidor '{tipo_servidor}' no soportado.")