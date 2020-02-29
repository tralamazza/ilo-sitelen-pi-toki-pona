# import the pygame module, so you can use it
import os
import sys
import re
import json

if len(os.path.dirname(sys.argv[0]))>0:
	os.chdir(os.path.dirname(sys.argv[0]))

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["DISPLAY"]=":0"

import pygame

#KEYMAP
#
# 49, 50, 51, 52, 53, 54
# 113, 119, 101, 114, 116, 122 
# 97, 115, 100, 102, 103, 104
# 112, 120, 99, 118, 98
#

SCALE = 2

s_w = 800
s_h = 480

eingabewort=""

keyname = {
	49: "links",
	50: "oben",
	51: "rechts",
	52: ":",
	53: "\"",
	54: "\t",

	113: "ende",
	119: "unten",
	101: "MIJ",
	114: "SEN",
	116: "L",
	122: "rücktaste",

	97: "anfang",
	115: ",",
	100: "TOK",
	102: "PA",
	103: "WU",
	104: " ",

	304: "pali",#  MOD = 1 for shiftb
	120: ".",
	99: "!",
	118: "?",
	98: "\n",

}

interpunktion_codes = {
	52: ":",
	53: "\"",
	115: ",",
	120: ".",
	99: "!",
	118: "?",

}

def kk_seiAlpha(kk):
	return kk==101 or kk==114 or kk==116 or kk==100 or kk==102 or kk==103


def kk_wortEnde(kk):
	return kk==104 

def kk_Interpunktion(kk):
	return kk==52 or kk==53 or kk==115 or kk==120 or kk==99 or kk==118 

def kk_Cursorbewegung(kk):
	return kk==49 or kk==50 or kk==51 or kk==113 or kk==119 or kk==97

def kk_Formatting(kk):
	return kk==54 or kk==98 or kk ==122


v_Position=0



blatt_idx=0

cursor_x=0;
cursor_y=0;
cursor_str=""

blätter = []

wörter = [
	["a","kin"],
	["akesi"],
	["ala","ale"],
	["alasa"],
	["ali"],
	["anpa"],
	["ante"],
	["anu"],
	["awen"],
	["e"],
	["en"],
	["esun"],
	["ijo"],
	["ike"],
	["ilo"],
	["insa"],
	["jaki"],
	["jan"],
	["jelo"],
	["jo"],
	["kala"],
	["kalama"],
	["kama"],
	["kasi"],
	["ken"],
	["kepeken"],
	["kili"],
	["kiwen"],
	["ko"],
	["kon"],
	["kule"],
	["kulupu"],
	["kute"],
	["la"],
	["lape"],
	["laso"],
	["lawa"],
	["len"],
	["lete"],
	["li"],
	["lili"],
	["linja"],
	["lipu"],
	["loje"],
	["lon"],
	["luka"],
	["lukin","oko"],
	["lupa"],
	["ma"],
	["mama"],
	["mani"],
	["meli"],
	["mi"],
	["mije"],
	["moku"],
	["moli"],
	["monsi"],
	["mu"],
	["mun"],
	["musi"],
	["mute"],
	["nanpa"],
	["nasa"],
	["nasin"],
	["nena"],
	["ni"],
	["nimi"],
	["noka"],
	["o"],
	["olin"],
	["ona"],
	["open"],
	["pakala"],
	["pali"],
	["palisa"],
	["pan"],
	["pana"],
	["pi"],
	["pilin"],
	["pimeja"],
	["pini"],
	["pipi"],
	["poka"],
	["poki"],
	["pona"],
	["pu"],
	["sama"],
	["seli"],
	["selo"],
	["seme"],
	["sewi"],
	["sijelo"],
	["sike"],
	["sin","namako"],
	["sina"],
	["sinpin"],
	["sitelen"],
	["sona"],
	["soweli"],
	["suli"],
	["suno"],
	["supa"],
	["suwi"],
	["tan"],
	["taso"],
	["tawa"],
	["telo"],
	["tenpo"],
	["toki"],
	["tomo"],
	["tu"],
	["unpa"],
	["uta"],
	["utala"],
	["walo"],
	["wan"],
	["waso"],
	["wawa"],
	["weka"],
	["wile"]
]

alleWörter = [item for sublist in wörter for item in sublist]

def buchstabe_zu_kk(bs):
	if "mij".find(bs)>=0:
		return "m"#101
		
	if "sen".find(bs)>=0:
		return "s"#114
		
	if "l".find(bs)>=0:
		return "l"#116
		
	if "tok".find(bs)>=0:
		return "t"#100
		
	if "pa".find(bs)>=0:
		return "p"#102
		
	if "wu".find(bs)>=0:
		return "w"#103
	
	return -1


