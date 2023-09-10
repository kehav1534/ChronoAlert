from flask import Flask, render_template, request, redirect, url_for
import json
import webbrowser
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def Home():
    if request.method=="GET":
        with open("notification.json", "r") as file:
                data = json.load(file)
                file.close()
        code = ""
        for noti in data:
            code += f"""
                    <h3 style="font-weight:normal;">{noti["title"]}</h3><p>{noti["message"]}</p>
                    <!-style='display:flex; justify-content:space-between;'->
                    <div style='display:flex; justify-content:left;'>
                        <button id="showInputBtn" action="/Gdrive" method="post" style="background-color:grey"> Edit </button>
                        <span style ='width:20px'></span>
                        <form method='POST' action='/'>
                        <button id="delBtn" name='nid' value='{noti["nid"]}' action="/" method="POST" style="background-color:red">Delete</button>
                        </form>
                    </div><hr><br>"""
        return render_template("ChronowebApp.html", data=code)
            
    if request.method == 'POST':
        btn_value = int(request.form.get('nid'))
        with open("notification.json", "r") as file:
            data = json.load(file)
            file.close()
            
            for n in data:
                if n["nid"] == btn_value:
                    data.remove(n)
                with open("notification.json", "w") as json_file:
                    json.dump(data, json_file, indent=6)
        return redirect(url_for('Home'))
    

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    render_template()


if __name__ == "__main__":
    
    app.run(port=45296)
    webbrowser.open('http://localhost:45296')
    
