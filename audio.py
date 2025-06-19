import pygame 


# Initialize pygame mixer
pygame.mixer.init()

# Function to play alarm
def play_alarm():
    global alarm_playing
    pygame.mixer.music.load('alarm.mp3')
    pygame.mixer.music.play(-1)  # Loop alarm
    alarm_playing = True


# Function to stop alarm
def stop_alarm():
    global alarm_playing
    pygame.mixer.music.stop()
    alarm_playing = False