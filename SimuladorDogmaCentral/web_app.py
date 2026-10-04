# Interfaz web local. Ejecutar con: python web_app.py
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser

from models import DNA
from replication import replicate
from transcription import transcribe
from translation import translate

WEB_DIR = Path(__file__).resolve().parent / 'web'
MAX_BASES = 600


def simulate(sequence: str, fragment_size: int = 5) -> dict:
    # Adapta los objetos Python a datos que el navegador puede leer como JSON
    dna = DNA(sequence)
    if dna.length() > MAX_BASES:
        raise ValueError(f'Utiliza como máximo {MAX_BASES} bases para la vista didáctica.')
    replication = replicate(dna, fragment_size)
    transcription = transcribe(replication['molecule_1'])
    translation = translate(transcription['mrna'])
    return {
        'dna': {'coding': dna.strand_5_3, 'template': dna.strand_3_5},
        'replication': {key: value for key, value in replication.items()
                        if key != 'original_dna'},
        'transcription': {key: value for key, value in transcription.items()
                          if key not in {'mrna', 'dna_molecule'}},
        'translation': {**{key: value for key, value in translation.items()
                           if key not in {'mrna', 'protein'}},
                        'protein': translation['protein'].sequence(),
                        'protein_length': translation['protein'].length()},
    }


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, data, content_type='application/json; charset=utf-8'):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8') if isinstance(data, dict) else data
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # Solo se sirven estos archivos; no se expone el código ni otras carpetas
        routes = {'/': ('index.html', 'text/html'),
                  '/style.css': ('style.css', 'text/css'),
                  '/app.js': ('app.js', 'text/javascript')}
        route = routes.get(self.path.split('?')[0])
        if route is None:
            self.respond(404, {'error': 'Página no encontrada.'})
            return
        name, content_type = route
        self.respond(200, (WEB_DIR / name).read_bytes(), content_type + '; charset=utf-8')

    def do_POST(self):
        if self.path != '/api/simulate':
            self.respond(404, {'error': 'Ruta no encontrada.'})
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 10000:
                raise ValueError('La entrada está vacía o es demasiado grande.')
            body = self.rfile.read(length)
            # Consumimos la petición antes de responder para cerrar correctamente
            # la conexión también en Windows cuando se rechaza el origen
            origin = self.headers.get('Origin')
            port = self.server.server_address[1]
            if origin and origin not in {f'http://127.0.0.1:{port}', f'http://localhost:{port}'}:
                self.respond(403, {'error': 'Origen no permitido.'})
                return
            payload = json.loads(body)
            if not isinstance(payload, dict):
                raise ValueError('Se esperaba una secuencia de ADN.')
            result = simulate(payload.get('sequence'), payload.get('fragment_size', 5))
        except (ValueError, TypeError, UnicodeDecodeError) as error:
            self.respond(400, {'error': str(error)})
            return
        self.respond(200, result)


def main():
    parser = argparse.ArgumentParser(description='Simulador web local del dogma central')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    except OSError as error:
        parser.exit(1, f'No se puede abrir el puerto {args.port}: {error}\nPrueba --port 8001.\n')
    url = f'http://127.0.0.1:{server.server_address[1]}'
    print(f'Abre {url} en el navegador. Para terminar, pulsa Ctrl+C.', flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
