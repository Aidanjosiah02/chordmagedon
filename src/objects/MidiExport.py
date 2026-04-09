import mido

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
        # is chord right format
        notes = chord if hasattr(chord, '__iter__') else [chord]

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
    print("meow")
