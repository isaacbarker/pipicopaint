import uasyncio as asyncio
import os
from oled import display_pixels

async def serve_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    # get route and method from request    
    try:
        request_line = await reader.readline()
        parts = request_line.decode().split()
        if len(parts) != 3:
            raise ValueError("Invalid request line format")

        method, path, _ = parts
    except Exception:
        return await respond_text(writer, "Bad request", 400)
    
    # process headers
    try:
        headers = {}
        while True:
            header_bytes = await reader.readline()
            if header_bytes == b"\r\n":
                break # break at end of HTTP headers

            header_line = header_bytes.decode()
            key, value = header_line.split(":", 1)
            headers[key.strip().lower()] = value.strip()
    except Exception as e:
        print("Error when reading headers:", e)
        return await respond_text(writer, "Bad request", 400)
    
    # routing
    if method == "POST" and path == "/":

        """
        Recieves data from client and displays pixel array on OLED screen
        """

        # ensure body is present in request
        if "content-type" not in headers or "content-length" not in headers:
            return await respond_text(writer, "Bad request", 400)
        
        if headers["content-type"] != "application/octet-stream":
            return await respond_text(writer, "Bad request", 400)
        
        content_length = int(headers["content-length"])

        # read body until content length sufficient
        body_bytes = bytearray(content_length)
        read_len = 0
        while read_len < content_length:
            chunk = await reader.read(content_length - read_len)
            if not chunk:
                break
            body_bytes[read_len:read_len+len(chunk)] = chunk
            read_len += len(chunk)
        
        display_pixels(body_bytes)
        
        await respond_text(writer, "OK", 200)

    elif method == "GET" and path == "/":

        """
        Returns base html file for client
        """

        file_path = "./public/index.html"
        await respond_file(writer, file_path)

    elif method == "GET" and path.startswith("/static"):

        """
        Returns static files if available
        """

        file_path = "./public/" + path.split("/")[2]
        await respond_file(writer, file_path)
            
    else:
        
        """
        Returns 404 error if route is not registered
        """

        return await respond_text(writer, "404 Not Found", 404)

def file_exists(path):
    try:
        os.stat(path)
        return True
    except OSError:
        return False

async def respond_text(writer: asyncio.StreamWriter, status_text: str, status_code: int = 200) -> None:
    
    """
    Return basic response with status code and text for error messages and 200 oks
    """

    response = f"HTTP/1.0 {status_code} {status_text}\r\n\r\n"
    writer.write(response.encode())
    await writer.drain()
    await writer.wait_closed()

async def respond_file(writer: asyncio.StreamWriter, file_path: str, status_code=200) -> None:
    
    """
    Serve files from file_path to client
    """

    try:
        use_gzip = False
        gz_path = file_path + ".gz"

        # serve .gz if exists
        if file_exists(gz_path):
            file_path = gz_path
            use_gzip = True

        size = os.stat(file_path)[6]

        # select correct content type
        if ".css" in file_path:
            content_type = "text/css"
        elif ".js" in file_path:
            content_type = "application/javascript"
        elif ".html" in file_path:
            content_type = "text/html"
        else:
            content_type = "text/plain"
        
        # load header into buffers
        header = (
            f"HTTP/1.0 {status_code}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {size}\r\n"
            f"Connection: close\r\n"
        )

        if use_gzip:
            header += "Content-Encoding: gzip\r\n"

        header += "\r\n"

        writer.write(header.encode())
        await writer.drain()

        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                writer.write(chunk)
                await writer.drain()

        await writer.drain()
        await asyncio.sleep(0.01)
        await writer.wait_closed()
    
    except OSError:
        await respond_text(writer, "404 Not Found", 404)


