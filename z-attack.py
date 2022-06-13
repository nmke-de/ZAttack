import tkinter, time, _thread, pickle


main = tkinter.Tk()
world = tkinter.Frame(main,width=200,height=200,relief="sunken",bd=1)
world.pack()

inv_label = tkinter.Label(main,text="")
gameover = False

# classes/functions
class movable():
	"""
	x = 0
	y = 0
	life = 3
	animation = tkinter.Label(world)
	
	def __init__(self):
		self.x = 0
		self.y = 0
		self.life = 3
		self.animation = tkinter.Label(world)
	"""
	def __del__(self):
		global world
		global main
		self.animation.destroy()
		end = tkinter.Label(main,text="You have lost.")
		end.pack()
		#main.destroy()
	def up(self):
		self.y = self.y - 5
		if self.y < 0:
			self.y = 0
		self.animation.place(x=self.x,y=self.y,anchor="nw")
	
	def left(self):
		self.x = self.x - 5
		if self.x < 0:
			self.x = 0
		self.animation.place(x=self.x,y=self.y,anchor="nw")
	
	def down(self):
		self.y = self.y + 5
		if self.y > 180:
			self.y = 180
		self.animation.place(x=self.x,y=self.y,anchor="nw")
	
	def right(self):
		self.x = self.x + 5
		if self.x > 180:
			self.x = 180
		self.animation.place(x=self.x,y=self.y,anchor="nw")
	
	def beaten(self):
		self.life -= 1
		print(self.life)
		if self.life < 0:
			self.__del__()
		#
	
	def getpos(self):
		return (self.x,self.y)
	#	def __del__(self):
	#		self.animation.place(x=-1000,y=-1000)
	def __init__(self,c,startpos_x,startpos_y,base):
		self.char = c
		self.animation = base
		self.animation["text"]=self.char
		self.x = startpos_x
		self.y = startpos_y
		self.animation.place(x=self.x,y=self.y,anchor="nw")
		self.life = 3
	# End of class

class player(movable):
	def __init__(self,c,startpos_x,startpos_y,base):
		movable.__init__(self,c,startpos_x,startpos_y,base)
		self.players_inventory = ""
	def inventory(self,ev):
		global inv_label
		inv_label["text"] = self.players_inventory
		#self.inv_label.pack()
	def __del__(self):
		movable.__del__(self)
	def get_sword(self):
		self.players_inventory = "Sword"
	def update(self,ev):
		global inv_label
		if ev.char=="h":self.life = 3
		if self.life <=0:
			inv_label["text"] = "GAME OVER"
			gameover = True
			del self
			return
		if ev.char == "a":
			self.left()
		elif ev.char =="w":
			self.up()
		elif ev.char =="s":
			self.down()
		elif ev.char =="d":
			self.right()
		elif ev.char =="q":
			save_exit()
		if self.x==0 and self.y==5:
			self.get_sword()
			inv_label["text"] = self.players_inventory
	def __del__(self):
		global world
		global main
		world.destroy()
		end = tkinter.Label(main,text="You have lost.")
		end.pack()
		main.destroy()
	# End of class

class zombie(movable):
	def __init__(self,c,startpos_x,startpos_y,base):
		movable.__init__(self,c,startpos_x,startpos_y,base)
		self.reaction_time = 1
	def act(self):
		while not gameover:
			time.sleep(self.reaction_time)
			if the_player.getpos()[1] > self.y:
				self.down()
			elif the_player.getpos()[0] > self.x:
				self.right()
			elif the_player.getpos()[1] < self.y:
				self.up()
			elif the_player.getpos()[0] < self.x:
				self.left()
			else:
				the_player.beaten()
		
	
	#End of class

#Load

print("Loading...")
try:
	f = open("game.pix","rb")
except:
	print("Error with loading...")
	print("Program will quit NOW")
	quit()
p_x = pickle.load(f)
p_y = pickle.load(f)
z_x = pickle.load(f)
z_y = pickle.load(f)
f.close()
#Actors
the_player = player("X",p_x,p_y,tkinter.Label(world))
the_zombie = zombie("Z",z_x,z_y,tkinter.Label(world))
anchored_zombie = zombie("Z",50,50,tkinter.Label(world))
#Functions

def info(x):
	info_label = tkinter.Label(main,text="Author: Nathanael M.\nProduct: Z-Attack Alpha 2\nby Dot.")
	info_label.pack()

def act_zombie(x):
	if the_player.x > x.x:
		x.down(0)
	elif the_player.x < x.x:
		x.up(0)
	elif the_player.y > x.y:
		x.right(0)
	elif the_player.y < x.y:
		x.left(0)
	else:
		the_player.beaten()
	#

def save_exit():
	try:
		the_file = open("game.pix","wb")
	except:
		print("Error with saving program datas")
	pickle.dump(the_player.getpos()[0],the_file) #player's x
	pickle.dump(the_player.getpos()[1],the_file) #player's y
	pickle.dump(the_zombie.getpos()[0],the_file) #zombie's x
	pickle.dump(the_zombie.getpos()[1],the_file) #zombie's y
	the_file.close()
	quit()

# main program

_thread.start_new_thread(the_zombie.act,())
_thread.start_new_thread(anchored_zombie.act,())
main.bind("<Key>",the_player.update)
#main.bind("<i>",info)

button = tkinter.Button(main,text="Save + Quit",command=save_exit)
button.pack()

inv_label.pack()

main.mainloop()
