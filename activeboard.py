'''TRR LensCrafter version 1.0.0'''
'''3 Jul 2015'''
import sys,time,io
from SimpleCV import Camera
import urllib as url
import pygame
from pygame.locals import *
from PIL import ImageTk, Image
global tk,canvas,pygame,localtime
global cam_num,Camera
global screen,Button1,Position1,bg_color,root,xroot,yroot
global Date_Button,Month_Button,Date_set,Month_set,Cancel_Button
global L_set,O_set,save_data,load_data
global pic_num,plu_pic_num,plu,plu_pic,plu_tkpi,plu_rect,plu_take_a_picture
global nok_air_task,print_text,passpass,xx,yy
cam_num=0
passpass=0
pygame.init()
news_url='http://prthai.com/rss-news.asp?catid=20'
bg_color=(30,144,255)
root=0
xroot=0
yroot=0

class Button:

	def create_button(self, surface, color, x, y, length, height, width, text, text_color):
		global rect
		surface = self.draw_button(surface, color, length, height, x, y, width)
		surface = self.write_text(surface, text, text_color, length, height, x, y)
		self.rect = pygame.Rect(x,y, length, height)
		return surface

	def write_text(self, surface, text, text_color, length, height, x, y):
		if len(text)==0:
			return surface
		elif len(text)>=3:
			font_size = int(length//len(text))
		else:
			font_size = int(height//len(text))
		myFont = pygame.font.SysFont("Calibri", font_size)
		myText = myFont.render(text, 1, text_color)
		surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
		return surface

	def draw_button(self, surface, color, length, height, x, y, width):           
		for i in range(1,10):
			s = pygame.Surface((length+(i*2),height+(i*2)))
			s.fill(color)
			alpha = (255/(i+2))
			if alpha <= 0:
				alpha = 1
			s.set_alpha(alpha)
			pygame.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
			surface.blit(s, (x-i,y-i))
		pygame.draw.rect(surface, color, (x,y,length,height), 0)
		pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)  
		return surface

	def pressed(self, mouse):
		if mouse[0] > self.rect.topleft[0]:
			if mouse[1] > self.rect.topleft[1]:
				if mouse[0] < self.rect.bottomright[0]:
					if mouse[1] < self.rect.bottomright[1]:
						return True
					else: return False
				else: return False
			else: return False
		else: return False

def print_text(surface, text, text_color, bg_color, length, height, x, y):
	pygame.draw.rect(surface, bg_color, (x,y,length,height), 0)
	font_size = int(length//len(text))
	myFont = pygame.font.SysFont("Calibri", font_size)
	myText = myFont.render(text, 1, text_color)
	surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))

def save_data():
	global pic_num,plu_pic,plu_pic_num,Position1,plu_text,L_set,O_set
	f=open('data.txt','r')
	line=f.readlines()
	if len(line)==0:
		f.close()
		f=open('data.txt','w')
		pic_num=1
		f.write(str(1)+'\n')
	else:
		f.close()
		f=open('data.txt','w')
		f.write(str(pic_num)+'\n')
	for i in range(4,45):
		f.write(str(Position1[i])+'\n')
	for i in range(4,45):
		if plu_pic[i]==True: 
			f.write('1\n')
			f.write(str(plu_pic_num[i])+'\n')
			f.write(plu_text[i]+'\n')
			if L_set[i]:
				f.write('L\n')
			elif O_set[i]:
				f.write('O\n')
			else:
				f.write('None\n') 
		else: 
			f.write('0\n')
	f.close()

def load_data():
	global pic_num,plu_pic,plu_pic_num,plu_tkpi,plu_rect,Position1,plu_text,L_set,O_set
	f=open('data.txt','r')
	line=f.readlines()
	if len(line)==0:
		f.close()
		save_data()
		f=open('data.txt','r')
		line=f.readlines()
	pic_num=int(line[0])
	k=1
	for i in range(4,45):
		Position1[i]=int(line[k])
		k=k+1
	for i in range(4,45):
		if int(line[k])==0:
			k=k+1
		else:
			plu_pic[i]=True
			plu_pic_num[i]=int(line[k+1])
			plu_tkpi[i] = pygame.image.load('./pic/p'+format(plu_pic_num[i],'012')+'.jpg')
			plu_rect[i] = plu_tkpi[i].get_rect()
			plu_text[i]=line[k+2][:-1]
			if line[k+3][:-1]=='L':
				L_set[i]=True
			elif line[k+3][:-1]=='O':
				O_set[i]=True
			k=k+4
	f.close()

