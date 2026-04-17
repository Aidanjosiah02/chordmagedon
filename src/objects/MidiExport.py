import mido
from src.objects.Chord import Chord
from src.utils.io_handler import load_pickle
from src.constants import ARRANGEMENT_PICKLE, GENERATIONS, PROCESSED_DIR, MARKOV_PICKLE_SUFFIX, MUTATION_RATE, POPULATION_SIZE, NOTE_MAP
from src.objects.Arrangement import Arrangement 
from src.objects.ChordProgression import ChordProgression
from src.objects.Bassline import BassLine

def export_midi(arrangement, filename='song.mid', tempo = 500000, ticks_per_beat=480, velocity=64):
    # create file
    file = mido.MidiFile(type=1, ticks_per_beat=ticks_per_beat)
    chord_track = mido.MidiTrack()
    bass_track = mido.MidiTrack()

    file.tracks.append(chord_track)
    file.tracks.append(bass_track)
    
    # tempo
    tempo_message = mido.MetaMessage('set_tempo', tempo=tempo, time = 0)
    chord_track.append(tempo_message)
    bass_track.append(tempo_message)

    # change instruments
    #90 - Polysynth, 38 - Synth Bass 1
    chord_track.append(mido.Message('program_change', program=90, time = 0))
    bass_track.append(mido.Message("program_change", program=38, time=0))

    # note duration
    note_duration = ticks_per_beat * 2

    # chord stuff
    for chord in arrangement.progression.chords:
        if chord is None:
            chord_track.append(mido.Message('note_on', note=0, velocity=0, time=note_duration))
            continue
        midi_notes = translate_midi_chord(chord)

        step = note_duration // len(midi_notes)
        
        for i, note in enumerate(midi_notes):
            # turn on note, turn off note, then move onto next. NOT a block of chords.
            # turn on notes
            chord_track.append(mido.Message('note_on', note=int(note), velocity=velocity, time=0))
            # turn off notes 
            chord_track.append(mido.Message('note_off', note=int(note), velocity=0, time=step))
    # bass stuff
    for note in arrangement.bassline.notes:
        if note is None:
            bass_track.append(mido.Message('note_on', note = 0, velocity = 0, time=note_duration))
            continue
        midi_note = translate_midi_bass(note)
        #turn on and off
        bass_track.append(mido.Message('note_on', note=int(midi_note), velocity=velocity, time=0))
        bass_track.append(mido.Message('note_off', note=int(midi_note), velocity = 0, time=note_duration))
    
    # save file
    file.save(filename)
    print("Song finished!")

#Turn the output into something compatible with mido export  
def translate_midi_chord(chord):
   from src.constants import NOTE_POSITIONS
   intervals = NOTE_POSITIONS[chord.quality.value]
   midi_notes = [(chord.root + interval + 48) for interval in intervals]
   return midi_notes
                
def translate_midi_bass(note):
    midi_note = (note + 36)
    return midi_note
