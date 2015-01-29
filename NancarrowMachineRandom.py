# NancarrowMachine.py
# Sam Goree
# January 2015
# Main Class of the NancarrowMachine project - Generates canons in the style of Conlon Nancarrow's Study no. 19 for player piano

#TODO: Make the melody longer, not just the length of the talea

from midiutil.MidiFile3 import MIDIFile
import time
import random
import math

bottom = 10

def main():
	voices = 3
	voiceSize = 36
	instRange = 72
	ratios = [1, 2, 8];
	Piece = GeneratePiece(voices, voiceSize, instRange, ratios)
	binfile = open("output" + time.strftime("%d-%m-%Y") + time.strftime("-%H-%M-%S")+ ".mid", 'wb')
	Piece.writeFile(binfile)
	binfile.close()
	
# GeneratePiece generates a MIDI file with N tracks that was composed algorithmically
# Uses the algorithm detailed on p. 9-10 of "The Player-Piano Music of Conlon Nancarrow" by Carlsen
# voices is the number of voices
# voiceSize is the range of each voice, in half-steps
# range is the total range of the piece, in half-steps
# ratios is the ratio of tempos between voices. R[0] should be 1, for the bottom voice
def GeneratePiece(voices, voiceSize, instRange, ratios):
	C = (instRange - voiceSize)//voices #the interval of imitation
	retval = MIDIFile(voices)
	#voices is the number of voices, numbered from bottom up
	#set tempi
	track = 0
	for r in ratios:
		retval.addTempo(track, 0, r * 80)
		track+=1
	#generate taleae, talea[0] is the top octave's talea, talea[1] is the next highest, etc.
	talea = [[]]
	for i in range(0, random.randint(3, 5)):
		talea[0].append(random.randint(1,5))
	#each other talea is the same number of notes, with each note lengths incremented 1 or 2 times
	for m in range(1, math.floor(voiceSize//12)):
		talea.append([])
		for i in range(0, len(talea[0])):
			talea[m].append(talea[m-1][i] + random.randint(1, 2))
	print(talea)
	#calculate the length of the piece (in half steps)
	length = 1
	temp = 0
	for m in range(0, len(talea)):
		temp = 0
		for i in range(0, len(talea[m])):
			temp += talea[m][i]
		length = lcm(length, temp)
	print(length)
	#figure out where each voice enters
	entrances = []
	for m in range(0, len(ratios)):
		temp = (ratios[m]-1)/ratios[m] * length
		print(temp)
		entrances.append(temp)
	
	#write a melody for each octave of a single voice
	melody = GenerateMelody(talea, length)
	print (len(melody[0]))
	#write the melody to the midi file in each voice
	currentTime = 0
	for n in range(0, voices):
		for m in range(0, voiceSize//12):
			currentTime = entrances[n]
			i = 0
			while currentTime < length:
				i += 1
				retval.addNote(n, 0, bottom + melody[m][i] + (C * n), currentTime, talea[m][i%len(talea[m])]/2, 100)
				currentTime+=talea[m][i%len(talea[m])]
			#add in a last note
			retval.addNote(n, 0, bottom + melody[m][0] + (C * n), currentTime, 1, 100)
	return retval
	
# Generates a melody with notes pitches, which is returned as a 2d list of distances above C, with one list per octave of the melody
# TODO
def GenerateMelody(talea, length):
	retval = [[],[]]
	# generate the top melody
	for i in range(length):
		retval[0].append(random.randint(1, 12))
	# generate the other melodies from this one
	for m in range(1, len(talea)):
		currentTime = 0
		i = 0
		while currentTime < length:
			i+=1
			i%=len(talea[m])
			#find the pitch for this note
			tempTime = 0
			k = 0
			while tempTime < currentTime:
				k+=1
				k%=len(talea[0])
				tempTime+=talea[0][k]
			pitch = retval[0][k]
			#put it in the melody
			retval[m].append(12 * (len(talea) - m) + pitch)
			currentTime += talea[m][i]
		retval.append([])
	return retval

def gcd(a, b):
    #Return greatest common divisor using Euclid's Algorithm.
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    #Return lowest common multiple.
    return a * b // gcd(a, b)


main()