#Update the display and show the button
def update_display():
	global Button,Button1,Position1,root,xroot,yroot,passpass,Date_Button,Month_Button,Cancel_Button
	global Date_set,Month_set,L_set,O_set
	global plu_pic,plu_tkpi,plu_rect,plu_text,localtime,xx,yy
	mm=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

	screen.fill(bg_color)
	Button1[0].create_button(screen, (200,0,0),  5,  5, 90,    170,    0,      'L', (255,255,255))
	Button1[1].create_button(screen, (60,0,15),  5,  185, 90,   170,    0,      'O', (255,255,255))
	Button1[2].create_button(screen, (0,142,15),  5,  365, 90,   170,    0,      'X', (255,255,255))
	for j in range(12):
		if Month_set==j+1:
			Month_Button[j].create_button(screen, (250,250,0), 840,255+(j*25),35,20,0,mm[j], (0,0,0))
		else:
			Month_Button[j].create_button(screen, (0,0,250), 840,255+(j*25),35,20,0,mm[j], (255,255,255))
	if Date_set!=0 or Month_set!=0:
		Cancel_Button.create_button(screen,(107,142,35), 840,230,35,20,0,'C',(255,255,255))
	else:
		Cancel_Button.create_button(screen,(250,250,0), 840,230,35,20,0,'C',(255,255,255))
	for j in range(22):
		if Date_set==j+1:
			Date_Button[j].create_button(screen, (250,250,0), 800,5+(j*25),35,20,0,str(j+1), (0,0,0))		
		else:
			Date_Button[j].create_button(screen, (107,142,35), 800,5+(j*25),35,20,0,str(j+1), (255,255,255))		
	for j in range(22,31):
		if Date_set==j+1:
			Date_Button[j].create_button(screen, (250,250,0), 840,5+((j-22)*25),35,20,0,str(j+1), (0,0,0))				
		else:		
			Date_Button[j].create_button(screen, (107,142,35), 840,5+((j-22)*25),35,20,0,str(j+1), (255,255,255))				
	k=3
	kk=1
	for j in range(6):
		for i in range(7):
			cx=(250,250,0)
			bx=(200,0,0)
			if L_set[Position1[k]]:
				cx=(200,0,0)
				bx=(255,255,255)
			elif O_set[Position1[k]]:
				cx=(60,0,15)
				bx=(255,255,255) 
			if k!=root:
				#Parameters       surface,      color,          x,                  y, length, height, width,    text,      text_color
				Button1[k].create_button(screen, (107,142,35),  100+(i*100),  5+(j*90), 90,    80,    0,          '', (255,255,255))
				if k==3 and passpass==30:
					nok_air_task()
					screen.blit(plu_tkpi[3],plu_rect[3])
					print_text(screen,plu_text[3],bx,cx,90,20,100,65)
					passpass=0
				elif k==3:
					if plu_pic[3]:
						screen.blit(plu_tkpi[3],plu_rect[3])
						print_text(screen,plu_text[3],bx,cx,90,20,100,65)
					passpass=passpass+1
				elif plu_pic[Position1[k]]:
					plu_rect[Position1[k]][0]=100+(i*100)
					plu_rect[Position1[k]][1]=5+(j*90)
					screen.blit(plu_tkpi[Position1[k]],plu_rect[Position1[k]])
					print_text(screen,plu_text[Position1[k]],bx,cx,90,20,100+(i*100),65+(j*90))
			k=k+1
			kk=kk+1
	k=3
	kk=1
	for j in range(6):
		for i in range(7):
			if k==root:
				bx=(200,0,0)
				cx=(250,250,0)
				if L_set[Position1[k]]:
					cx=(200,0,0)
					bx=(255,255,255)
				elif O_set[Position1[k]]:
					cx=(60,0,15)
					bx=(255,255,255) 
				#Parameters       surface,      color,          x,                                                           y, length, height, width,    text,      text_color
				Button1[k].create_button(screen, (107,142,35),  pygame.mouse.get_pos()[0]-xroot,  pygame.mouse.get_pos()[1]-yroot, 90,    80,    0,        '' , (255,255,255))
				plu_rect[Position1[k]][0]=pygame.mouse.get_pos()[0]-xroot
				plu_rect[Position1[k]][1]=pygame.mouse.get_pos()[1]-yroot
				screen.blit(plu_tkpi[Position1[k]],plu_rect[Position1[k]])
				print_text(screen,plu_text[Position1[k]],bx,cx,90,20,pygame.mouse.get_pos()[0]-xroot,pygame.mouse.get_pos()[1]-yroot+60)
			k=k+1
			kk=kk+1
	pygame.display.flip()

