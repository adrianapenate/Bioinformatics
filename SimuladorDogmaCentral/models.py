from validation import validate_dna, validate_rna

class DNA:
    DNA_COMPLEMENT = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }

    def __init__(self, strand_5_3: str):
        # A partir de la secuencia 5 -> 3, crea el ADN, su cadena 3 -> 5
        self.strand_5_3 = validate_dna(strand_5_3)
        self.strand_3_5 = self._complementary_strand(self.strand_5_3)

    def _complementary_strand(self, strand: str) -> str:
        # Genera la cadena complementaria
        return "".join(
            self.DNA_COMPLEMENT[base]
            for base in strand
        )

    def length(self) -> int:
        # Devuelve longitud del ADN, pares de bases
        return len(self.strand_5_3)

    def display(self) -> str:
        # Representación 
        bonds = "|" * self.length()

        return (
            f"5' - {self.strand_5_3} - 3'\n"
            f"     {bonds}\n"
            f"3' - {self.strand_3_5} - 5'"
        )

    def __str__(self) -> str:
        return self.display()


class MessengerRNA:
    # ARNm guardado siempre 5 -> 3
    def __init__(self, sequence: str):
        self.sequence = validate_rna(sequence)

    def find_start_codon(self) -> int:
        # Busca codón de inicio AUG, devuelve -1 si no lo encuentra, o opsición donde empieza
        return self.sequence.find("AUG")

    def get_codons(self, start: int = 0) -> list[str]:
        # Devuelve lista de codones desde codón de incio (start, dado por otra clase), los separa cada 3
        if type(start) is not int:
            raise TypeError("La posición inicial debe ser un entero.")
        if start < 0:
            raise ValueError(
                "La posición inicial no puede ser negativa."
            )
        codons = []
        for i in range(start, len(self.sequence) - 2, 3):
            codon = self.sequence[i:i + 3]
            codons.append(codon)

        return codons

    def length(self) -> int:
        # Cuenta los nucleótidos del ARN
        return len(self.sequence)

    def display(self) -> str:
        # Devuelve representación del ARN
        return f"5' - {self.sequence} - 3'"

    def __str__(self) -> str:
        return self.display()


class AminoAcid:
    # Representa un aminoácido.
    def __init__(
        self,
        name: str,
        abbreviation: str
    ):
        self.name = name
        self.abbreviation = abbreviation

    def __str__(self) -> str:
        return self.abbreviation


class Protein:
    # Representa cadena de aminoácidos construida tras la traducción
    def __init__(self):
        self.amino_acids: list[AminoAcid] = []

    def add_amino_acid(self, amino_acid: AminoAcid):
        # Añade un aminoácido a la cadena polipeptídica.
        self.amino_acids.append(amino_acid)

    def length(self) -> int:
        # Devuelve el número de aminoácidos de la proteína.
        return len(self.amino_acids)

    def sequence(self) -> str:
        # Devuelve la proteína utilizando abreviaturas de tres letras.
        return "-".join(
            amino_acid.abbreviation
            for amino_acid in self.amino_acids
        )

    def __str__(self) -> str:
        if not self.amino_acids:
            return "(proteína vacía)"

        return self.sequence()


class TransferRNA:
    # ARN de transferencia, con anticodón 3 -> 5 y aminoácido
    def __init__(
        self,
        anticodon_3_5: str,
        amino_acid: AminoAcid
    ):
        self.anticodon_3_5 = anticodon_3_5
        self.amino_acid = amino_acid

    def __str__(self) -> str:
        return (
            f"ARNt 3'-{self.anticodon_3_5}-5' "
            f"-> {self.amino_acid.name}"
        )


class Ribosome:
    def __init__(self):
        self.site_a = None
        self.site_p = None
        self.site_e = None

    def snapshot(self) -> dict:
        return {
            name: trna.anticodon_3_5 if trna is not None else None
            for name, trna in (
                ("A", self.site_a), ("P", self.site_p), ("E", self.site_e)
            )
        }

    def read(
        self,
        mrna: MessengerRNA,
        start: int
    ) -> list[str]:
        # Devuelve los codones del ARNm desde una posición.

        return mrna.get_codons(start)