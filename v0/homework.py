import requests
from canvasapi import Canvas
from datetime import datetime
import re

class Profile:
    def __init__(self,auth=[]):
        if len(auth)==2:
            self.canvas = Canvas(auth[0],auth[1])
        else:
            self.canvas = "none"
        self.canvasCourses = []
        self.other = []

    def add_canvas(self, url, token):
        '''
        Get Canvas access token in user settings
        '''
        self.canvas = Canvas(url,token)

    def add_canvas_course(self, numbername, method="assignments", formatbreaker=""):
        '''
        method: how/where homework is displayed, ie assignments tab,
        announcements tab, etc.
        types: assignments, announcements, home
        formatbreaker: used to separate multiple hw assignments on a single page. Ex:
        <strong>--------------------------------------------------------------------------------</strong>
        '''
        if self.canvas != "none":
            if str(numbername).isnumeric():
                self.canvasCourses.append([numbername,method,formatbreaker])
            else:
                for course in self.canvas.get_courses():
                    m = re.findall(numbername.lower(),str(course).lower())
                    if len(m) != 0:
                        self.canvasCourses.append([course.id,method,formatbreaker])
        else:
            raise Exception("No Canvas account added to profile.")
            #print("No Canvas account added to profile.")

    def add_other(self,url,hyperlink=""):
        self.other.append([url,hyperlink])

    def get_all_canvas_hw(self):
        if self.canvas != "none":
            homework = []
            for course in self.canvasCourses:
                
                c = self.canvas.get_course(course[0])
                method = course[1]
                formatbreaker = course[2]
                
                if method == "assignments":
                    
                    assignments = c.get_assignments()
                    for assignment in assignments:
                        if assignment.due_at == None:
                            continue
                        dueDate = datetime.strptime(assignment.due_at[:10],"%Y-%m-%d")
                        today = datetime.today()
                        if dueDate >= today:
                            m = re.findall("(?<=\<p>)(.*?)(?=\</p>)",str(assignment.description))
                            content = "\n".join(m)
                            homework.append([c.name, content,assignment.due_at])

                if method == "home":
                    
                    body = re.findall("(?<=\<p>)(.*?)(?=\</p>)", c.show_front_page().body)
                    body = body[:body[body.index(formatbreaker)+1:].index(formatbreaker)]
                    body = "\n".join(body)
                    body = body.replace("<strong>","")
                    body = body.replace("</strong>","")
                    homework.append(body)
                    
            return homework
                
                
        else:
            raise Exception("No Canvas account added to profile.")
            #print("No Canvas account added to profile.")

    def get_canvas_hw(self,course):
        ''' course must be in format of the class'''
        if self.canvas != "none":
            homework = []
            c = self.canvas.get_course(course[0])
            method = course[1]
            formatbreaker = course[2]
                
            if method == "assignments":
                    
                assignments = c.get_assignments()
                for assignment in assignments:
                    dueDate = datetime.strptime(assignment.due_at[:10],"%Y-%m-%d")
                    today = datetime.today()
                    if dueDate >= today:
                        m = re.findall("(?<=\<p>)(.*?)(?=\</p>)",str(assignment.description))
                        content = "\n".join(m)
                        homework.append(content)

            if method == "home":
                    
                body = re.findall("(?<=\<p>)(.*?)(?=\</p>)", c.show_front_page().body)
                body = body[:body[body.index(formatbreaker)+1:].index(formatbreaker)]
                body = "\n".join(body)
                body = body.replace("<strong>","")
                body = body.replace("</strong>","")
                homework.append(body)
                    
            return homework
                      
        else:
            raise Exception("No Canvas account added to profile.")
            #print("No Canvas account added to profile.")

    def print_hw(self):
        for x in self.get_canvas_hw():
            print(x)
            
    def get_other_hw(self):
        homework = []
        for page in self.other:
            p = requests.get(page[0])
            
            if page[1] != "":
                hyperlink = re.findall('(?<=\<a href=")(.*?)(?=\">'+page[1]+')', p.text)
                if len(hyperlink) != 0:
                    p = requests.get(page[0]+hyperlink[0])

            #very specific
            cells = re.findall('(?<=\<td>)(.*?)(?=\</td>)', p.text)
            cells = [x for x in cells if x != '&nbsp;']
            month = datetime.today().strftime("%B")
            dates = [x.split() for x in cells if month in x]
            day = datetime.today().strftime("%d")
            prevdates = [x for x in dates if int(x[1]) <= int(day)]
            print(len(prevdates))
            if len(prevdates) != 0:
                hwday = prevdates[-1]
                nextdate = dates.index(hwday)+1
                hwday = " ".join(hwday)
                #print(cells)
                content = cells[cells.index(hwday)+1:nextdate]
                #print(content,cells)
                homework += content
            
        return homework
        
        
            
                



