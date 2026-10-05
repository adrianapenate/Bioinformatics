# Simula la transcripción de ADN a ARN mensajero (ARNm)

# strand_3_5 actúa como cadena molde;
# strand_5_3 actúa como cadena codificante;
# la ARN polimerasa lee el molde en dirección 3' -> 5';
# el ARNm se sintetiza en dirección 5' -> 3'

from models import DNA, MessengerRNA
from validation import validate_dna
from enzymes import get_enzyme_description

DNA_TO_RNA_COMPLEMENT = {
    "A": "U",
    "T": "A",
    "C": "G",
    "G": "C"
}

# Funciones auxiliares
def _add_event(
    events: list[str],
    stage: str,
    message: str
):
    events.append(
        f"[{stage}] {message}"
    )

def _transcribe_template(template_3_5: str) -> str:
    # Genera una secuencia de ARN complementaria a una cadena molde de ADN escrita en dirección 3' -> 5'.
    # La nueva molécula de ARN queda escrita en dirección 5' -> 3'.

    return "".join(
        DNA_TO_RNA_COMPLEMENT[base]
        for base in template_3_5
    )


def transcribe(dna_molecule: dict) -> dict:
    # Simulación de la transcripción
    if not isinstance(dna_molecule, dict):
        raise TypeError(
            "transcribe() necesita una molécula de ADN "
            "representada mediante un diccionario."
        )

    required_keys = {
        "strand_5_3",
        "strand_3_5"
    }

    if not required_keys.issubset(dna_molecule.keys()):
        raise ValueError(
            "La molécula de ADN no contiene las dos "
            "cadenas necesarias para la transcripción."
        )

    try:
        coding_strand_5_3 = (
            dna_molecule["strand_5_3"]["sequence"]
        )

        template_strand_3_5 = (
            dna_molecule["strand_3_5"]["sequence"]
        )

    except (KeyError, TypeError):
        raise ValueError(
            "La estructura de la molécula de ADN "
            "no es válida."
        )

    coding_strand_5_3 = validate_dna(coding_strand_5_3)
    template_strand_3_5 = validate_dna(template_strand_3_5)
    if DNA(coding_strand_5_3).strand_3_5 != template_strand_3_5:
        raise ValueError("Las hebras de ADN deben ser complementarias y de igual longitud.")

    events = []

    # PASO 1 - SELECCIÓN HEBRA MOLDE
    _add_event(
        events,
        "transcription",
        (
            "Se selecciona la cadena de ADN orientada "
            "3' -> 5' como cadena molde."
        )
    )

    _add_event(
        events,
        "transcription",
        (
            "La cadena orientada 5' -> 3' queda definida "
            "como cadena codificante."
        )
    )

    # PASO 2 - UNIÓN ARN POLIMERASA
    _add_event(
        events,
        "rna_polymerase",
        (
            "La ARN polimerasa se une a la región de inicio "
            "y abre localmente la doble cadena de ADN."
        )
    )

    # PASO 3 - LECTURA MOLDE
    _add_event(
        events,
        "rna_polymerase",
        (
            "La ARN polimerasa comienza a leer la cadena "
            "molde en dirección 3' -> 5'."
        )
    )

    # PASO 4 - ELONGACIÓN ARN
    mrna_sequence = ""

    nucleotide_events = []

    for position, dna_base in enumerate(
        template_strand_3_5,
        start=1
    ):
        rna_base = DNA_TO_RNA_COMPLEMENT[dna_base]

        mrna_sequence += rna_base

        nucleotide_event = (
            f"Posición {position}: "
            f"ADN molde {dna_base} -> ARN {rna_base}"
        )

        nucleotide_events.append(nucleotide_event)

    _add_event(
        events,
        "rna_polymerase",
        (
            "La ARN polimerasa sintetiza el ARNm "
            "complementario en dirección 5' -> 3'."
        )
    )

    # CREAMOS OBJETO ARNm
    mrna = MessengerRNA(
        mrna_sequence
    )

    # PASO 5 - TERMINACIÓN
    _add_event(
        events,
        "transcription",
        (
            "La transcripción finaliza y se libera "
            "la molécula de ARNm."
        )
    )

    # COMPROBAMOS CONSISTENCIA
    # La cadena codificante debe tener la misma secuencia
    # que el ARNm, sustituyendo T por U.
    expected_mrna = coding_strand_5_3.replace(
        "T",
        "U"
    )

    sequences_match = (
        expected_mrna == mrna_sequence
    )

    if sequences_match:
        _add_event(
            events,
            "transcription",
            (
                "Comprobación correcta: el ARNm coincide "
                "con la cadena codificante sustituyendo "
                "timina (T) por uracilo (U)."
            )
        )
    else:
        _add_event(
            events,
            "warning",
            (
                "El ARNm generado no coincide con la "
                "cadena codificante esperada."
            )
        )

    # RESULTADO
    return {
        "dna_molecule": dna_molecule,

        "coding_strand": {
            "sequence": coding_strand_5_3,
            "orientation": "5' -> 3'"
        },

        "template_strand": {
            "sequence": template_strand_3_5,
            "orientation": "3' -> 5'"
        },

        "mrna": mrna,

        "mrna_sequence": mrna_sequence,

        "nucleotide_events": nucleotide_events,

        "sequences_match": sequences_match,

        "events": events
    }

# Información adicional
def get_transcription_enzyme() -> dict:
    return {
        "rna_polymerase":
            get_enzyme_description("rna_polymerase")
    }