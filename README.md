# Del ADN a la Proteína

**Autora:** Adriana Peñate Sosa

## Descripción

Este trabajo tiene como objetivo estudiar los principales procesos relacionados con el flujo de la información genética desde el ADN hasta la proteína.

A lo largo de los ejercicios se trabajan los procesos de replicación, transcripción y traducción, además del splicing alternativo y la relación entre la secuencia de aminoácidos, la estructura y la función de las proteínas.

La parte práctica se ha realizado utilizando Python y Biopython.

## Contenido de la entrega

La entrega está formada por los siguientes archivos:

- `Del ADN a la Proteína - Adriana Peñate.pdf`
  Contiene la resolución de los ejercicios, las explicaciones teóricas y las reflexiones correspondientes.

- `ADNaProteína.ipynb`
  Notebook de Jupyter que contiene los ejercicios realizados con Biopython y el pipeline final de replicación, transcripción y traducción.

- `lacZ_Ecoli_NC_000913.3.fasta`
  Archivo FASTA que contiene la secuencia de ADN utilizada en los ejercicios prácticos.

- `README.md`
  Documento con la descripción del trabajo y las instrucciones necesarias para ejecutar el notebook.

## Secuencia utilizada

Para los ejercicios prácticos se utiliza una secuencia del gen `lacZ` de Escherichia coli, correspondiente al identificador `NC_000913.3`.

La secuencia utilizada contiene 3075 nucleótidos y se encuentra almacenada en el archivo:

`lacZ_Ecoli_NC_000913.3.fasta`

## Ejercicios realizados

1. Replicación del ADN.
2. Transcripción del ADN a ARN.
3. Traducción del ARNm a proteína.
4. Splicing alternativo.
5. Introducción a las proteínas y análisis de su estructura.
6. Actividad integradora: del ADN a la proteína.

En el último ejercicio se implementa un pipeline que integra los tres procesos principales:

ADN → Replicación → Transcripción → Traducción → Proteína

El programa informa de cada una de las etapas y muestra las secuencias obtenidas durante el proceso.

## Requisitos

Para ejecutar el notebook es necesario disponer de:

- Python
- Jupyter Notebook
- Biopython

Biopython puede instalarse mediante:

    pip install biopython

## Ejecución

1. Descargar todos los archivos de la entrega.
2. Mantener `ADNaProteína.ipynb` y `lacZ_Ecoli_NC_000913.3.fasta` en la misma carpeta.
3. Abrir `ADNaProteína.ipynb` con Jupyter Notebook.
4. Ejecutar las celdas del notebook en orden.

El notebook leerá automáticamente la secuencia almacenada en el archivo FASTA y realizará los diferentes ejercicios.

## Recursos utilizados

- NCBI: secuencia de ADN de Escherichia coli.
- Ensembl: consulta de transcritos e isoformas de FGFR2.
- Protein Data Bank (PDB): visualización de la estructura 1CRN (crambin).
- Biopython: tratamiento y análisis de secuencias biológicas.