localtime = time.asctime( time.localtime(time.time()) )
Month_list = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
xx=[]
yy=[]
Date_Button = []
Month_Button = []
Cancel_Button = Button()
Date_set=int(localtime[8:10])
Month_set=(Month_list[localtime[4:7]])
pic_num = 0
plu_tkpi = []
plu_rect = []
plu_text = []
plu_pic = []
plu_pic_num = []
Button1 = []
Position1 = []
L_set = []
O_set = []
Chk = []
for i in range(45):
	Button1.append(Button())
	Position1.append(i)
	plu_pic.append(False)
	plu_pic_num.append(0)
	plu_tkpi.append('')
	plu_rect.append('')
	plu_text.append('')
	L_set.append(False)
	O_set.append(False)
	Chk.append(False)
	xx.append(0)
	yy.append(0)
for i in range(31):
	Date_Button.append(Button())
for i in range(12):
	Month_Button.append(Button())
k=3
for j in range(6):
	for i in range(7):
		xx[k]=100+(i*100)
		yy[k]=65+(j*90)
		k=k+1
load_data()

def nok_air_task():
	global plu_tkpi,plu_rect,plu_text,cam_num,plu_pic
	plu_pic[3] = True
	cam = Camera(cam_num)
	img = cam.getImage()
	thumbnail = img.scale(90,60)
	thumbnail.save('tmp_picture.jpg')
	plu_tkpi[3] = pygame.image.load('tmp_picture.jpg')
	plu_rect[3] = plu_tkpi[3].get_rect()
	plu_rect[3][0] = 100
	plu_rect[3][1] = 5
	plu_text[3] = localtime[8:10]+' '+localtime[4:7]

def take_a_picture(i):
	global pic_num,plu_pic_num,plu_tkpi,plu_rect,plu_text,cam_num,plu_pic
	if i<=3 : return
	mm=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	plu_pic[i] = True
	cam = Camera(cam_num)
	img = cam.getImage()
	thumbnail = img.scale(90,60)
	pic_num=pic_num+1
	thumbnail.save('./pic/p'+format(pic_num,'012')+'.jpg')
	plu_tkpi[i] = pygame.image.load('./pic/p'+format(pic_num,'012')+'.jpg')
	plu_pic_num[i] = pic_num
	plu_rect[i] = plu_tkpi[i].get_rect()
	if Date_set!=0 and Month_set!=0:
		plu_text[i] = str(Date_set)+' '+mm[Month_set-1]
	else:
		plu_text[i] = localtime[8:10]+' '+localtime[4:7]

