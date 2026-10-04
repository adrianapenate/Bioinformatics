# Simulador del dogma central

Práctica de Bioinformática desarrollada en Python. Simula la replicación del ADN, la transcripción a ARN mensajero y la traducción a una cadena de aminoácidos.

Puede utilizarse desde la terminal o mediante una interfaz web local.

## Requisitos

- Python 3.9 o superior.
- Un navegador para utilizar la interfaz web.

No es necesario instalar librerías externas.

## Ejecución

Descarga o clona el repositorio y abre una terminal en la carpeta donde están `main.py` y `web_app.py`.

### Interfaz web

```bash
python web_app.py
```

Se abrirá el navegador en [http://127.0.0.1:8000](http://127.0.0.1:8000). Introduce una secuencia de ADN y pulsa **Simular** para ver los resultados.

Mantén la terminal abierta mientras utilizas la web. Para detener el servidor, pulsa `Ctrl+C`. Si el puerto está ocupado, utiliza `python web_app.py --port 8001`.

### Terminal

```bash
python main.py
```

Selecciona la opción `1` e introduce una secuencia de ADN. Pulsa ENTER sin escribir nada para utilizar el ejemplo. La opción `2` cierra el programa.

En Windows, si `python` no se reconoce, prueba con `py` en su lugar.

## Funcionamiento

1. **Replicación:** genera dos moléculas de ADN y representa la hebra líder, la rezagada y los fragmentos de Okazaki.
2. **Transcripción:** utiliza una hebra molde para obtener un ARNm complementario.
3. **Traducción:** lee codones desde el primer AUG y obtiene los aminoácidos hasta encontrar STOP. Si no hay AUG o STOP, informa de ello.

La entrada admite A, T, C y G, con espacios o minúsculas. La interfaz web acepta hasta 600 bases.

## Ejemplo

```text
ADN:      ATGCCATGGAATGCTTAA
ARNm:     AUGCCAUGGAAUGCUUAA
Proteína: Met-Pro-Trp-Asn-Ala
STOP:     UAA
```

## Archivos principales

| Archivo | Función |
| --- | --- |
| `main.py` | Ejecuta el simulador en la terminal. |
| `web_app.py` | Conecta la interfaz web con Python. |
| `models.py` | Representa las moléculas y el ribosoma. |
| `validation.py` | Valida las secuencias. |
| `replication.py` | Simula la replicación del ADN. |
| `transcription.py` | Genera el ARN mensajero. |
| `translation.py` | Obtiene la cadena de aminoácidos. |
| `enzymes.py` | Contiene descripciones de las enzimas. |
| `output.py` | Muestra los resultados en la terminal. |
| `web/` | Contiene el HTML, CSS y JavaScript de la web. |

## Simplificaciones

Es un modelo didáctico procariota: utiliza una sola horquilla y fragmentos de Okazaki de cinco bases. Se transcribe toda la hebra molde y se traduce desde el primer AUG. Las acciones de las enzimas y los cebadores se describen de forma simplificada.
