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

    def format_timedelta(self, tdelta):

        seconds = tdelta.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return '%02d:%02d:%02d' % (hours, minutes, seconds)

    def draw(self):
        if (self.active):
            dt = datetime.timedelta(seconds=self.elapsed+(time.time() - self.timer_start))
            drawText = " " + self.title + "\t" + str(self.selected) + "\t" + self.format_timedelta(dt) 
        else:
            dt = datetime.timedelta(seconds=self.elapsed)
            drawText = self.title + "\t" + str(self.selected) + "\t" + self.format_timedelta(dt)

        return drawText

#----------Functions--------------------------------------------------------

def addTask():

    #Never add more tasks than can fit on the current screen
    if (len(stack) > taskdims[0]-4):
        return

    newTask = Task()
    newTask.activate()

    #Deactivate the last item in the stack before adding a new active task
    if (len(stack) != 0):
        stack[len(stack)-1].deactivate()

    
    stack.append(newTask)

    if (len(stack) == 1):
        stack[0].selected = True

def closeTask():

    if (len(stack) != 0):
        stack[len(stack)-2].activate()
        stack.pop()

def redrawStack():

    stackwin.move(0,0)

    for position, task in enumerate(stack):

        if (task.selected):
            stackwin.addstr(task.draw(), curses.A_REVERSE)
        else:
            stackwin.addstr(task.draw())

        stackwin.clrtoeol()
        stackwin.move(position+1, 0)

    stackwin.clrtobot()
    stackwin.refresh()

def redrawDescrip():
    #description.addstr("Hey look here!")
    description.refresh()


def threadedRedraw():
    while (render):
        redrawStack()
        redrawDescrip()
        time.sleep(0.25)

def exitApp():
    render = False
    curses.endwin()
    sys.exit(0)

#Runtime state variable
stack = []
select_pointer = 0
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
        exitApp()

    elif (key == 'j'):
        if (select_pointer < (len(stack)-1)):
            select_pointer += 1
            stack[select_pointer].selected = True
            stack[select_pointer-1].selected = False
            redrawStack()

    elif (key == 'k'):
        if (select_pointer > len(stack)-1):
            select_pointer = len(stack)-1

        if (select_pointer != 0):
            select_pointer -= 1
            stack[select_pointer].selected = True
            stack[select_pointer+1].selected = False
            redrawStack()