decknamen={}
for w in alleWörter:
	deckname = "".join(list(map(buchstabe_zu_kk,w)))
	decknamen[deckname]=w

alle_decknamen=decknamen.keys()

def wurzelzahl(wurzel):
	zahl=0
	ziel=""
	for deckname in alle_decknamen:
		if wurzel==deckname[:len(wurzel)]:
			zahl=zahl+1
			ziel=deckname
	return (zahl,ziel)


def wortIndex(w):
	for idx,toks in enumerate(wörter):
		if w in toks:
			return (0,idx)
	
	
	p_idx = interpunktuationzeichen.find(str(w))
	if p_idx>=0:
		return (1,p_idx)

	if w=="\t":
		return (2,0)

	return (-1,-1)

def lade_globalen_Zustand():
	global blatt_idx

	dname="lipu/zustand.cfg"
	if (os.path.isfile(dname)):
		with open("lipu/zustand.cfg", "r") as f:
			zustand = json.load(f)
			print(zustand)
			blatt_idx=int(zustand['blatt_idx'])
	else:
		blatt_idx=0


def speichere_globale_Daten():
	global blatt_idx
	zustand={
		'blatt_idx':blatt_idx
	}
	with open("lipu/zustand.cfg", "w") as f:
		json.dump(zustand, f)


buchstaben="aeioujklmnpstw"
interpunktuationzeichen=".,:-?!'\"[]“”"
leerzeichen="\t"

zeichen_pro_zeile=19
bildschirm_zeilen=12

def parse_rohe_Datei(rohe):
	global zeichen_pro_zeile

	rohe=rohe.lower()

	toks = re.findall(r"(\w+|\.|\,|\:|\-|\?|\!|\'|\"|\[|\]|\“|\”|\n|\t)", rohe)



	splittoks=[]
	zeichen_index=0

	zeile=[]
	splittoks.append(zeile)

	for t in toks:
		if t=="\n":
			zeichen_index=0
			zeile=[]
			splittoks.append(zeile)
		else:
			idx = wortIndex(t)[0]
			if idx==-1:
				print("couldn't process token '"+t+"'.")
				#zeile.append(idx)

			zeile.append(t)

			zeichen_index=zeichen_index+1
			if zeichen_index>=zeichen_pro_zeile:
				zeile=[]
				zeichen_index=0
				#zeile.append("\t")
				#zeichen_index=1
				splittoks.append(zeile)
	
	del splittoks[0][8:]


	return splittoks



def speicheren_Datei(n):
	global blätter
	print("saving")

	if n<0 or n>=len(blätter):
		return

	blatt=blätter[n]
	datei_name="lipu/"+str(n)+".txt"

	print("saving stuff to",datei_name)
	def fuse_Linie(l):
		return " ".join(l)
	linien=map(fuse_Linie,blatt)
	dateistr = "\n".join(linien)
	f=open(datei_name,'w')
	f.write(dateistr)
	f.close();

def lade_Datei():
	global blätter

	rohe_datein=[]

	i=0
	while os.path.isfile("lipu/"+str(i)+".txt"):		
		filename = "lipu/"+str(i)+".txt";
		with open(filename,"r") as f:
			datei_str = f.read()
			rohe_datein.append(datei_str)
		i=i+1

	blätter = list(map(parse_rohe_Datei,rohe_datein))


def zeiche_Cursor(bildfläche,zeichen):
	global cursor_x
	global cursor_y

	t_x = 20*cursor_x + 1
	t_y = 20*(cursor_y - v_Position) + 1

	zeichen.set_clip(SCALE*0,SCALE*252,SCALE*20,SCALE*20)
	draw_me = zeichen.subsurface(zeichen.get_clip())

	bildfläche.blit(draw_me,(SCALE*(t_x-1),SCALE*(t_y-1)))

def zeiche_Cursorinhalt(bildfläche,zeichen):
	global cursor_x
	global cursor_y
	global SCALE
	global eingabewort
	global zeichen_sm

	if len(eingabewort)==0:
		return

	t_x = 20*cursor_x + 1
	t_y = 20*(cursor_y - v_Position) + 1

	r = pygame.Rect(SCALE*t_x,SCALE*t_y,SCALE*18,SCALE*18)

	BLACK = (0,0,0)
	#WHITE = (255,255,255)

	bildfläche.fill(BLACK,r)

	for i,b in enumerate(eingabewort):
		
		(dy,dx) = divmod(i,3)
		z_x=t_x+1+6*dx
		z_y=t_y+1+9*dy

		zeichen_idx = "mpsltw".find(b)

		zeichen_sm.set_clip(36+(18*zeichen_idx),252,8,15)
		draw_me = zeichen_sm.subsurface(zeichen_sm.get_clip())

		bildfläche.blit(draw_me,(SCALE*(z_x),SCALE*(z_y)))


	#pygame.draw.rect(bildfläche,WHITE,r,SCALE)



