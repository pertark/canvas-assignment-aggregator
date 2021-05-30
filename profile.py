import requests
from canvasapi import Canvas
from datetime import datetime
import re

class Profile:
    def __init__(self, auth, empty=False):
        assert len(auth) == 2
        self.canvas = Canvas(auth[0],auth[1])
        if empty:
            self.courses = []
        else:
            self.courses = [i.id for i in self.canvas.get_courses(enrollment_state='active')]
        self.other = []
        self.get_all_canvas_hw = self.get_all_homework
        

    def add_canvas(self, url, token):
        '''
        Get Canvas access token in user settings
        '''
        self.canvas = Canvas(url,token)

    def add_canvas_course(self, num):
        '''
        At this point, all classes are "Assignments" based
        '''
        if self.canvas == "":
            raise Exception("No Canvas account added to profile.")
        
        if str(num).isnumeric():
            self.courses.append(num)
            
    def get_canvas_hw(self, course):
        homework = []
        c = self.canvas.get_course(course)

        
        assignments = c.get_assignments(order_by='due_at', include='submission')
        for assignment in assignments:
            submission = assignment.submission
                
            if submission['workflow_state'] == 'unsubmitted' and assignment.submission_types[0] != "none": # and not assignment.locked_for_user:
                m = re.findall("(?<=\<p>)(.*?)(?=\</p>)",str(assignment.description))
                content = "\n".join(m)
                homework.append({
                    "course": {"name": c.name, "id": course},
                    "assignment": {"name": assignment.name, "id": assignment.id},
                    "content": content,
                    "due_date": assignment.due_at,
                    "missing": submission['missing']
                    })
        return homework

        ### mostly ignore below
        assignments = c.get_assignments()
        for assignment in assignments:
            if assignment.due_at == None:
                continue
            dueDate = datetime.strptime(assignment.due_at[:10],"%Y-%m-%d")
            today = datetime.today()
            if dueDate >= today:
                m = re.findall("(?<=\<p>)(.*?)(?=\</p>)",str(assignment.description))
                content = "\n".join(m)
                homework.append([c.name, assignment.name, content, assignment.due_at, False])
                    
        return homework

    def get_all_homework(self):
        res = []
        for course in self.courses:
            res += self.get_canvas_hw(course)
        return res

    '''def get_all_canvas_hw(self):
        return self.get_all_homework(self)
'''
