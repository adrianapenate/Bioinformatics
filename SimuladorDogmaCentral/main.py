# Punto de entrada principal del simulador del dogma central de la biología molecular.
from models import DNA
from validation import validate_dna
from replication import replicate
from transcription import transcribe
from translation import translate


from output import (
    print_title,
    show_initial_dna,
    show_replication_result,
    show_transcription_result,
    show_translation_result,
    show_final_summary
)

DEFAULT_SEQUENCE = "ATGCCATGGAATGCTTAA"

# Input
def request_dna_sequence() -> str:
    print()
    print("Introduce una secuencia de ADN.")
    print()
    print("Solo se permiten las bases:")
    print("A, T, C y G")
    print()

    print(
        "Puedes pulsar ENTER sin escribir nada "
        "para utilizar la secuencia de demostración:"
    )

    print()
    print(
        f"5' - {DEFAULT_SEQUENCE} - 3'"
    )
    print()

    while True:

        sequence = input(
            "Secuencia de ADN 5' -> 3': "
        ).strip()

        # Si el usuario pulsa ENTER, utilizamos nuestra secuencia de prueba
        if sequence == "":
            sequence = DEFAULT_SEQUENCE

            print()
            print(
                "Se utilizará la secuencia "
                "de demostración."
            )

        try:
            return validate_dna(sequence)

        except (ValueError, TypeError) as error:

            print()
            print(
                f"ERROR: {error}"
            )

            print()
            print(
                "Inténtalo de nuevo."
            )
            print()


def run_complete_simulation(
    sequence: str
):
    # Ejecuta el flujo completo del dogma central.

    # Creamos ADN
    dna = DNA(
        sequence
    )

    show_initial_dna(
        dna
    )

    # Replicación
    replication_result = replicate(
        dna
    )

    show_replication_result(
        replication_result
    )

    # Seleccionamos molécula de ADN
    dna_for_transcription = (
        replication_result["molecule_1"]
    )

    # Transcripción
    transcription_result = transcribe(
        dna_for_transcription
    )

    show_transcription_result(
        transcription_result
    )

    # Traducción
    mrna = transcription_result[
        "mrna"
    ]

    translation_result = translate(
        mrna
    )

    show_translation_result(
        translation_result
    )

    # Sumario
    show_final_summary(
        dna,
        transcription_result,
        translation_result
    )


def show_menu():
    # Menú principal
    print()
    print("1. Ejecutar simulación completa")
    print("2. Salir")
    print()


def main():
    # Función principal del programa
    print_title(
        "SIMULADOR DEL DOGMA CENTRAL"
    )

    print(
        "Este programa simula el flujo de "
        "información genética:"
    )

    print()

    print(
        "ADN -> ADN -> ARNm -> proteína"
    )

    while True:

        show_menu()

        option = input(
            "Selecciona una opción: "
        ).strip()

        if option == "1":

            sequence = request_dna_sequence()

            print_title(
                "INICIO DE LA SIMULACIÓN"
            )

            run_complete_simulation(
                sequence
            )

            print()
            print(
                "Simulación completada."
            )

        elif option == "2":

            print()
            print(
                "Simulador finalizado."
            )

            break

        else:

            print()
            print(
                "Opción no válida."
            )

            print(
                "Selecciona 1 o 2."
            )


if __name__ == "__main__":
    main()