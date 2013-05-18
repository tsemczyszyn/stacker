#!/usr/bin/env python

import time
import curses
import hashlib

class Task:

    def __init__(self):
        title = "default"
        taskID = hashlib.md5()
        creation = time.time() 
        elapsed = 0
        active = False
        selected = False

        timer_start = 0
        timer_stop = 0

        taskID.update(creation)

    def activate():
        self.timer_start = time.time()
        self.active = True

    def deactivate():
        self.timer_stop = time.time()
        self.elapsed = self.timer_stop - self.timer_start
        self.active = False

class Stacker:

    #Create the window for curses stuff
    mainscr = curses.initscr()

    #Menu
    mainscr.addstr("\n\n\n N", curses.A_UNDERLINE)
    mainscr.addstr("ew Task\n")
    mainscr.addstr(" E", curses.A_UNDERLINE)
    mainscr.addstr("dit Task\n")
    mainscr.addstr(" C", curses.A_UNDERLINE)
    mainscr.addstr("lose Task\n")
    mainscr.addstr(" C")
    mainscr.addstr("a", curses.A_UNDERLINE)
    mainscr.addstr("ncel Task\n")
    mainscr.addstr(" E")
    mainscr.addstr("x", curses.A_UNDERLINE)
    mainscr.addstr("it\n")

    mainscr.border(0)
    mainscr.addstr(0, 1, "Task Stacker")
    mainscr.refresh()

    dims = mainscr.getmaxyx()
    
    #Initialize Task Window
    taskwin = mainscr.subwin(dims[0]-4, (dims[1]/2)-7, 2, 15)
    taskwin.border(0)
    taskwin.addstr(0, 1, "Tasks")
    taskwin.refresh()

    #Initialize Description Window
    description = mainscr.subwin(dims[0]-4, (dims[1]/2)-10, 2, (dims[1]/2)+9)
    description.border(0)
    description.addstr(0, 1, "Description")
    description.refresh()
    curses.curs_set(0)
    mainscr.getch()

    #Need a main loop here
    #Loop redraw the screen and check for input

    curses.endwin()