def zeiche_Zeile(bildfläche,zeichen,s,pos):
	global SCALE

	t_x=(20*pos[0]+1)
	t_y=(20*pos[1]+1)

	for i,z in enumerate(s):
		if z=="\t":
			t_x=(t_x+20)
			continue

		idx = wortIndex(z)
		
		s_x = idx[1] % 12
		s_y = int(int(10*idx[0])+(int(idx[1]) / int(12)))

		zeichen.set_clip(SCALE*18*s_x,SCALE*18*s_y,SCALE*18,SCALE*18)
		draw_me = zeichen.subsurface(zeichen.get_clip())

		bildfläche.blit(draw_me,(SCALE*t_x,SCALE*t_y))
		t_x=(t_x+20)



def zeiche_Bild(bildfläche,hg,zeichen):
	global bildschirm_zeilen
	global SCALE
	global v_Position

	bildfläche.blit(hg, (0,0))
	
	blatt = blätter[blatt_idx]
	
	seite_pos=(0,0)
	

	for i in range(bildschirm_zeilen):
		l = v_Position+i;
		if l>=len(blatt):
			break

		print("l",l)
		print("len(blatt)",len(blatt))
		zeiche_Zeile(bildfläche,zeichen,blatt[l],(seite_pos[0],seite_pos[1]+i))

	zeiche_Cursor(bildfläche,zeichen)

	oberste_zeile=v_Position
	unterste_zeile=v_Position+bildschirm_zeilen-1

	aktuelles_blatt = blätter[blatt_idx]


	pixel_oberste = 7
	pixel_unterste = 240-7

	sichtbares_prozent =  float(bildschirm_zeilen) /  max(float(len(aktuelles_blatt)),float(bildschirm_zeilen))

	stabgröße = int((pixel_unterste-pixel_oberste+1)*sichtbares_prozent)

	fortschritt_prozent = v_Position/max(v_Position, max(len(aktuelles_blatt)+1-bildschirm_zeilen,1) )
	stab_y_min = pixel_oberste
	stab_y_max = pixel_unterste-stabgröße
	stab_y = stab_y_min+(stab_y_max-stab_y_min)*fortschritt_prozent

	r_x=387
	r_w=6
	r = pygame.Rect(2*r_x,2*stab_y,2*r_w,2*stabgröße)

	#BLACK = (0,0,0)
	WHITE = (255,255,255)

	bildfläche.fill(WHITE,r)
	#pygame.draw.rect(bildfläche,WHITE,r,SCALE)

	zeiche_Cursorinhalt(bildfläche,zeichen)

	pygame.display.flip()    


def beenden():
	pygame.quit()
	sys.exit()


def fitCursor():
	global cursor_x
	global cursor_y
	global blatt_idx
	global blätter
	global v_Position

	höchst_sichtbare_reihe = v_Position
	niedrigst_sichtbare_reihe = v_Position+bildschirm_zeilen-1

	if cursor_y>niedrigst_sichtbare_reihe:
		v_Position=v_Position+1
	elif cursor_y<v_Position:
		v_Position=cursor_y

	if v_Position<0:
		v_Position=0



