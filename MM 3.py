from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, 
from mindstorms.control import wait_for_seconds
#from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
#import math
import random

# Create your objects here.
hub = MSHub()
#app = App()

y_motor = MotorPair('A', 'B')
a_motor = Motor('A')
b_motor = Motor('B')
x_motor = Motor('D')
pick_motor = Motor('C')
color_sensor = ColorSensor('F')
distance_sensor = DistanceSensor('E') #sostituisce touch_sensor

#settings
y_motor.set_default_speed(-80)   # num positivo va in fondo - negativo verso il giocatore
y_motor.set_stop_action('coast')
x_motor.set_default_speed(100)
x_motor.set_stop_action('coast')
pick_motor.set_default_speed(25)
hub.speaker.set_volume(100)


def test(cp,c_ft): #confronta due combinazioni e ritorna il ch
    ch_test=[0,0]
    bn=0 #bianchi + neri
    neri=0
    for i in range(5, 11): #prendi il minor numero di volte che un colore è presente
        if cp[i] < c_ft[i]:
            bn=bn+cp[i]
        else:
            bn=bn+c_ft[i]
    for i in range(0,4): #calcola il numeri di neri
        if cp[i]==c_ft[i]:
            neri += 1
    ch_test[0]=bn-neri #calcola i bianchi per differenza
    ch_test[1]=neri
    return ch_test

def popola_bc(ft,db,db_ft,db_bc):
    min = 9999
    db_bc=[]
    for i in range (0,ft): #ripeti per tutti gli ft
        ch_hit=[]
        for a in range (0,5):
            ch_hit.append([0,0,0,0,0])
        for j in range (0,ft):
            ch_test=test(db_ft[i], db_ft[j]) #trova ch tra i cp e i possibili cs
            ch_hit[ch_test[0]][ch_test[1]] +=1 #incrementa le ricorrenze di ch uguali
        max=0
        for x in range(0,5): #trova il valore massimo in ch_hit
            for y in range(0,5):
              if ch_hit[x][y] > max:
                 max = ch_hit[x][y]
        db_ft[i][11] = max #assegna max al cp
        if max < min: # assegna a min il minore tra i max
            min = max
    flag=False #flag diveta true se c'è almeno un ft in db_bc
    for i in range (0,ft):
        if db_ft[i][11] == min:
            db_bc.append(db_ft[i])
    return db_bc #crea il db dei bc dalla prima giocata e le successive


def go (px, py):
  global x_current_pos, y_current_pos
  y_motor.move_tank((py-y_current_pos)/10)
  y_current_pos = py
  x_motor.run_for_rotations(-(px-x_current_pos)/100)
  x_current_pos = px
      
def pick ():
  drop=83
  pick_motor.run_for_rotations(drop/100, speed=30)
  pick_motor.run_for_rotations(-drop/100)
  #distance_sensor.wait_for_distance_closer_than(10, 'cm')

def release ():
  drop1=20
  drop2=30
  pick_motor.run_for_rotations(drop1/100, speed=40)
  pick_motor.run_for_rotations(drop2/100, speed=30)
  #distance_sensor.wait_for_distance_closer_than(10, 'cm')
  pick_motor.run_for_rotations(-(drop1+drop2)/100)
  
def reset_position():
  pick_motor.start_at_power(-50)
  wait_for_seconds(0.2)
  while pick_motor.get_speed() <0:
    wait_for_seconds(0.2)
  pick_motor.stop()
  y_motor.start_at_power(60)
  #global y_current_pos
  wait_for_seconds(0.2)
  while a_motor.get_speed() !=0 and b_motor.get_speed !=0 :
     #print (y_motor.get_default_speed())
     wait_for_seconds(0.2)
  y_motor.stop()
  x_motor.start_at_power(50)
  wait_for_seconds(0.2)
  while x_motor.get_speed() >0:
    #print (x_motor.get_speed())
    wait_for_seconds(0.2)
  x_motor.stop()

  
 
