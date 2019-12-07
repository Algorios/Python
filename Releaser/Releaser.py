# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 23:06:45 2019

@author: owner
"""

from tkinter import filedialog, messagebox, Tk, Frame, StringVar, Label, Button, mainloop, W, N, E, S, LEFT, Listbox
import os
#import sys

version='Releaser 0.1.1'

def find(name, path):
    for root, disr, files in os.walk(path):
        if name in files:
            return root
import git
from git import Git

master=Tk()
master.title(version)
master.minsize(300,160)
frame=Frame(master)
frame.grid(row=2, column=3, sticky=E+N+W)
variable=StringVar(master)
repo_path=''
releaseFile_path=''

def RepoPath():
    global repo_path
    repo_path=filedialog.askdirectory(title='Please select a local junodatabase repo folder', parent=master)
    Label_02.configure(repo_path)
    
def ReleaseFile():
    global releaseFile_path
    releaseFile_path=filedialog.askopenfilename(title='Please select a release file in your local directory', parent=master)
    Label_12.configure(releaseFile_path)
    
def LoadCommits():
    if repo_path !='' and releaseFile_path !='':
        global g
        try:
            g=Git(repo_path)
        except:
            print('Problem with the selected repo folder')
        #g.checkout('develop') #this can be used to automaticaly checkout to a certain branch
        log_list=g.log('--merges', '--max-count=30', '--first-parent').split('\n\ncommit')
        #log_list=g.log().split('\n\ncommit')
        matching_granular=[i.split('\n')[:6] for i in log_list]
        global dd_list
        dd_list=[]
        for e in matching_granular[0:50]:
           #this can be used to get just the required informantion
           #dd_list.append(e[0].replace('commit', '').lstrip()[:50]+', '
                            #+ ''.join(e[2].split(':')[1].strip().split(','))+', '
                            #+ ' '.join(e[3].split(' ')[1:7]).strip()+', '
                            #+ e[5].split('from')[-1].strip().lstrip()[:100]+ ' ...'
                            #)
            #this loads the whole log info:
            dd_list.append(e)
        global variable
        variable.set('select commit')
        global w
        w=Listbox(master, selectmode='multiple', width=150, height=30)
        w.insert('end', *dd_list)
        w.grid(row=2,column=2,stick=W)
    else:
        messagebox.showinfo('Warning', 'You need to select a repo folder and a release file first!', parent=master)
        
        
def GetListBox():
    print('\n')
    print('Selected commits:')
    for i in w.curselection():
        print (dd_list[i])

def GitCall():
    global commits
    commits=[]
    
    for i in w.curselection():
        commits.append(git.Repo(repo_path).commit(dd_list[i][:11]))
        
    global files
    files={}
    
    for num, commit in enumerate(commits):
        k=str(commits[num])
        v=list(commit.stats.files.keys())
       
        #remove something
        """
        try:
            v.remove('File')
        except Exception:
            pass
        """
        #remove somthing 2 (if needed)
        for i in v:
            if i.startswith('abcdefgh'):
                v.remove(i)
            files[k]=v
   
def ShowScripts():
    if repo_path != '' and releaseFile_path !='':
        GitCall()
        print('\n')
        print('Scripts updated by the selected commits:')
        for key, value in files.items():
                for i in value:
                    print(str(key)[:11]+': '+i)
    else:
        messagebox.showinfo('Warning', 'You need to select a repo folder and a release file and a commit first!', parent=master)
        
def UpdateReleaseFile():
    if repo_path != '' and releaseFile_path !='':
        GitCall()
        reversed_comits=list(reversed(commits))
        for num, commit in enumerate(reversed_comits):
            print(str(reversed_comits[num]))
            with open(releaseFile_path, 'a') as outfile:
                outfile.write('\n')
                outfile.write('--RELEASER START '+commit.summary)
                print(str(commit)[:11]+' releasing files:')
                for fname in files[str(commit)]:
                    try:
                        with open(repo_path+'/'+fname) as infile:
                            outfile.write('\n')
                            outfile.write('GO')
                            outfile.write('\n')
                            outfile.write('\n')
                            outfile.write('--'+ fname)
                            outfile.write('\n')
                            outfile.write(infile.read())
                            outfile.write('\n')
                            outfile.write('GO')
                        print(fname)
                    except:
                        print('**************** ' + fname +' was not found')
                outfile.write('--RELEASER END '+commit.summary)
            print(str(reversed_comits[num])[:11]+ ' end')
        #g.checkout('develop')
        messagebox.showinfo('Confirmation','Done', parent=master)  
    else:
        messagebox.showinfo('Warning', 'You need to select a repo folder and a release file and a commit first!', parent=master)
    
class LeftLabel:
    def __init__(self, row, text):
        self.Label=Label(master, text=text)
        self.Label.grid(row=row, column=1, sticky=N+E)
class MidleLabel:
    def __init__(self, row, text):
        self.Label=Label(master, text=text, bg='white', justify=LEFT, anchor=W)
        self.Label.grid(row=row, column=2, sticky=N+S+E+W)
    def configure(self, text):
        self.Label.configure(text=text)
class RightButton:
    def __init__(self, row, text,command):
        self.Button=Button(master, text=text, command=command)
        self.Button.grid(row=row, column=3, sticky=N+E+W)
class FrameButton:
    def __init__(self, row, text,command):
        self.Button=Button(frame, text=text, command=command)
        self.Button.grid(row=row, column=1, sticky=N+E+W)

button_03=RightButton(0, 'Browse', RepoPath)     
button_13=RightButton(1, 'Browse', ReleaseFile)
button_33=RightButton(5, 'Update Release File', UpdateReleaseFile)

button_0=FrameButton(0, 'LoadCommits', LoadCommits)     
button_1=FrameButton(1, 'Print Selected Commits', command=GetListBox)
button_2=FrameButton(2, 'Print Selected Scripts', command=ShowScripts)

Label_01=LeftLabel(0, 'Selected local repo folder:')
Label_11=LeftLabel(1, 'Selected release file:')
Label_21=LeftLabel(2, 'Selected commit(s):')

Label_02=MidleLabel(0, repo_path)
Label_12=MidleLabel(1, releaseFile_path)

mainloop()


        
        