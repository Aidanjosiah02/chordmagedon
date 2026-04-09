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
    for chord in arrangement.progression.chords:
        # is chord right format - Use translation function
        notes = translate_midi(chord if hasattr(chord, '__iter__') else [chord])
        
        # starts notes
        for i, note in enumerate(notes):
            chord_track.append(mido.Message('note_on', note=int(note), velocity=velocity, time = 0))
        # ends notes
        for i, note in enumerate(notes):
            time_change = note_duration if i == 0 else 0
            chord_track.append(mido.Message('note_off', note=int(note), velocity = 0, time = time_change))

    # bass stuff - same logic I think - ask team
    for note in arrangement.bassline.notes:
        #starts bass notes
        notes = [note]
        for i, n in enumerate(notes):
            bass_track.append(mido.Message('note_on', note=int(n), velocity = velocity, time = 0))
        #ends bass notes
        for i, n in enumerate(notes):
            time_change = note_duration if i == 0 else 0
            bass_track.append(mido.Message('note_off', note=int(n), velocity = 0, time = time_change))
    # save file
    file.save('song.mid')
    print("Song finished!")

#Turn the output into something compatible with mido export  
def translate_midi(arrangement):
    NOTE_MAP = {'C': 0, 'Cs': 1, 'Db': 1, 'D': 2, 'Ds': 3, 'Eb': 3, 'E': 4, 'F': 5, 'Fs': 6, 'Gb': 6, 'G': 7, 'Gs': 8, 'Ab': 8, 'A': 9, 'As': 10, 'Bb': 10, 'B': 11}
    NOTE_ITEMS = list(NOTE_MAP.values())
    NOTE_KEYS = list(NOTE_MAP.keys())
    RESULT_MAP = {}
    result_list = []
    #Add 48 to each value for a certain octave - Maybe 60 if it sounds better
    for NOTE_ITEMS, NOTE_KEYS in NOTE_MAP.items():
        match NOTE_KEYS:
            case 'C':
                result_list.append(NOTE_MAP.get('C') + 48)
            case 'Cs':
                result_list.append(NOTE_MAP.get('Cs') + 48)
            case 'Db':
                result_list.append(NOTE_MAP.get('Db') + 48)
            case 'D':
                result_list.append(NOTE_MAP.get('D') + 48)
            case 'Ds':
                result_list.append(NOTE_MAP.get('Ds') + 48)
            case 'Eb':
                result_list.append(NOTE_MAP.get('Eb') + 48)
            case 'E':
                result_list.append(NOTE_MAP.get('E') + 48)
            case 'F':
                result_list.append(NOTE_MAP.get('F') + 48)
            case 'Fs':
                result_list.append(NOTE_MAP.get('Fs') + 48)
            case 'Gb':
                result_list.append(NOTE_MAP.get('Gb') + 48)
            case 'G':
                result_list.append(NOTE_MAP.get('G') + 48)
            case 'Gs':
                result_list.append(NOTE_MAP.get('Gs') + 48)
            case 'Ab':
                result_list.append(NOTE_MAP.get('Ab') + 48)
            case 'A':
                result_list.append(NOTE_MAP.get('A') + 48)
            case 'As':
                result_list.append(NOTE_MAP.get('As') + 48)
            case 'Bb':
                result_list.append(NOTE_MAP.get('Bb') + 48)
            case 'B':
                result_list.append(NOTE_MAP.get('B') + 48)
            case _:
                print("Unknown note.")

    #What we are giving back to Mido
    return result_list
                

