import sys

import matplotlib.pyplot as plt
from flask import Flask, render_template_string


student_data_page = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <title>Student Data</title>
                        </head>
                        <body>
                            <div><h1> Student Details </h1></div>
                            
                            <div>
                                <table border="1" cellpadding="1" cellspacing="0">
                                    <tr>
                                        <th>Student ID</th>
                                        <th>Course ID</th>
                                        <th>Student Name</th>
                                    </tr>
                                    {% for student in data %}
                                        <tr>
                                            <td> {{student.0}} </td>
                                            <td> {{student.1}} </td>
                                            <td> {{student.2}} </td>
                                        </tr>
                                    {% endfor %}
                                    <tr>
                                        <td colspan=2> Total Marks </td>
                                        <td> {{ total }} </td>
                                    </tr>
                                </table>
                            </div>
                        </body>
                        </html>
                        """

course_page ="""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Course Data</title>
                </head>
                <body>
                    <div><h1> Course Details </h1></div>
                    
                    <div>
                        <table border="1" cellpadding="1" cellspacing="0">
                            <tr>
                                <th> Average Marks </th>
                                <th>Maximum Marks</th>
                            </tr>
                            <tr>
                                <td> {{ average }} </td>
                                <td> {{ max }} </td>
                            </tr>
                        </table>
                    </div>
                    
                    <div>
                        <img src= "{{ image }}">
                    </div>
                </body>
                </html>
                """

error_page = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Something went wrong</title>
                </head>
                <body>
                    <div><h1>Wrong details </h1></div>
                    <div><p>Something went wrong<p></div>
                </body>
                </html>
                """
def something_went_wrong():
    with open("./output.html", "w") as outfile:
        with Flask(__name__).app_context():
            outfile.write(render_template_string(error_page))

def main():
    data = []
    total = 0
    args = sys.argv

    try:
        if len(args) == 3:
            if args[1] == "-s":
                with open("data.csv") as infile:
                    for line in infile:
                        content = line.rstrip().split(",")
                        if content[0] == args[2]:
                            data.append(content)
                            total += int(content[2])
                if len(data) == 0:
                    something_went_wrong()
                    sys.exit()

                with open("./output.html", "w") as outfile:
                    with Flask(__name__).app_context():
                        outfile.write(render_template_string(student_data_page, data=data, total=total))

            elif args[1] == "-c":
                with open("data.csv") as infile:
                    for line in infile:
                        content = line.rstrip().split(",")
                        if content[1].lstrip() == args[2]:
                            total += int(content[2])
                            data.append(int(content[2]))
                if len(data) == 0:
                    something_went_wrong()
                    sys.exit()

                fig, ax = plt.subplots()
                ax.hist(data)
                ax.set_xlabel('Marks')
                ax.set_ylabel('Frequency')
                fig.savefig("./hist.png")

                with open("./output.html", "w") as outfile:
                    with Flask(__name__).app_context():
                        outfile.write(render_template_string(course_page, average=total/len(data), max=max(data), image="./hist.png"))
            else:
                something_went_wrong()

    except Exception:
        something_went_wrong()

if __name__ == '__main__':
    main()