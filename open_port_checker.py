import socket

def is_port_available(port):
    print(f"Verificando se a porta {port} está disponível...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", port))
        return True  # A porta está disponível
    except (OSError, ConnectionError):
        return False  # A porta não está disponível

# # Exemplo de uso
# port_number = 5000  # Número da porta que você deseja verificar

# if is_port_available(port_number):
#     print(f"A porta {port_number} está disponível.")
# else:
#     print(f"A porta {port_number} não está disponível.")