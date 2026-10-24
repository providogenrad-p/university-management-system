import json
import socket


class HTTPClient:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port

    def get(self, path):
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        return self._send(request)

    def post(self, path, data):
        body = json.dumps(data)
        body_bytes = body.encode("utf-8")
        request = (
            f"POST {path} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(body_bytes)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            + body
        )
        return self._send(request)

    def _send(self, request):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        try:
            sock.connect((self.host, self.port))
        except OSError:
            sock.close()
            raise ConnectionError("Application Server is unavailable.")

        try:
            sock.sendall(request.encode("utf-8"))

            # The server sends "Connection: close",
            # so read until it closes the connection.
            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
        except OSError:
            raise ConnectionError("Application Server is unavailable.")
        finally:
            sock.close()

        return self._parse_response(response)

    def _parse_response(self, response):
        response_text = response.decode("utf-8")
        headers, body = response_text.split("\r\n\r\n", 1)

        status_line = headers.split("\r\n")[0]  # HTTP/1.1 201 Created
        status = int(status_line.split()[1])

        data = json.loads(body) if body else None

        if status >= 400:
            raise ValueError(data["error"])

        return data