mm=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
pygame.display.set_icon(pygame.image.load('trr.gif'))
pygame.display.set_caption('active board v1')
size=(880,550)
screen=pygame.display.set_mode(size)
clock = pygame.time.Clock() 
#label4002 = tk.Label(canvas, text=localtime,font="Arial 8")
#canvas.create_window(10,80, anchor='nw', window=label4002)
running = True
while running:
	update_display()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			save_data()
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			posi=pygame.mouse.get_pos()
			if posi[0]>800:
				if root!=0:
					L_set[Position1[root]]=False
					O_set[Position1[root]]=False
					if Date_set!=0 and Month_set!=0:
						plu_text[Position1[root]] = str(Date_set)+' '+mm[Month_set-1]
					else:
						plu_text[Position1[root]] = localtime[8:10]+' '+localtime[4:7]
					root=0
					save_data()
					continue
				else:
					for i in range(31):
						if Date_Button[i].pressed(posi):
							Date_set=i+1
							continue
					for i in range(12):
						if Month_Button[i].pressed(posi):
							Month_set=i+1
							continue
					if Cancel_Button.pressed(posi):
						Date_set=int(localtime[8:10])
						Month_set=(Month_list[localtime[4:7]])
						continue
			else:
				if root!=0:
					if Button1[0].pressed(posi):
						L_set[Position1[root]]=True
						root=0
						save_data()
						continue	
					if Button1[1].pressed(posi):
						O_set[Position1[root]]=True
						root=0
						save_data()
						continue	
					if Button1[2].pressed(posi):
						L_set[Position1[root]]=False
						O_set[Position1[root]]=False
						plu_pic[Position1[root]]=False
						root=0
						save_data()
						continue	
					t=root
					tt=Position1[root]
					root=0
					for k in range(3,45):
						if Button1[k].pressed(posi):
							if t>k:
								ptt=Position1[t-1]
								for i in range(k,t):
									Position1[t-(i-k)]=Position1[t-((i-k)+1)]
								Position1[t]=ptt
								Position1[k]=tt
							elif t==k:
								pass
								# Position1[k]=tt
							else:
								for i in range(t,k):
									Position1[i]=Position1[i+1]
								Position1[k]=tt
							save_data()								
				else:
					if Button1[0].pressed(posi):
						k=3
						for i in range(3,45):
							if plu_pic[Position1[i]] and L_set[Position1[i]]==False and O_set[Position1[i]]==False:
								kk=Position1[k]
								Position1[k]=Position1[i]
								Position1[i]=kk
								k=k+1
						for i in range(3,45):
							if L_set[Position1[i]]==True:
								kk=Position1[k]
								Position1[k]=Position1[i]
								Position1[i]=kk
								k=k+1
						for i in range(3,45):
							if O_set[Position1[i]]==True:
								kk=Position1[k]
								Position1[k]=Position1[i]
								Position1[i]=kk
								k=k+1
						save_data()
						continue
					if Button1[1].pressed(posi):
						k=3
						for i in range(3,45):
							if plu_pic[Position1[i]] and L_set[Position1[i]]==False and O_set[Position1[i]]==False:
								kk=Position1[k]
								Position1[k]=Position1[i]
								Position1[i]=kk
								k=k+1
						if k<=9 : k=10
						elif k>10 and k<=16: k=17
						elif k>17 and k<=23: k=24
						elif k>24 and k<=30: k=31
						elif k>31 and k<=37: k=38
						for i in range(3,45): Chk[i]=False
						for i in range(3,45):
							if k>=45: break
							if L_set[Position1[i]]==True and Chk[i]==False:
								kk=Position1[k]
								Position1[k]=Position1[i]
								Chk[k]=True
								Position1[i]=kk
								k=k+1
						if k<=9 : k=10
						elif k>10 and k<=16: k=17
						elif k>17 and k<=23: k=24
						elif k>24 and k<=30: k=31
						elif k>31 and k<=37: k=38
						for i in range(3,45): Chk[i]=False						
						for i in range(3,45):
							if k>=45: break
							if O_set[Position1[i]]==True and Chk[i]==False:
								kk=Position1[k]
								Position1[k]=Position1[i]
								Chk[k]=True
								Position1[i]=kk
								k=k+1
						save_data()
						continue						
					for k in range(3,45):
						if Button1[k].pressed(posi):
							if plu_pic[Position1[k]]:
								xroot=pygame.mouse.get_pos()[0]-Button1[k].rect.x
								yroot=pygame.mouse.get_pos()[1]-Button1[k].rect.y
								root=k
							else:
								take_a_picture(Position1[k])
								save_data()
	msElapsed = clock.tick(30)
pygame.quit()