def scan_keycode(): #Scan with color sensor the key code 
  global bianchi
  global neri
  bianchi=0
  neri=0
  px0=350
  py0=1000
  go (px0,py0)
  delta_x=70
  delta_y=110
  px=[px0, px0+delta_x, px0+delta_x, px0  ]
  py=[py0, py0, py0+delta_y, py0+delta_y]
  drop=40
  pick_motor.run_for_rotations(drop/100, speed=30)
  color_sensor.get_color()
  for i in range(0, 4): 
      go(px[i],py[i])
      print (color_sensor.get_color())
      if str(color_sensor.get_color()) == "None":
        wait_for_seconds(0.1)
      if str(color_sensor.get_color()) == "white":
        bianchi=bianchi+1
      if str(color_sensor.get_color()) == "black":
        neri=neri+1
      #distance_sensor.wait_for_distance_closer_than(10, 'cm')
  pick_motor.start_at_power(-50)
  wait_for_seconds(0.1)
  while pick_motor.get_speed() <0:
    wait_for_seconds(0.2)
  pick_motor.stop()
  ch=[]
  ch.append(bianchi)
  ch.append(neri)
  return ch

def go_pick(px,py): #Converte coordinate px,py in coordinate per EV3. poi chiama go(px,py) e pick()
  px=286+(px-1)*(490-286)/5
  py=33+(py-1)*(710-33)/9
  go(px,py)
  pick()

def go_rel(px,py): #Converte coordinate px,py in coordinate per EV3. Poi chiama go(px,py) e release()
  px=13+(px-1)*(136-13)/3
  py=46+(py-1)*(848-46)/9
  go(px,py)
  release()

def tuning0():
  
  go_pick (1,1) 
  go_rel (1,1) 

  go_pick (2,2) 
  go_rel (2,2)

  go_pick (3,3)
  go_rel (3,3)

  go_pick (4,4)
  go_rel (4,4)

  go_pick (5,5)
  go_rel (1,5)

  go_pick (6,6)
  go_rel (2,6)
  

  go_pick (5,7)
  go_rel (3,7)

  go_pick (4,8)
  go_rel (4,8)

  go_pick (3,9)
  go_rel (1,9)
  
  go_pick (2,10)
  go_rel (2,10)

  

def color_to_play(color): #Trova il primo piolo di colore color disponibile. Poi chiama go_pick()
  #next_peg contiene la posizione del primo piolo disponibile per ogni colore
  next_peg[color]=next_peg[color]+1
  #print ("next_peg ",next_peg)
  px=color
  py=next_peg[color]
  go_pick(px,py)

def play_code(board_row,cp):
  for column in range (1,5):
    color_to_play(cp[column-1]) #prende il peg di cp in posizione da 0 a 3
    go_rel(column,board_row)


def tuning1(): #Sequenza di presa/rilascio pioli usando color_to_play() e go_rel()
  print ("ok")
  color_to_play(1)
  go_rel(1,1)

  color_to_play(2)
  go_rel(2,1)

  color_to_play(1)
  go_rel(3,1)

  color_to_play(3)
  go_rel(4,1)
 
  color_to_play(1)
  go_rel(1,2)

  color_to_play(2)
  go_rel(2,2)

  color_to_play(1)
  go_rel(3,2)

  color_to_play(3)
  go_rel(4,2)

def new_guess (cp_board, ch_board, board_row):  
    for d in range(1, 7):
      for e in range(1, 7):
        hub.light_matrix.show_image("CLOCK"+str((e-1)*2+1))
        hub.speaker.beep(60, 0.1)
        #wait_for_seconds(0.1)
        hub.light_matrix.show_image("CLOCK"+str((e-1)*2+2))
        for b in range(1, 7):
          for c in range(1, 7):
            cp = [d,e,b,c,True,0,0,0,0,0,0,0]
            cp[4 + cp[0]] += 1 #inizializza 6 campi, uno per colore con il numero di volte che il colore è presente
            cp[4 + cp[1]] += 1
            cp[4 + cp[2]] += 1
            cp[4 + cp[3]] += 1
            cp_ok=True
            for i in range(0, board_row-1):
                    #print ("cp g",cp)
                    #print ("cp_board [i] g", cp_board[i])
                    ch=test(cp,cp_board[i])
                    """
                    print ("========")
                    print ("cp", cp)
                    print ("cp_board i", cp_board[i])
                    print ("ch", ch)
                    print ("ch_board i", ch_board[i])
                    """
                    if ch!=ch_board[i]:
                        cp_ok=False
            if cp_ok==True:
                hub.light_matrix.off()
                return cp



