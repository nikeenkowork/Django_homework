from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse


class Handler(BaseHTTPRequestHandler):
    """
    HTTP обработчик для простого веб-сайта.

    Поддерживает:
    - GET: отдаёт HTML страницы (home, categories, orders, contacts)
    - POST: принимает данные формы с страницы контактов
    """

    def do_GET(self):
        """
        Обрабатывает GET-запросы.

        Возвращает HTML-страницы в зависимости от пути:
        - / или /home → home.html
        - /categories → categories.html
        - /orders → orders.html
        - /contacts → contacts.html
        """

        # Определяем, какой файл нужно отдать
        if self.path in ["/", "/home"]:
            file_path = "home.html"

        elif self.path == "/categories":
            file_path = "categories.html"

        elif self.path == "/orders":
            file_path = "orders.html"

        elif self.path == "/contacts":
            file_path = "contacts.html"

        elif self.path == "/styles.css":
            with open("styles.css", "rb") as f:
                self.send_response(200)
                self.send_header("Content-Type", "text/css")
                self.end_headers()
                self.wfile.write(f.read())
            return

        else:
            # Если маршрут не найден → 404 ошибка
            self.send_error(404, "Page not found")


            return

        # Читаем HTML файл
        with open(file_path, "r", encoding="utf-8") as file:
            html = file.read()

        # Отправляем ответ клиенту
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # Отдаём HTML страницу браузеру
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        """
        Обрабатывает POST-запросы.

        Используется на странице /contacts для получения:
        - name (имя пользователя)
        - email (почта)
        - message (сообщение)

        Данные приходят в формате form-data (urlencoded).
        """

        # Проверяем, что запрос именно с формы контактов
        if self.path == "/contacts":

            # Получаем длину тела запроса
            content_length = int(self.headers.get("Content-Length", 0))

            # Читаем "сырые" данные из запроса
            post_data = self.rfile.read(content_length)

            # Декодируем и парсим form-data
            data = urllib.parse.parse_qs(post_data.decode("utf-8"))

            # Извлекаем поля формы
            name = data.get("name", [""])[0]
            email = data.get("email", [""])[0]
            message = data.get("message", [""])[0]

            # Логируем данные на сервере (для проверки)
            print("📩 Получено новое сообщение:")
            print("Имя:", name)
            print("Email:", email)
            print("Сообщение:", message)

            # Возвращаем пользователю ту же страницу
            with open("contacts.html", "r", encoding="utf-8") as file:
                html = file.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        else:
            # Если путь не поддерживается
            self.send_error(404, "Page not found")



# Создаём и запускаем сервер
server = HTTPServer(("localhost", 8000), Handler)

print("🚀 Сервер запущен: http://localhost:8000")
server.serve_forever()
