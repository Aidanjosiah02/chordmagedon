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

    # note duration
    note_duration = ticks_per_beat * 2

    # chord stuff
<<<<<<< Updated upstream
    # is chord right format - Use translation function
    notes = translate_midi_chord(arrangement.progression.chords)
    # starts notes
    for i, note in enumerate(notes):
        chord_track.append(mido.Message('note_on', note=int(note), velocity=velocity, time = 0))
    # ends notes
    for i, note in enumerate(notes):
        time_change = note_duration if i == 0 else 0
        chord_track.append(mido.Message('note_off', note=int(note), velocity = 0, time = time_change))

    # bass stuff - same logic I think - ask team
    #starts bass notes
    notes = translate_midi_bass(arrangement.bassline.notes)
    for i, n in enumerate(notes):
        bass_track.append(mido.Message('note_on', note=int(n), velocity = velocity, time = 0))
    #ends bass notes
    for i, n in enumerate(notes):
        time_change = note_duration if i == 0 else 0
        bass_track.append(mido.Message('note_off', note=int(n), velocity = 0, time = time_change))
=======
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
    
>>>>>>> Stashed changes
    # save file
    file.save('song.mid')
    print("Song finished!")

#Turn the output into something compatible with mido export  
def translate_midi_chord(notes):
    NOTE_MAP = {'C': 0, 'Cs': 1, 'Db': 1, 'D': 2, 'Ds': 3, 'Eb': 3, 'E': 4, 'F': 5, 'Fs': 6, 'Gb': 6, 'G': 7, 'Gs': 8, 'Ab': 8, 'A': 9, 'As': 10, 'Bb': 10, 'B': 11}
    result_list = []
    #Add 48 to each value for a certain octave - Maybe 60 if it sounds better
    for note in notes:
        if note in NOTE_MAP:
            result_list.append(NOTE_MAP[note] + 48)
        else:
            print("Unknown note")

    #What we are giving back to Mido
    return result_list
                
def translate_midi_bass(notes):
    BASS_MAP = {'C1': 24, 'E1': 28, 'G1': 31, 'A1': 33, 'C2': 36, 'E2': 40, 'G2': 43, 'A2': 45, 'C3': 48}
    result_list = []
    for note in notes:
        if note in BASS_MAP:
            result_list.append(BASS_MAP[note])
        else:
            print("Unknown")
    return result_list
