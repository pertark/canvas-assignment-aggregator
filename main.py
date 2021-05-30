from profile import Profile
import logging
from datetime import datetime
logging.basicConfig(filename='logger.log', level=logging.INFO)
logging.info('Imported profile.')
import time

with open('token.txt') as f:
    token = f.read()

with open('url.txt') as f:
    url = f.read()
    
p = Profile((url,token))
logging.info('Getting all homework.')
start = time.time()
homework = p.get_all_canvas_hw()
end = time.time()
logging.info(f'Retrieved all homework, {end-start} seconds elapsed.')

head = '''
        <html>
        <head>
        <title>Upcoming Homework</title>
        <link rel="stylesheet" href="style.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        </head>
        <body>
        <script>
        
        $( "td" ).click(function() {
          $( this ).parent().toggleClass( "dark" );
          $( this ).parent().toggleClass( "light" );
          console.log('clicked');
        });
        
        </script>
        
        <table>
        <tr>
            <th>Class</th>
            <th>Assignment</th>
            <th>Content</th>
            <th>Due Date</th>
        </tr>
        '''


content = ''.join([f'''<tr class="{"red" if i[4] else "white"}">
                        <td>{i["course"]["name"]}</td>
                        <td><a href="{url+"/courses/"+str(i["course"]["id"])+"/assignments/"+str(i["assignment"]["id"])}">{i["assignment"]["name"]}</a></td>
                        <td>{i["content"]}</td>
                        <td>{str(datetime.strptime(i[3],"%Y-%m-%dT%H:%M:%SZ") if items["due_date"] else "None")[5:]}</td>
                    </tr>''' for i in homework])

tail = '''
        </table>
        </body>
        </html>
        '''
with open('all_homework.html','w',encoding='utf-8') as f:
    f.write(head + content + tail)

'''
#debug stuff
co = p.courses
assign = p.canvas.get_course(499638).get_assignments(order_by='due_at', include='submission')
bios = [i for i in p.canvas.get_course(co[0]).get_assignments(order_by='due_at', include='submission')]
a=[i for i in assign][-1]
assignment = [i for i in assign][-1].submission
'''
