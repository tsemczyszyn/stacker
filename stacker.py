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
    taskdims = taskwin.getmaxyx()

    #Stackwin
    stackwin = taskwin.derwin(taskdims[0]-2, taskdims[1]-2, 1, 1)

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

    def closeTask():

        global stack
        if (len(stack) != 0):
            stack[len(stack)-2].activate()
            stack.pop()

    #Need a main loop here
    #Loop redraw the screen and check for input

    while (1):

        key = mainscr.getkey()

        if (key == 'n'):
            addTask()

        elif (key == 'c'):
            closeTask()

        elif (key == 'x'):
            curses.endwin()
            sys.exit(0)

        key = ''
        stackwin.move(0,0)
        for position, task in enumerate(stack):
            stackwin.addstr(task.title + "\t" + str(task.taskID.hexdigest()) + "\t" + str(task.active))
            stackwin.clrtoeol()
            stackwin.move(position+1, 0)

        stackwin.clrtobot()
        stackwin.refresh()
