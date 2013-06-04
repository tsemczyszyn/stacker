#!/usr/bin/env python

import time
import curses
import hashlib
import sys


stack = []

class Task:

    def __init__(self):
            
        self.title = "default"
        self.taskID = hashlib.md5()
        self.creation = time.time() 
        self.elapsed = 0
        self.active = False
        self.selected = False

        self.timer_start = 0
        self.timer_stop = 0

        self.taskID.update(str(self.creation))

    def activate(self):
        self.timer_start = time.time()
        self.active = True

    def deactivate(self):
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
    curses.noecho()

    def addTask():

        global stack
        newTask = Task()
        newTask.activate()
        if (len(stack) != 0):
            stack[len(stack)-1].deactivate()

        stack.append(newTask)


    #Need a main loop here
    #Loop redraw the screen and check for input

    while (1):
        key = mainscr.getkey()
        if (key == 'n'):
            addTask()
        elif (key == 'x'):
            curses.endwin()
            sys.exit(0)
        key = ''
        
        taskwin.move(1, 1)
        for position, task in enumerate(stack):
            taskwin.addstr(task.title + "\t" + str(task.taskID.hexdigest()) + "\t" + str(task.active))
            taskwin.move(position+2, 1)

        taskwin.refresh()
