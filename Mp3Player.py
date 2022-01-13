import time
from tkinter import *
import pygame
from tkinter import filedialog
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.geometry("470x470")
root.minsize(470, 470)
root.maxsize(470, 470)
root.title('MP3 Player')
root.configure(bg='grey')
root.wm_iconbitmap(f'E:/User Data/Downloads/musicimg.ico')

# Intialize Pygame Mixer
pygame.mixer.init()


# Add One Song Function
def add_song():
    global song
    song = filedialog.askopenfilename(initialdir='E:/Hangout/Music/', title="Choose A Song",
                                      filetypes=(("mp3 Files", "*.mp3"),))
    # strip out the dir info and .mp3 extension from the song player
    song = song.replace("E:/Hangout/Music/", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)


# Add Many Song Function
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='E:/Hangout/Music/', title="Choose A Song",
                                        filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        # strip out the dir info and .mp3 extension from the song player
        song = song.replace("E:/Hangout/Music/", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)


# Play selected song
def play():
    song = song_box.get(ACTIVE)
    song = f'E:/Hangout/Music/{song}.mp3'

    try:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    except:
        return None

    # call the play time function to get the length
    play_time()


# stop the current playing song
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    my_slider.config(value=0)
    time_position.config(text='')


def previous_song():
    next_one = song_box.curselection()
    next_one = next_one[0] - 1
    song = song_box.get(next_one)
    song = f'E:/Hangout/Music/{song}.mp3'

    try:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    except:
        return None

    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

    my_slider.config(value=0)
    time_position.config(text='')


def next_song():
    next_one = song_box.curselection()
    next_one = next_one[0] + 1
    song = song_box.get(next_one)
    song = f'E:/Hangout/Music/{song}.mp3'

    try:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    except:
        return None

    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

    my_slider.config(value=0)
    time_position.config(text='')


# global paused variable
global paused
paused = False


# pause and unpause the current song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


# To Delete a song
def delete_song():
    song_box.delete(ANCHOR)
    # stop the playing music
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    my_slider.config(value=0)
    time_position.config(text='')


# To Delete all song
def delete_all_song():
    song_box.delete(0, END)
    # stop the playing music
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    my_slider.config(value=0)
    time_position.config(text='')


# To grab a song length time info
def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000
    # converted to time format
    # converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))
    song = song_box.get(ACTIVE)
    song = f'E:/Hangout/Music/{song}.mp3'

    # using mutagen here
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_current_song = time.strftime('%H:%M:%S', time.gmtime(song_length))

    current_time += 1
    if int(my_slider.get()) == int(song_length):
        time_position1.config(text=f'Time Elapsed: {converted_current_song} ')

    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime('%H:%M:%S', time.gmtime(my_slider.get()))
        time_position.config(text=f'{converted_current_time}')
        time_position1.config(text=f'{converted_current_song}')

        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    time_position.after(1000, play_time)


# create slider function
def slide(x):
    song = song_box.get(ACTIVE)
    song = f'E:/Hangout/Music/{song}.mp3'

    try:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
    except:
        return None


def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


# master frame created
master_frame = Frame(root, bg='grey')
master_frame.pack(pady=20)

# Create Playlist Box4
song_box = Listbox(master_frame, bg='black', fg='orange', width='70', height='12', selectbackground='grey',
                   selectforeground='black')
song_box.grid(row=0, column=0)

# define player control button images
back_btn_img = PhotoImage(file='E:/User Data/Downloads/buttons png/back.png')
play_btn_img = PhotoImage(file='E:/User Data/Downloads/buttons png/play.png')
pause_btn_img = PhotoImage(file='E:/User Data/Downloads/buttons png/pause.png')
stop_btn_img = PhotoImage(file='E:/User Data/Downloads/buttons png/stop.png')
forward_btn_img = PhotoImage(file='E:/User Data/Downloads/buttons png/forward.png')

# create a player control frame
controls_frame = Frame(master_frame, bg='grey')
controls_frame.grid(row=1, column=0, pady=20)

# volume_frame
volume_frame = LabelFrame(master_frame, text='Volume', bg='grey')
volume_frame.grid(row=4, column=0, sticky=W, pady=10)

# create player control button
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, bg='grey', command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, bg='grey', command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, bg='grey', command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, bg='grey', command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, bg='grey', command=stop)

back_button.grid(row=0, column=0, padx=8)
forward_button.grid(row=0, column=1, padx=8)
play_button.grid(row=0, column=2, padx=8)
pause_button.grid(row=0, column=3, padx=8)
stop_button.grid(row=0, column=4, padx=8)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Add Song Menu
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

# Add Many Song Menu
add_song_menu.add_command(label="Add Many Song To Playlist", command=add_many_songs)

# create delete song menu
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song", command=delete_song)
remove_song_menu.add_command(label="Delete All Song", command=delete_all_song)

time_position = Label(master_frame)
time_position.grid(row=3, column=0, sticky=W)

time_position1 = Label(master_frame)
time_position1.grid(row=3, column=0, sticky=E)

# create music position slider
my_slider = ttk.Scale(master_frame, from_=0, to_=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=7)

# create volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to_=1, orient=HORIZONTAL, value=1, command=volume, length=125)
volume_slider.pack(padx=10)

root.mainloop()