wait_for_seconds(7)
reset_position()
x_current_pos=0
y_current_pos=0


"""
#hub.status_light.off()
hub.light_matrix.off()
#hub.light_matrix.show_image('HAPPY')
#wait_for_seconds(3)
#hub.light_matrix.show_image(CLOCK1, brightness=100)
for i in range (1, 13):
  clock= "CLOCK"+str(i)
  hub.light_matrix.show_image(clock)
  wait_for_seconds(0.2)
#next_peg=[0,0,0,0,0,0,0,] #mantiene il primo peg disponibile per ogni colore
tuning0()
#tuning1()
#ch=scan_keycode()
#print (ch)
go (0,0)
"""


while True:
    print ("Inserisci il Codice Segreto e premi il pulsante")
    #distance_sensor.wait_for_distance_closer_than(10, 'cm')
    #wait_sensor_pressed()
    #say scegli e nascondi il CS e poi pigia il bottone
    board_row=0
    ch_board=[]
    cp_board=[]
    next_peg=[0,0,0,0,0,0,0,] #mantiene il primo peg disponibile per ogni colore
    reset_position()
    x_current_pos=0
    y_current_pos=0
    while board_row < 11: #al massimo 10 codici tentativo
        board_row +=1
        print ("----------------")
        print ("board_row", board_row)
        if board_row ==1:
            cp=[1,4,2,5,True,0,0,0,0,0,0,0]
            cp[4 + cp[0]] += 1 #inizializza 6 campi, uno per colore con il numero di volte che il colore è presente
            cp[4 + cp[1]] += 1
            cp[4 + cp[2]] += 1
            cp[4 + cp[3]] += 1
        else:
            cp=new_guess(cp_board, ch_board, board_row )

        cp_board.append(cp)
        print ("cp_board")
        for temp in cp_board:
          print(temp)
               
        play_code (board_row,cp)
        
        if board_row == 4:
          break

        print ("inserisci il Codice Chiave e premi il pulsante")    
        distance_sensor.wait_for_distance_closer_than(10, 'cm')
        #pressed=wait_sensor_pressed()
        ch=scan_keycode() #human inserisce il ch
        print ("ch ", ch)
        if ch[1]==4: #se inserisce 4 neri il cs è indovinato
            print ("codice indovinato")
            break
        ch_board.append(ch)
        print ("ch_board")
        for temp in ch_board:
          print(temp)
        
    hub.light_matrix.show_image('HAPPY')
    go (70,1070)
    drop=25
    pick_motor.run_for_rotations(drop/100, speed=30)
    #go (70,800)  #distance_sensor.wait_for_distance_closer_than(10, 'cm')
    go (0,0)
    pick_motor.run_for_rotations(-drop/100)
    print ("Premi il pulsante per un'altra partita")
    distance_sensor.wait_for_distance_closer_than(10, 'cm')
    #wait_sensor_pressed()
    go(0,0)



"""
distance_sensor.wait_for_distance_closer_than(10, 'cm')
#distance_sensor.wait_for_distance_closer_than(10, 'cm')   

#wait_for_seconds (4)
#x_motor.set_stall_detection(True)
#y_motor.move(2, 'seconds')
# Allow the motors to turn freely after stopping.
distance_sensor.light_up_all(brightness=100)
#app.play_sound('Laughing Girl', volume=70)
wait_for_seconds(2)
distance_sensor.light_up_all(0)
#distance_sensor.light_up_all(brightness=100)
#distance_sensor.light_up_all(0)
"""


