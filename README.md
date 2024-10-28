Chat application (StarkComm)

--> Project Structure :

chat_app/
├── app.py                      # Main application
├── templates/                  # HTML templates
│   ├── index.html              # Chat interface
│   ├── login.html              # User login page
│   └── signup.html             # User sign-up page
├── static/                     # Static files
│   ├── css/                    # CSS files
│   │   └── style.css           # Stylesheet
│   ├── images/                 # Image files
│   │   ├── logo.png            # Example logo 
│   │   ├── background.jpg      # Example background image 
│   └── js/                     # JavaScript files
│       ├── main.js             # Main JavaScript file
│       └── script.js           # Additional JavaScript file
└── README.md                   # Project documentation



--> How to Run :

1) Run the app.py file and click on the url from the terminal window which will open a browser on localhost port 5000

2) If You are registered before on the application use that credentials otherwise go to the sign up page and create a new username and password 

3) Open the mongodb Compass and connect to the database and see the 2 collections named messages and users created under the database named chat 


--> Features of the project : 

1)  Chat room UI for convenience using chatting 

2) Sign up pages for new users to register and use the chat application 

3) Login page for existing users to use the applications at  any time 

4) Facilitate techniques for many users to communicate at the same time 

5) Instead of redirecting the invalid credentials to the next page displaying it on the same page to the user below the password coloumn 

6) Forcing users to create strong passwords using different symbol combinations 


--> Technologies Used :

1) Python (Flask)

2) HTML, CSS

3) JavaScript 


--> Databases Used :

1) Mongodb 

