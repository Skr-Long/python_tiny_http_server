import socket
import logging

server_recv_len = 2048

HTTP_HEAD_TEMPLATE = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Content-Length: {0}\r\n"
    "\r\n"
)

def read_html(filepath):
    context = ""
    with open(filepath, "r") as html:
        for line in html:
            context += line
    return context


def init_log_config():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # 可以设置为 DEBUG、INFO、WARNING、ERROR 或 CRITICAL
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def process_request(client_socket, client_address):
    logging.info(f"Connection from {client_address}.")

    data = client_socket.recv(server_recv_len)
    logging.info(f"{data}")
    
    try:
        http_context = read_html("asset/index.html")
        http_head = HTTP_HEAD_TEMPLATE.format(len(http_context))
        msg = http_head + http_context
        data = msg.encode()
        client_socket.sendall(data)
    except TypeError as type_error:
        logging.warning("catch exception: %s", type_error)
    finally:
        client_socket.close()


def tcp_server():
    server_ip = '0.0.0.0'
    server_port = 10034
    server_listen_num = 10

    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(server_listen_num)

        logging.info(f"Server listening on {server_ip}:{server_port}")
        while True:
            client_socket, client_address = server_socket.accept()
            process_request(client_socket, client_address)


if __name__ == "__main__":
    init_log_config()
    tcp_server()
        
        
        
        
        