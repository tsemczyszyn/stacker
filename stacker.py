#!/usr/bin/env python

import time
import datetime
import curses
import hashlib
import sys
import thread

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
        self.elapsed += self.timer_stop - self.timer_start
        self.active = False


stack = []
render = True

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

    newTask = Task()
    newTask.activate()
    if (len(stack) != 0):
        stack[len(stack)-1].deactivate()

    stack.append(newTask)

def closeTask():

    if (len(stack) != 0):
        stack[len(stack)-2].activate()
        stack.pop()

def redrawStack():

    stackwin.move(0,0)

    for position, task in enumerate(stack):

        if (task.active == True):
            stackwin.addstr("\t" + task.title + "\t" + str(task.taskID.hexdigest()) + "\t" + str(datetime.timedelta(seconds=task.elapsed+(time.time() - task.timer_start))))
        else:
            stackwin.addstr(task.title + "\t" + str(task.taskID.hexdigest()) + "\t" + str(task.elapsed))

        stackwin.clrtoeol()
        stackwin.move(position+1, 0)

    stackwin.clrtobot()
    stackwin.refresh()

def threadedRedraw():
    while (render):
        redrawStack()
        time.sleep(0.25)

thread.start_new_thread(threadedRedraw, ())

while (1):

    key = mainscr.getkey()

    if (key == 'n'):
        addTask()
        redrawStack()

    elif (key == 'c'):
        closeTask()
        redrawStack()

    elif (key == 'x'):
        render = False
        curses.endwin()
        sys.exit(0)