def machCursorbewegung(kk,kmod):	
	global cursor_x
	global cursor_y
	global blatt_idx
	global blätter
	global v_Position
	global eingabewort

	eingabewort=""

	aktuelles_blatt = blätter[blatt_idx]


	if kk==49:#links
		if kmod==1:			
			cursor_x=0
		else:
			if cursor_x==0:
				if cursor_y>0:
					cursor_y=cursor_y-1;
					aktuelle_zeile = aktuelles_blatt[cursor_y]

					cursor_x=len(aktuelle_zeile)

					if cursor_x==zeichen_pro_zeile:
						cursor_x=cursor_x-1
			else:
				cursor_x=cursor_x-1

	elif kk==50:#oben
		if cursor_y>0:
			if kmod==0:
				cursor_y=cursor_y-1
			else:
				diff = cursor_y-v_Position

				cursor_y=cursor_y - bildschirm_zeilen
				if cursor_y<0:
					cursor_y=0

				v_Position=cursor_y-diff
				if v_Position<0:
					v_Position=0
			aktuelle_zeile = aktuelles_blatt[cursor_y]
			zeile_länge = len(aktuelle_zeile)
			if cursor_x>zeile_länge:
				cursor_x=zeile_länge

	elif kk==51:#rechts	
		if kmod==1:
			if cursor_y==len(aktuelles_blatt):
				pass
			else:
				aktuelle_zeile = aktuelles_blatt[cursor_y]

				cursor_x=len(aktuelle_zeile)
				if cursor_x>=zeichen_pro_zeile:
					cursor_x=zeichen_pro_zeile-1
		else:
			if cursor_y==len(aktuelles_blatt):
				pass
			else:
				aktuelle_zeile = aktuelles_blatt[cursor_y]
				if (cursor_x==zeichen_pro_zeile-1) or (cursor_x==len(aktuelle_zeile)):
					cursor_x=0
					cursor_y=cursor_y+1
				elif cursor_x<len(aktuelle_zeile):
					cursor_x=cursor_x+1
	elif kk==119:#unten
		if cursor_y<len(aktuelles_blatt):
			if kmod==0:
				cursor_y=cursor_y+1	
			else:
				diff = cursor_y-v_Position
				cursor_y=cursor_y + bildschirm_zeilen

				if cursor_y>len(aktuelles_blatt):
					cursor_y=len(aktuelles_blatt)
				
				v_Position=cursor_y-diff
				if v_Position+bildschirm_zeilen-1>len(aktuelles_blatt):
					v_Position = len(aktuelles_blatt)-bildschirm_zeilen				

			if cursor_y<len(aktuelles_blatt):
				aktuelle_zeile = aktuelles_blatt[cursor_y]
				zeile_länge = len(aktuelle_zeile)
				if cursor_x>zeile_länge:
					cursor_x=zeile_länge
			else:
				cursor_x=0

	elif kk==97:#anfang	
			if blatt_idx>0:
				blatt_idx=blatt_idx-1
				speichere_globale_Daten()
				cursor_x=0
				cursor_y=0

	elif kk==113:#ende		
			if blatt_idx==len(blätter)-1:
				blätter.append([])

			blatt_idx=blatt_idx+1

			speichere_globale_Daten()

			cursor_x=0
			cursor_y=0

	fitCursor()


def machFormatting(kk,kmod):
	global cursor_x
	global cursor_y
	global blatt_idx
	global blätter
	global v_Position
	global eingabewort

	blatt=blätter[blatt_idx]

	if kk==122:#rücktaste
		if kmod:
			blätter[blatt_idx]=[]
			cursor_x=0
			cursor_y=0
			return

		if len(eingabewort)>0:
			eingabewort=eingabewort[:-1]
		elif cursor_x>0:
			cursor_x=cursor_x-1
			zeile = blatt[cursor_y]
			zeile.pop(cursor_x)
		elif cursor_y>0:
			if cursor_y==len(blatt):
				cursor_y=cursor_y-1
				cursor_x=len(blatt[cursor_y])
			else:
				aux_linie=blatt.pop(cursor_y)
				cursor_y=cursor_y-1
				cursor_x=len(blatt[cursor_y])
				blatt[cursor_y]=(blatt[cursor_y]+aux_linie)[:zeichen_pro_zeile]

	elif kk==54:#tab
		eingabewort=""
		if cursor_y==len(blatt):
			blatt.append([])
		zeile = blatt[cursor_y]
		zeile.insert(cursor_x,"\t")

		del zeile[zeichen_pro_zeile:]

		if cursor_x<zeichen_pro_zeile-1:
			cursor_x=cursor_x+1
		else:
			cursor_y=cursor_y+1

			if cursor_y<len(blatt):
				aktuelle_zeile = blatt[cursor_y]
				zeile_länge = len(aktuelle_zeile)
				if cursor_x>zeile_länge:
					cursor_x=zeile_länge
			else:
				cursor_x=0
	elif kk==98:#enter 
		if len(eingabewort)>0:
			machWortEnde(104,kmod)

		if cursor_y==len(blatt):
			blatt.append([])
			cursor_y=cursor_y+1
		else:
			aktuelle_zeile = blatt[cursor_y]
			teil_wan = aktuelle_zeile[:cursor_x]
			teil_tu = aktuelle_zeile[cursor_x:]

			blatt[cursor_y]=teil_wan
			blatt.insert(cursor_y+1,teil_tu)

			cursor_y=cursor_y+1
			cursor_x=0

	fitCursor()

