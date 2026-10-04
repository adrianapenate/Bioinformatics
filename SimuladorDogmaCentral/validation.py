# Se valida el tipo de dato para poder trabajar con ello, sin comprobar si las letras son válidas

def _validate_sequence(sequence: str, alphabet: str, name: str) -> str:
    if not isinstance(sequence, str):
        raise TypeError(f"La secuencia de {name} debe ser texto.")
    sequence = "".join(sequence.upper().split())
    if not sequence:
        raise ValueError(f"La secuencia de {name} no puede estar vacía.")
    invalid = set(sequence) - set(alphabet)
    if invalid:
        raise ValueError(f"Bases no válidas para {name}: {', '.join(sorted(invalid))}.")
    return sequence

def validate_dna(sequence: str) -> str:
    return _validate_sequence(sequence, "ATCG", "ADN")

def validate_rna(sequence: str) -> str:
    return _validate_sequence(sequence, "AUCG", "ARN")