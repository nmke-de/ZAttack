#!/usr/bin/python3
import pickle

def save_exit():
	try:
		the_file = open("game.pix","wb")
	except:
		print("Error with saving program datas")
	pickle.dump(0,the_file) #player's x
	pickle.dump(0,the_file) #player's y
	pickle.dump(100,the_file) #zombie's x
	pickle.dump(100,the_file) #zombie's y
	the_file.close()
	quit()

save_exit()
