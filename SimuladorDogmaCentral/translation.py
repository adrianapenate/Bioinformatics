# Simula la traducción del ARN mensajero a una proteína

from validation import validate_rna
from models import (
    MessengerRNA,
    AminoAcid,
    Protein,
    TransferRNA,
    Ribosome
)

GENETIC_CODE = {
    # None son codones de parada
    "UUU": ("Fenilalanina", "Phe"),
    "UUC": ("Fenilalanina", "Phe"),
    "UUA": ("Leucina", "Leu"),
    "UUG": ("Leucina", "Leu"),

    "UCU": ("Serina", "Ser"),
    "UCC": ("Serina", "Ser"),
    "UCA": ("Serina", "Ser"),
    "UCG": ("Serina", "Ser"),

    "UAU": ("Tirosina", "Tyr"),
    "UAC": ("Tirosina", "Tyr"),
    "UAA": None,
    "UAG": None,

    "UGU": ("Cisteína", "Cys"),
    "UGC": ("Cisteína", "Cys"),
    "UGA": None,
    "UGG": ("Triptófano", "Trp"),

    "CUU": ("Leucina", "Leu"),
    "CUC": ("Leucina", "Leu"),
    "CUA": ("Leucina", "Leu"),
    "CUG": ("Leucina", "Leu"),

    "CCU": ("Prolina", "Pro"),
    "CCC": ("Prolina", "Pro"),
    "CCA": ("Prolina", "Pro"),
    "CCG": ("Prolina", "Pro"),

    "CAU": ("Histidina", "His"),
    "CAC": ("Histidina", "His"),
    "CAA": ("Glutamina", "Gln"),
    "CAG": ("Glutamina", "Gln"),

    "CGU": ("Arginina", "Arg"),
    "CGC": ("Arginina", "Arg"),
    "CGA": ("Arginina", "Arg"),
    "CGG": ("Arginina", "Arg"),

    "AUU": ("Isoleucina", "Ile"),
    "AUC": ("Isoleucina", "Ile"),
    "AUA": ("Isoleucina", "Ile"),
    "AUG": ("Metionina", "Met"),

    "ACU": ("Treonina", "Thr"),
    "ACC": ("Treonina", "Thr"),
    "ACA": ("Treonina", "Thr"),
    "ACG": ("Treonina", "Thr"),

    "AAU": ("Asparagina", "Asn"),
    "AAC": ("Asparagina", "Asn"),
    "AAA": ("Lisina", "Lys"),
    "AAG": ("Lisina", "Lys"),

    "AGU": ("Serina", "Ser"),
    "AGC": ("Serina", "Ser"),
    "AGA": ("Arginina", "Arg"),
    "AGG": ("Arginina", "Arg"),

    "GUU": ("Valina", "Val"),
    "GUC": ("Valina", "Val"),
    "GUA": ("Valina", "Val"),
    "GUG": ("Valina", "Val"),

    "GCU": ("Alanina", "Ala"),
    "GCC": ("Alanina", "Ala"),
    "GCA": ("Alanina", "Ala"),
    "GCG": ("Alanina", "Ala"),

    "GAU": ("Ácido aspártico", "Asp"),
    "GAC": ("Ácido aspártico", "Asp"),
    "GAA": ("Ácido glutámico", "Glu"),
    "GAG": ("Ácido glutámico", "Glu"),

    "GGU": ("Glicina", "Gly"),
    "GGC": ("Glicina", "Gly"),
    "GGA": ("Glicina", "Gly"),
    "GGG": ("Glicina", "Gly")
}

START_CODON = "AUG"

STOP_CODONS = {
    "UAA",
    "UAG",
    "UGA"
}


