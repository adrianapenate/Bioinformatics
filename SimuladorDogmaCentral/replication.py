# Simula la replicación

from models import DNA
from enzymes import get_enzyme_description

# Los fragmentos reales son mucho mayores.
# Utilizamos un tamaño pequeño para que puedan observarse
# fácilmente durante la simulación.
OKAZAKI_FRAGMENT_SIZE = 5

# Funciones auxiliares
def _complement(sequence: str) -> str:
    # Devuelve la secuencia complementaria de ADN.
    complement_map = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }

    return "".join(
        complement_map[base]
        for base in sequence
    )

def _add_event(
    events: list[str],
    enzyme: str,
    message: str
):
    # Registro de explicaciones del proceso
    events.append(
        f"[{enzyme}] {message}"
    )

def _create_okazaki_fragments(template_5_3: str, fragment_size: int) -> list[dict]:
    # Orden de aparición: izquierda a derecha; síntesis local: derecha a izquierda
    fragments = []
    for start in range(0, len(template_5_3), fragment_size):
        end = min(start + fragment_size, len(template_5_3))
        segment = template_5_3[start:end]
        # Cada molde se lee 3' -> 5' para sintetizar ADN 5' -> 3'.
        template_read = segment[::-1]
        fragments.append({
            "number": len(fragments) + 1,
            "template_start": start + 1,
            "template_end": end,
            "template_segment_5_3": segment,
            "template_read_3_5": template_read,
            "sequence_5_3": _complement(template_read),
            "primer": "RNA primer",
        })
    return fragments


