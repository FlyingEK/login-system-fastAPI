# oyen-assessment

# STEPS TO SET UP AND RUN

# Download the project code using zip file or git clone

# Set up virtual environment in command prompt
Step 1: Install virtual environment:<br>
Run "pip install virtualenv"<br>
<br>
Step 2: Navigate to the project directory<br>
Run "cd <directory -path>"<br>
<br>
Step 3: Use the venv<br>
Run "python'<version>' -m venv '<virtual-environment-name>'"<br>
e.g:  python3 -m venv env<br>
<br>
Step 4: Activate the venv<br>
For Windows, Run ".\env\Scripts\activate"<br>
For Mac/Linus, Run "source env/bin/activate"<br>
<br>
Step 5: Install the dependencies<br>
Run "pip install -r backend\requirements.txt"<br>

# Run the project
Step 1: run "uvicorn backend.main:app --reload"
Step 2: open browser and go to "http://127.0.0.1:8000/"
2.1 enter login credentials, Username = username1, Password = password1
2.2 click login
Step 3: open browser and go to "http://127.0.0.1:8000/docs"
3.1 Click authorize button on top right corner
3.2 Enter login credentials stated in 2.1
3.3 Expand POST /user
3.4 Click "try it out" button in the parameter tab and click "execute"
3.5 The response will show the user details 
(This shows that the authentication token can be used to retrieve the logined user details; authenticate them before accessing to protected page by checking if the user details are not empty)




