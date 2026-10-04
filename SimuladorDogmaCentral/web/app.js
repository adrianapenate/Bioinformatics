// Python hace los cálculos. JavaScript envía el ADN y muestra los resultados
const form = document.getElementById('form');
const button = document.getElementById('simulate');
const error = document.getElementById('error');
const results = document.getElementById('results');

function show(id, text) {
  document.getElementById(id).textContent = text;
}

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  button.disabled = true;
  button.textContent = 'Simulando…';
  error.hidden = true;
  results.hidden = true;

  try {
    const response = await fetch('/api/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sequence: document.getElementById('sequence').value })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);

    const leading = data.replication.leading_strand;
    const lagging = data.replication.lagging_strand;
    show('leading', 'Molde: 3′ ' + leading.template + ' 5′\nNueva: 5′ ' + leading.new_strand + ' 3′');
    show('lagging', 'Molde: 5′ ' + lagging.template + ' 3′\nNueva: 3′ ' + lagging.new_strand + ' 5′');

    show('dna', 'Molécula hija 1:\n5′ ' + data.dna.coding + ' 3′  (original)\n3′ ' +
      data.dna.template + ' 5′  (nueva)\n\nMolécula hija 2:\n5′ ' +
      data.dna.coding + ' 3′  (nueva)\n3′ ' + data.dna.template + ' 5′  (original)');

    const fragments = data.replication.lagging_strand.okazaki_fragments;
    show('fragments', fragments.map(f =>
      'Fragmento ' + f.number + ': 5′ ' + f.sequence_5_3 + ' 3′'
    ).join('\n'));

    show('rna', 'ADN molde: 3′ ' + data.dna.template + ' 5′\nARNm:      5′ ' +
      data.transcription.mrna_sequence + ' 3′');

    const translation = data.translation;
    show('codons', translation.codons.join(' | ') || 'No se encontró AUG.');
    show('protein', translation.protein || 'No se ha sintetizado una cadena.');

    // Utilizamos los pasos calculados por Python, solo hasta el primer STOP.
    const rows = document.getElementById('translation-rows');
    rows.replaceChildren();
    document.getElementById('translation-table').hidden = translation.translation_steps.length === 0;
    for (const step of translation.translation_steps) {
      const row = document.createElement('tr');
      const aminoAcid = step.type === 'STOP'
        ? 'STOP · terminación, no codifica un aminoácido'
        : step.amino_acid.name + ' (' + step.amino_acid.abbreviation + ')';
      for (const value of [step.codon_number, step.codon, aminoAcid]) {
        const cell = document.createElement('td');
        cell.textContent = value;
        row.append(cell);
      }
      rows.append(row);
    }

    let status;
    if (translation.completed) {
      status = 'La traducción termina en ' + translation.stop_codon + '.';
    } else if (translation.start_position === -1) {
      status = 'Sin AUG, la traducción no puede comenzar.';
    } else {
      status = 'Cadena parcial: se ha llegado al final sin encontrar STOP.';
    }
    if (translation.incomplete_codon) {
      status += ' Bases finales sin codón completo: ' + translation.incomplete_codon + '.';
    }
    if (translation.untranslated_after_stop) {
      status += ' Después de STOP queda sin traducir: ' + translation.untranslated_after_stop + '.';
    }
    show('status', status);
    results.hidden = false;
  } catch (problem) {
    error.textContent = problem instanceof TypeError
      ? 'No se puede conectar. Comprueba que web_app.py sigue abierto.'
      : problem.message;
    error.hidden = false;
  } finally {
    button.disabled = false;
    button.textContent = 'Simular';
  }
});

