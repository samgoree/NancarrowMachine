from midiutil.MidiFile3 import MIDIFile

MyMIDI = MIDIFile(1)

track = 0
time = 0

MyMIDI.addTrackName(track,time,"Sample Track")
MyMIDI.addTempo(track,time,120)

track = 0
channel = 0
pitch = 60
time = 0
duration = 10
volume = 100

MyMIDI.addNote(track,channel,pitch,time,duration,volume)

binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()