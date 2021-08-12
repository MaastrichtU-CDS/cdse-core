import os
import socket
import uuid
from random import randint

import docker

from .exceptions import DockerEngineFailedException


def run_model_container(image_name, image_id, port, secret_token, invocation_url):
    try:
        client = docker.from_env()
        client.containers.run(
            image_name + "@" + image_id,
            auto_remove=True,
            detach=True,
            ports={str(port) + "/tcp": port},
            environment=[
                "PORT=" + str(port),
                "INVOCATION_HOST=" + invocation_url,
                "SECRET_TOKEN=" + str(secret_token),
                "TEMPLATE_DIR=template" "STATIC_DIR=static" "DEBUG=False",
                "ALLOWED_HOSTS=localhost 127.0.0.1 0.0.0.0",
            ],
        )
    except Exception:
        raise DockerEngineFailedException()


def prepare_container_properties(image_name, image_id):
    invocation_host = "http://" + os.environ.get("INVOCATION_HOST", "localhost")
    invocation_port = ":" + os.environ.get("INVOCATION_PORT", "8000")
    api_route = "/api/v1"
    port = generate_random_open_port()
    secret_token = uuid.uuid4()
    invocation_url = invocation_host + invocation_port + api_route

    return {
        "image_name": image_name,
        "image_id": image_id,
        "invocation_url": invocation_url,
        "port": port,
        "secret_token": secret_token,
    }


def generate_random_open_port():
    host = os.environ.get("INVOCATION_HOST", "localhost")
    is_open = False

    while not is_open:
        selected_port = randint(8000, 9000)
        is_open = is_port_available(host, selected_port)

    return selected_port


def is_port_available(host, selected_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, selected_port))
    if result == 0:
        return False
    else:
        return True
