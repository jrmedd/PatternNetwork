var intervals = [2, 2, 1, 2, 2, 2, 1];
var notes = {c:0, cS:1, d:2, dS:3, e:4, f:5, fS:6, g:7, gS:8, a:9, aS:10, b:11};
var modes = {io:0, do:1, ph:2, ly:3, mi:4, ae:5, lo:6};

function midiMode(note, mode, octave) {
  startNote = notes[note] + (octave * 12);
  output = [startNote];
  mode = modes[mode];
  for (var i = 0; i < 7; i ++) {
    output[1+i] = output[i] + intervals[(mode+i)%7];
  }
  return output;
}
