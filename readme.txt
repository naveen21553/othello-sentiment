To run:
python othello-sentiment.py -f othello.fasta 

optional args
-A for act {1, 5}
-S for scene {1, 4}
-C for Character

Scene Breakdown
Act 1: 3 Scenes
Act 2: 3 scenes
Act 3: 4 Scenes
Act 4: 3 Scenes
Act 5: 2 Sceens

** Scene argument won't be accepted without Act Argument **

Characters in Othello 
'othello','desdemona','iago','michael cassio','emilia', 
'roderigo','bianca','brabanzio','montano','lodvico','graziano', 
'clown','duke of venice'

Example:
python othello-sentiment.py -f othello.fasta -C emilia
python othello-sentiment.py -f othello.fasta -A 2
python othello-sentiment.py -f othello.fasta -A two
python othello-sentiment.py -f othello.fasta -A II
python othello-sentiment.py -f othello.fasta -A 2 -S 1

## Full Play
<img src=https://github.com/naveen21553/othello-sentiment/blob/master/FULL%20Play.png/>

## Full Play for Emilia
<img src=https://github.com/naveen21553/othello-sentiment/blob/master/Full%20Play%20for%20Emilia.png/>