RNA_COMPLEMENT = {
    "A": "U",
    "U": "A",
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


def get_anticodon(codon: str) -> str:
    # Obtiene el anticodón complementario de un codón de ARNm
    codon = validate_rna(codon)
    if len(codon) != 3:
        raise ValueError(
            "Un codón debe contener exactamente "
            "tres nucleótidos."
        )

    return "".join(
        RNA_COMPLEMENT[base]
        for base in codon
    )


def get_amino_acid(codon: str) -> AminoAcid:
    # Obtiene el aminoácido correspondiente a un codón
    codon = validate_rna(codon)
    if codon not in GENETIC_CODE:
        raise ValueError(
            f"El codón '{codon}' no es válido."
        )

    amino_acid_data = GENETIC_CODE[codon]

    if amino_acid_data is None:
        raise ValueError(
            f"El codón {codon} es un codón STOP "
            "y no codifica ningún aminoácido."
        )

    name, abbreviation = amino_acid_data

    return AminoAcid(
        name=name,
        abbreviation=abbreviation
    )


def create_transfer_rna(codon: str) -> TransferRNA:
    # Crea el ARNt correspondiente a un codón.
    codon = validate_rna(codon)
    if codon in STOP_CODONS:
        raise ValueError(
            "Los codones STOP no son reconocidos "
            "por ARNt, sino por factores de liberación."
        )

    anticodon = get_anticodon(codon)

    amino_acid = get_amino_acid(codon)

    return TransferRNA(
        anticodon_3_5=anticodon,
        amino_acid=amino_acid
    )


def translate(mrna: MessengerRNA) -> dict:
    # Traduce desde el primer AUG hasta STOP o hasta agotar los codones completos

    if not isinstance(mrna, MessengerRNA):
        raise TypeError("translate() necesita un objeto MessengerRNA.")

    protein = Protein()
    ribosome = Ribosome()
    start = mrna.find_start_codon()
    events = []
    steps = []
    result = {
        "mrna": mrna,
        "start_position": start,
        "codons": [],  # Solo codones realmente procesados, incluido STOP
        "protein": protein,
        "translation_steps": steps,
        "stop_codon": None,
        "completed": False,
        "status": "no_start",
        "untranslated_prefix": mrna.sequence if start == -1 else mrna.sequence[:start],
        "untranslated_after_stop": "",
        "incomplete_codon": "",
        "events": events,
    }
    if start == -1:
        events.append("No se encontró AUG: la traducción no comienza.")
        return result

    events.append(f"AUG encontrado en la posición {start + 1}; establece el marco de lectura.")
    result["status"] = "no_stop"
    for number, codon in enumerate(ribosome.read(mrna, start), start=1):
        result["codons"].append(codon)
        if codon in STOP_CODONS:
            # El STOP lo reconoce un factor de liberación, nunca un ARNt
            events.append(f"STOP {codon}: un factor de liberación libera la cadena.")
            ribosome.site_a = ribosome.site_p = ribosome.site_e = None
            result["stop_codon"] = codon
            result["completed"] = True
            result["status"] = "completed"
            result["untranslated_after_stop"] = mrna.sequence[start + number * 3:]
            steps.append({
                "codon_number": number, "codon": codon, "type": "STOP",
                "anticodon": None, "amino_acid": None,
                "protein_sequence": protein.sequence(), "ribosome_states": [],
            })
            break

        trna = create_transfer_rna(codon)
        states = []
        if number == 1:
            # El iniciador entra directamente en P; aún no hay enlace peptídico
            ribosome.site_p = trna
            protein.add_amino_acid(trna.amino_acid)
            events.append("Iniciación: el ARNt iniciador se sitúa en P.")
            states.append({"stage": "Iniciación", "sites": ribosome.snapshot()})
        else:
            ribosome.site_a = trna
            states.append({"stage": "Entrada en A", "sites": ribosome.snapshot()})
            events.append(f"Codón {number}: entra el ARNt en A.")
            protein.add_amino_acid(trna.amino_acid)
            events.append("Enlace peptídico: la cadena pasa del ARNt de P al de A.")
            # Tras la translocación, el ARNt con la cadena queda en P
            ribosome.site_e = ribosome.site_p
            ribosome.site_p = ribosome.site_a
            ribosome.site_a = None
            states.append({"stage": "Translocación", "sites": ribosome.snapshot()})
            events.append("Translocación: A -> P, P -> E; el ARNt descargado sale por E.")
            ribosome.site_e = None
            states.append({"stage": "Salida por E", "sites": ribosome.snapshot()})

        steps.append({
            "codon_number": number, "codon": codon, "type": "amino_acid",
            "anticodon": trna.anticodon_3_5,
            "amino_acid": {"name": trna.amino_acid.name,
                           "abbreviation": trna.amino_acid.abbreviation},
            "protein_sequence": protein.sequence(), "ribosome_states": states,
        })

    if not result["completed"]:
        events.append("Final del ARNm sin STOP: cadena parcial, sin terminación normal.")
        tail = mrna.sequence[start + len(result["codons"]) * 3:]
        result["incomplete_codon"] = tail
        if tail:
            events.append(f"Quedan {len(tail)} bases ({tail}) que no forman un codón completo.")
    elif result["untranslated_after_stop"]:
        events.append("Región posterior a STOP sin traducir: " + result["untranslated_after_stop"])
    return result
