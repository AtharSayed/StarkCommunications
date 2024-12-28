Chat application (StarkComm)

--> Project Structure :

chat_app/
├── app.py                      
├── templates/                  
│   ├── chat.html              
│   ├── login.html              
│   └── signup.html             
├── static/                     
│   ├── css/                    
│   │   └── style.css          
│   ├── images/                 
│   │   ├── logo.png            
│   │   ├── background.jpg      
│   └── js/                    
│       ├── main.js            
│       └── script.js           
└── README.md                     



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

7) WebSocket's is used for message exchange between the users 
  Since WebSocket's provide the functionality of bidirectional message exchange between the two entities or multiple entities 


--> Technologies Used :

1) Python (Flask)

2) HTML, CSS

3) JavaScript 


--> Databases Used :

1) Mongodb 

