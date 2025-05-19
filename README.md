See [wiki](../../wiki)!
DO NOT USE NEWEST COMMIT IT DOES NOT WORK
no time to complete the restructuring but check  
version: https://github.com/CYix1/WSSGTemplate/commit/0d4fe25a1bebddac6eb8719a067e7d82ce3e1885
IMPORTANT THE CURRENT VERSION USES POSTGRES 
To change it back, set the values correct e.g used_databases
delete all migrations 
`python manage.py makemigrations`
`python manage.py migrate`
And check again with the admin panel e.g 127.0.0.1:8000/admin/
  
RESTRUCTURING ONGOING!!!!!!! 

TODO (checking if it works)
REST:
- [] GET SET stuff
- [] Friendship
- [] Leaderboard
- [] Lobby/Tictactoe

WS:
- [] Chat
- [] Leaderboard
- [] Tictactoe
