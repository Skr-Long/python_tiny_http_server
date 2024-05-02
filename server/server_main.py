import socket
import logging

http_context = "<html><body><h1>Hello Server!</h1></body></html>"

context_len = len(http_context)
http_head = (
    f"HTTP/1.1 200 OK\r\n"
    f"Content-Type: text/html\r\n"
    f"Content-Length: {context_len}\r\n"
    f"\r\n"
)

def init_log(filename):
    logging.basicConfig(filename=filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def tcp_server():
    server_ip = '0.0.0.0'
    server_port = 10034
    server_listen_num = 10
    server_recv_len = 2048
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(server_listen_num)

        logging.info(f"Server listening on {server_ip}:{server_port}")
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info(f"Connection from {client_address}.")

            data = client_socket.recv(server_recv_len)
            logging.info(f"{data}")
            
            try:
                msg = http_head + http_context
                data = msg.encode()
                client_socket.sendall(data)
            except TypeError as type_error:
                logging.warning("catch exception: %s", type_error)
            finally:
                client_socket.close()

if __name__ == "__main__":
    init_log("log/run.log")
    tcp_server()
        
        
        
        
        