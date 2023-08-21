import openai
import speech_recognition as sr
import pyttsx3
import pygame
import math
import pyaudio
import threading 

from config import SECRET_KEY

openai.api_key = SECRET_KEY

microphone = sr.Microphone()

recognizer = sr.Recognizer()

microphone_event = threading.Event()

running = True 

#Pygame Initialization
screen_width = 500
screen_height = 500
pygame.init()
pygame.display.set_caption("Gerald Visualizer")
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

#Audio Initialization
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def get_microphone_input_level(): #1
	data = stream.read(CHUNK)
	rms = 0
	for i in range(0, len(data), 2):
		sample = int.from_bytes(data[i:i + 2], byteorder='little', signed=True)
		rms += sample * sample
	rms = math.sqrt(rms / (CHUNK / 2))
	return rms 

def draw_sine_wave(amplitude): #2
	screen.fill((0,0,0))
	points = []
	if amplitude > 10:
		for x in range(screen_width):
			y = screen_height/2 + int(amplitude * math.sin(x * 0.02))
			points.append((x, y))
	else:
		points.append((0, screen_height/2))
		points.append((screen_width, screen_height/2))

	pygame.draw.lines(screen, (255, 255, 255), False, points, 2)
	pygame.display.flip()


def text_to_speech(text): #3
	engine = pyttsx3.init()
	engine.setProperty("rate", 200)
	engine.say(text)
	engine.runAndWait()


def listen_microphone(): #4
	while microphone_event.is_set():
		with microphone as source:
			print("Listening...")
			audio = recognizer.listen(source)

		try:
			text = recognizer.recognize_google(audio)
			if text != "stop":
				gpt_response = get_gpt_response(text)
				text_to_speech(gpt_response)
				print("GPT: ", gpt_response)
			else:
				break
		except sr.UnknownValueError:
			print("Unable to recognize speech.")
		except sr.RequestError as e:
			print("Speech recognition request error:", str(e))

def get_gpt_response(text): #5
    response = openai.Completion.create(
        engine='text-curie-001',
        prompt= "Respond as my friend who only says a maximum of 2 sentences:"+ " " + text,
        max_tokens=500
    )
    response_text = response.choices[0].text.strip() if response.choices else "Sorry, I couldn't generate a response at the moment."
    return response_text

def game_loop(): #6
	running = True
	amplitude = 100 

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				microphone_event.clear()

		amplitude_adjustment = get_microphone_input_level() / 50
		amplitude = max(10, amplitude_adjustment)

		draw_sine_wave(amplitude)
		clock.tick(60)

	pygame.quit()

#Start Threads
pygame_thread = threading.Thread(target=game_loop)

pygame_thread.start()

microphone_event.set()

microphone_thread = threading.Thread(target=listen_microphone)

microphone_thread.start()

#End Threads
pygame_thread.join()

microphone_event.clear()

microphone_thread.join()