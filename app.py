from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os

app = Flask(__name__)

# Define your Docker container name
DOCKER_CONTAINER_NAME = 'frappe_app'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        site_name = request.form['site_name']
        directory = 'sites'
        file_name = f"{site_name}.txt"
        # Combine the directory and file name into a full file path
        file_path = os.path.join(directory, file_name)

        # Check if the file exists
        if os.path.exists(file_path):
            return f"<center style='margin:20px;'>Site name {site_name} is already used. <a href='/'>Try another one!</a></center>"
        else:
            # Validate site name
            if not site_name or not site_name.isalnum():
                return "Invalid site name. Please use only alphanumeric characters.", 400
        
            # Run the bash script to set up Frappe Docker
            command = f'./setup_frappe.sh {site_name}'
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                return f"Error occurred: {e}", 500
        
            return redirect(url_for('select_apps', site_name=site_name))
    
    return render_template('index.html')

@app.route('/select_apps/<site_name>', methods=['GET', 'POST'])
def select_apps(site_name):
    if request.method == 'POST':
        selected_apps = request.form.getlist('apps')
        skip_install = 'skip_install' in request.form
        
        if not skip_install and not selected_apps:
            return "No apps selected. Please choose at least one app or skip installation.", 400
        
        if not skip_install:
            # Run the bash script to install the selected apps in the Docker container
            command = f'./install_apps.sh {DOCKER_CONTAINER_NAME} {site_name} {" ".join(selected_apps)}'
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                return f"Error occurred: {e}", 500
        
        return redirect(url_for('site', site_name=site_name))
    
    return render_template('select_apps.html', site_name=site_name)

@app.route('/site/<site_name>')
def site(site_name):
    # Open the file in read mode
    with open(f'sites/{site_name}.txt', 'r') as file:
        # Read the contents of the file
        contents = file.read()

    return f"""<center><h1>Congrats!</h1>
    <br>Your ERP System {site_name} is up and running at <a href='http://localhost:{contents}'>http://localhost:{contents}</a>
    <br><a href='{url_for('manage', site_name=site_name)}'>Manage this Site</a></center>"""

@app.route('/manage/<site_name>', methods=['GET', 'POST'])
def manage(site_name):
    if request.method == 'POST':
        action = request.form.get('action')
        selected_apps = request.form.getlist('apps')
        
        # Determine which action to perform
        if action == 'migrate':
            command = f'./migrate.sh {site_name}'
        elif action == 'backup':
            command = f'./backup.sh {site_name}'
        elif action == 'install':
            if not selected_apps:
                return "No apps selected. Please choose at least one app.", 400
            command = f'./install_apps.sh {DOCKER_CONTAINER_NAME} {site_name} {" ".join(selected_apps)}'
        elif action == 'clear_cache':
            command = f'./clear_cache.sh {site_name}'
        else:
            return "Invalid action.", 400

        # Run the corresponding bash script
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            return f"Error occurred: {e}", 500

        return redirect(url_for('site', site_name=site_name))
    
    return render_template('manage.html', site_name=site_name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