def replicate(
    dna: DNA,
    okazaki_fragment_size: int = OKAZAKI_FRAGMENT_SIZE
) -> dict:
    # Simulación de la replicación 
    if not isinstance(dna, DNA):
        raise TypeError(
            "replicate() necesita un objeto DNA."
        )

    if type(okazaki_fragment_size) is not int:
        raise TypeError("El tamaño de los fragmentos debe ser un entero.")
    if okazaki_fragment_size <= 0:
        raise ValueError(
            "El tamaño de los fragmentos de Okazaki "
            "debe ser mayor que cero."
        )

    events = []

    # PASO 1 - TOPOISOMERASA
    _add_event(
        events,
        "topoisomerase",
        (
            "La topoisomerasa actúa por delante de la "
            "horquilla y reduce la tensión generada "
            "durante la apertura del ADN."
        )
    )

    # PASO 2 - HELICASA
    _add_event(
        events,
        "helicase",
        (
            "La helicasa comienza a separar las dos "
            "cadenas de ADN y genera la horquilla "
            "de replicación."
        )
    )

    # PASO 3 - SSB PROTEINAS
    _add_event(
        events,
        "ssb",
        (
            "Las proteínas SSB se unen a las cadenas "
            "separadas y evitan que vuelvan a aparearse."
        )
    )

    # Identificar hebras molde

    # Nuestra horquilla avanza de izquierda a derecha.
    # Cadena inferior:
    # 3' ---------------------------- 5'
    # Puede ser leída por la polimerasa 3' -> 5'
    # mientras la horquilla avanza.
    # Por tanto es el molde de la cadena líder.

    leading_template_3_5 = dna.strand_3_5

    # Cadena superior:
    # 5' ---------------------------- 3'
    # Tiene la orientación contraria respecto al avance
    # de la horquilla.
    # Por tanto se replica mediante fragmentos de Okazaki.

    lagging_template_5_3 = dna.strand_5_3

    # PASO 4 - PRIMASE
    _add_event(
        events,
        "primase",
        (
            "La primasa sintetiza un cebador de ARN "
            "para iniciar la cadena líder."
        )
    )

    # PASO 5 - CADENA LÍDER
    # La nueva cadena líder se sintetiza continuamente
    # en dirección 5' -> 3'.
    leading_new_strand_5_3 = _complement(
        leading_template_3_5
    )

    _add_event(
        events,
        "dna_polymerase_iii",
        (
            "La ADN polimerasa III sintetiza la cadena "
            "líder de forma continua en dirección 5' -> 3'."
        )
    )

    leading_strand = {
        "template": leading_template_3_5,
        "template_orientation": "3' -> 5'",
        "new_strand": leading_new_strand_5_3,
        "new_strand_orientation": "5' -> 3'",
        "synthesis": "continuous",
        "primer_count": 1
    }

    # PASO 6 - HEBRA REZAGADA
    okazaki_fragments = _create_okazaki_fragments(
        lagging_template_5_3,
        okazaki_fragment_size
    )

    for fragment in okazaki_fragments:

        _add_event(
            events,
            "primase",
            (
                "La primasa coloca un cebador para el "
                f"fragmento de Okazaki {fragment['number']}."
            )
        )

        _add_event(
            events,
            "dna_polymerase_iii",
            (
                "La ADN polimerasa III sintetiza el "
                f"fragmento de Okazaki "
                f"{fragment['number']} en dirección 5' -> 3'."
            )
        )

    # Una vez finalizado todo el proceso, la cadena nueva
    # complementaria queda alineada respecto a la original
    # en orientación 3' -> 5'.
    # Los fragmentos están guardados 5' -> 3'. Los invertimos para
    # alinearlos bajo el molde y los unimos en orden de posición.
    lagging_new_strand_3_5 = "".join(
        fragment["sequence_5_3"][::-1] for fragment in okazaki_fragments
    )
    if lagging_new_strand_3_5 != _complement(lagging_template_5_3):
        raise ValueError("Los fragmentos no reconstruyen la cadena rezagada.")

    lagging_strand = {
        "template": lagging_template_5_3,
        "template_orientation": "5' -> 3'",
        "new_strand": lagging_new_strand_3_5,
        "new_strand_orientation": "3' -> 5'",
        "synthesis": "discontinuous",
        "primer_count": len(okazaki_fragments),
        "okazaki_fragments": okazaki_fragments
    }

    # PASO 7 - ADN POLIMERASA I
    _add_event(
        events,
        "dna_polymerase_i",
        (
            "La ADN polimerasa I elimina los cebadores "
            "de ARN y reemplaza esas regiones por ADN."
        )
    )

    # PASO 8 - ADN LIGASA
    _add_event(
        events,
        "dna_ligase",
        (
            "La ADN ligasa sella las discontinuidades "
            "entre los fragmentos de Okazaki."
        )
    )

    # PASO 9 - REPLICACIÓN SEMICONSERVADORA
    # MOLÉCULA 1
    # Conserva como original la cadena superior.
    # 5' original ---------------- 3'
    # 3' nueva    ---------------- 5'

    molecule_1 = {
        "name": "DNA molecule 1",

        "strand_5_3": {
            "sequence": dna.strand_5_3,
            "origin": "original"
        },

        "strand_3_5": {
            "sequence": lagging_new_strand_3_5,
            "origin": "new"
        }
    }

    # MOLÉCULA 2
    # Conserva como original la cadena inferior.
    # 5' nueva    ---------------- 3'
    # 3' original ---------------- 5'

    molecule_2 = {
        "name": "DNA molecule 2",

        "strand_5_3": {
            "sequence": leading_new_strand_5_3,
            "origin": "new"
        },

        "strand_3_5": {
            "sequence": dna.strand_3_5,
            "origin": "original"
        }
    }

    events.append(
        (
            "[replication] La replicación ha finalizado. "
            "Se han obtenido dos moléculas de ADN, "
            "cada una formada por una cadena original "
            "y una cadena recién sintetizada."
        )
    )

    # RESULTADO
    return {
        "original_dna": dna,

        "replication_fork_direction": "left -> right",

        "leading_strand": leading_strand,

        "lagging_strand": lagging_strand,

        "molecule_1": molecule_1,

        "molecule_2": molecule_2,

        "events": events
    }


# Infromación adicional 
def get_replication_enzymes() -> dict:
    # Devuelve las enzimas y factores utilizados durante la replicación junto con su función.
    enzyme_names = [
        "topoisomerase",
        "helicase",
        "ssb",
        "primase",
        "dna_polymerase_iii",
        "dna_polymerase_i",
        "dna_ligase"
    ]

    return {
        enzyme: get_enzyme_description(enzyme)
        for enzyme in enzyme_names
    }