def machInterpunktion(kk,kmod):
	global cursor_x
	global cursor_y
	global blatt_idx
	global blätter
	global v_Position
	global eingabewort
	global decknamen

	if len(eingabewort)>0:
		machWortEnde(104,kmod)

	blatt=blätter[blatt_idx]
	
	neues_wort = interpunktion_codes[kk]
	if cursor_y==len(blatt):
		blatt.append([])
	
	aktuelle_zeile = blatt[cursor_y]
	if cursor_x==len(aktuelle_zeile):
		aktuelle_zeile.append(neues_wort)
	else:
		aktuelle_zeile[cursor_x]=neues_wort
	
	cursor_x=cursor_x+1
	if cursor_x>=zeichen_pro_zeile:
		cursor_x=0
		cursor_y=cursor_y+1

	eingabewort=""

	fitCursor()



def machWortEnde(kk,kmod):
	global cursor_x
	global cursor_y
	global blatt_idx
	global blätter
	global v_Position
	global eingabewort
	global decknamen

	blatt=blätter[blatt_idx]

	if kk==104:#leerzeichen
		if not (eingabewort in decknamen):
			eingabewort=""
			return		

		if len(eingabewort)==0 :
			print("word",eingabewort,"not found")
			eingabewort=""
			return machCursorbewegung(51,kmod)

		neues_wort = decknamen[eingabewort]
		if cursor_y==len(blatt):
			blatt.append([])
		
		aktuelle_zeile = blatt[cursor_y]
		if cursor_x==len(aktuelle_zeile):
			aktuelle_zeile.append(neues_wort)
		else:
			aktuelle_zeile[cursor_x]=neues_wort
		
		cursor_x=cursor_x+1
		if cursor_x>=zeichen_pro_zeile:
			cursor_x=0
			cursor_y=cursor_y+1

		eingabewort=""

	fitCursor()


def machBuchstabe(kk,kmod):
	global eingabewort
	if len(eingabewort)>=7:
		return

	bsb = keyname[kk][0].lower()
	eingabewort+=bsb


	# (zahl,ziel)=wurzelzahl(eingabewort)
	# if zahl==1:
	# 	eingabewort=ziel
	# 	machWortEnde(104,kmod)

# define a main function
def main():
	global SCALE
	global v_Position
	global zeichen_sm

	clock = pygame.time.Clock()

	lade_Datei()

	lade_globalen_Zustand()

	# initialize the pygame module
	pygame.init()
	pygame.mouse.set_visible(False)
	pygame.key.set_repeat(150)
	pygame.event.set_blocked(pygame.MOUSEMOTION)
	pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
	pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
	pygame.event.set_blocked(pygame.KEYUP)


	# load and set the logo
	logo = pygame.image.load("sitelen_lili.png")
	
	hg_sm = pygame.image.load("hintergrund.png")
	hg = pygame.transform.scale(hg_sm,(s_w,s_h))
	
	zeichen_sm = pygame.image.load("font.png")
	zeichen = pygame.transform.scale(zeichen_sm,(zeichen_sm.get_width()*SCALE,zeichen_sm.get_height()*SCALE))

	pygame.display.set_icon(logo)
	pygame.display.set_caption("ilo sitelen")
	 
	bildfläche = pygame.display.set_mode((s_w,s_h),pygame.FULLSCREEN)


	# define a variable to control the main loop
	running = True
	 

	pygame.event.clear()
	zeiche_Bild(bildfläche,hg,zeichen) 

	# main loop
	while running:
		event = pygame.event.wait()
		print(event)
		# event handling, gets all event from the event queue
		if event.type == pygame.KEYDOWN:
			if event.key==27:
				beenden()
				return

			if keyname.get(event.key)== None:
				continue
			if event.key==304:
				speicheren_Datei(blatt_idx)
			elif kk_seiAlpha(event.key):
				machBuchstabe(event.key,event.mod)
			elif kk_wortEnde(event.key):
				machWortEnde(event.key,event.mod)
			elif kk_Interpunktion(event.key):
				machInterpunktion(event.key,event.mod)
			elif kk_Cursorbewegung(event.key):
				machCursorbewegung(event.key,event.mod)
			elif kk_Formatting(event.key):
				machFormatting(event.key,event.mod)

			zeiche_Bild(bildfläche,hg,zeichen)    

		# only do something if the event is of type QUIT
		if event.type == pygame.QUIT:
			# change the value to False, to exit the main loop
			running = False

		clock.tick(60)
	 
	 
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	# call the main function
	main()