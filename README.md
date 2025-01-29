# UOD MESSENGER APPLICATION 
#### Made by 100715281

## Architectures
- CS - Asynchronous Bi-directional communication between client & server - MAIN APPLICATION
- P2P - Asynchronous Bi-directional communication between clients - CALLING 



## Application 
### How to use
- Run Setup "setup_environment.bat"
- Run Server.py "py .\Server\Server.py"
- Run Client.py "py .\client\MainWindow.py"

### Using the application - You can
- Login or Register
- Get & View contacts they've saved

- Open chat with a contact
	- View everything sent previously & send more messages
	- Receive live messages from other participant 

- Add a new contact
	- Search for contacts name
	- Select from results which contact to add

- Call saved contact
	- Can call a saved contact.
	- Is a dial in system, if two participants dial in, will be put into a call session
	- sending and receiving audio data

- Broadcasting (if premium member)
	- If authorised, users can send broadcast messages - (must be premium members)


## More details



### GUI
- Uses PYQT6 for generating window and handling users UI & UX

### Contact calling
UDP - P2P:
- Dial into call with a contact - Works if other contact is online 
- Server sends IP of clients, caller will use this IP to establish P2P connection 
- Clients begins sends audio messages using User-Datagram UDP packets. Directly to client



## Authentication
### LOGIN
- User can submit to server login details (username, password)
- Server will check the database to determine if this account is valid
- If not successful, server will inform client on mistakes and clients application will present this


### REGISTER
- User can submit to server registered details (Email, username, password)
- Server will determine if account is already registered under the email and or username given
- If not successful, server will inform client on mistakes and clients application will present this

On success of authentications, client will proceed to main application.

### ACCOUNT LOCKING
- If someone fails login attempt so many times, will lock account and send email (warning)
### LOGGING IN AT DIFFERENT LOCATION
- Will send email to user if they log in at a different location (warning)


## Database
- Uses SQLlite 3
- Tables:
	- Messages - Entity
	- Accounts - Entity
	- Contacts - Relationship
- Can make changes, through running the database file directly. (Will run DDL SQL commands)

## Encryption & Cryptography
- RSA Encryption
## Keys share
- Is asynchronous - Private key is never shared, When communication channel is setup (socket) nodes will ask for the others public key to encrypt data to send to them


## Connecting
### Reconnecting
- Once lost connection with server, clients will keep reattempting to connect - once got response will do keyshare and login again automatically
### Disconnecting
- When closing will send "Exit" to server
- Server also uses a "still there" test 

## Broadcasting
- Authorised users can use broadcast feature to send message for everyone to see on home page

## Storing Cache Of Credentials
- When login or register is successful, will store these details for reuse when application restarts (on client side)

## Frame Segmenting
- Splits packet/frame into segments/chunks for effective & optimal use of RSA encryption

## Emailing
- Welcome when creating account
- Warning, "you have logged in at a different location"
- Warning, "you have been locked out you're account - someone is attempting to get in"

## Defending against attacks
REPLAY ATTACK DEFENCE:
	- attaches unique ID to packet which server will keep track of once received. If this unique packet has been resent WILL IGNORE AND OUTPUT "THIS IS A REPLAY ATTACK"

## Premium accounts
- Allowed to send broadcast messags
- If put valid code in on register, will be accepted as a premium member




