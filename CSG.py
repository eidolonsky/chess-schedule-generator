#-*-coding:utf-8-*-
from Tkinter import *
import tkMessageBox
from collections import deque
import random
	
def clr_text():
	e.delete(0, END)

def nameget():
	global namelist,n
	name = e.get()
	namelist.append(name)
	#排除重复输入同一姓名
	tl = []
	for i in namelist:
		if not i in tl:
			tl.append(i)
	namelist = tl	
	n=len(namelist)
	
def output():
	global namelist,n
	#国际象棋需要至少两人
	if n == 1:
		tkMessageBox.showwarning("Warning","Only one player!\nPlease input at least two players.")
		return

	#由于两人对阵，总人数为奇数时，多出来的一人轮空。加入“Bye”视作凑成偶数。
	if n % 2 != 0:
		n = n + 1
		namelist = namelist + ["Bye"]

	checkinfo()

def checkinfo():    
	global n
	if n <= 8:
		csche = "The schedule: double round robin"
	if n > 8:
		csche = "The schedule: single round robin"
	
	schetop = Toplevel()
	schetop.title("Generate")
	
	if "Bye" in namelist:
		Label(schetop,text="The number of players is "+str(n-1)).grid(sticky=W)
	else:
		Label(schetop,text="The number of players is "+str(n)).grid(sticky=W)
	Label(schetop,text=csche).grid()
	
	Button(schetop,text="Generate",command=generate).grid()

def generate():
	gene_top = Toplevel()
	gene_top.geometry("200x450") 
	gene_top.title("Schedule")
	
	Button(gene_top,text="Input Outcome",command=scoreget).grid(sticky=W)
	
	Label(gene_top,text="This is the schedule: ").grid(sticky=W)
	
	text = Text(gene_top)
	


	#此段关于循环赛程，参考了网上的蛇环算法，原用于英超赛程.
	global namelist,n
	scheobj = dict.fromkeys(range(1,n))
	fixpos = namelist[0]
	ring = namelist[1:]
	ring = deque(ring)

	#前半赛程，1~n-1轮(round)
	for round in range(1,n):
		#第1人不动，再加上轮转(rotate)的环
		teams = [fixpos] + list(ring)
		#切成2列，左边执白，右边执黑
		white, black = teams[:len(teams)/2],teams[len(teams)/2:]
		black = black[::-1]
		#随机打乱先后手
		scheobj[round] = [(x,y) if random.random()>=0.5 else (y,x) for x,y in zip(white,black)]
		ring.rotate(1)

	#后半赛程对阵跟前半赛程一样，但先后手对调
	for round in range(n,2*n-1):
		scheobj[round] = [(y,x) for x,y in scheobj[round-n+1]]
	
	#生成，人数不同，轮数不同
	e = 0
	dr2 = ""
	if n > 10:
		for n in range(1,n):
			e = e + 1
			dr1 = u"---round"+str(e)+"---\n"
			dr2 = dr2 + dr1
			for w,b in scheobj[n]:
				dr3 = "{} : {}\n".format(w,b)
				dr2 = dr2 + dr3	
	
	if n <= 10:
		for n in range(1,2*n-1):
			e = e + 1
			dr1 = u"---round"+str(e)+"---\n"
			dr2 = dr2 + dr1
			for w,b in scheobj[n]:
				dr3 = "{} : {}\n".format(w,b)
				dr2 = dr2 + dr3	
	
	text.insert(INSERT, dr2)
	text.grid()

#生成两个与姓名列表等长的列表，用姓名列表的索引定位，从而使分数和累进分列表中的同索引分数与姓名对应
#赢棋计两分，和棋计一分，输棋不计分
def scoreget():
	def clr_text():
		e.delete(0, END)
	
	def getscore():
		global n,namelist,selection,scorelist,pscorelist
		try:	
			score_name = e.get()
			t = namelist.index(score_name)
			score = var.get()
			scorelist[t] = scorelist[t] + score
			pscorelist[t] = pscorelist[t] + scorelist[t]
		except ValueError:
			tkMessageBox.showwarning("Warning","This player doesn't attend!\nPlease input another player.")
			
	global n,namelist,selection,scorelist,pscorelist
	scorelist = n*[0]
	pscorelist = n*[0]
	
	score_top = Toplevel()
	score_top.geometry("330x200")
	score_top.title("Input Score")
	
	e = Entry(score_top) 
	e.grid(row=0,column=1,columnspan=3,sticky=W)
	
	Label(score_top,text="Name:").grid(row=0,column=0,sticky=W)
	Label(score_top,text="Outcome:").grid(row=1,column=0,sticky=W)
	var = IntVar()

	R1 = Radiobutton(score_top, text="Win", variable=var, value=2)
	R1.grid(row=1,column=1,sticky=W)
	R2 = Radiobutton(score_top, text="Draw", variable=var, value=1)
	R2.grid(row=2,column=1,sticky=W)
	R3 = Radiobutton(score_top, text="Lose", variable=var, value=0)
	R3.grid(row=3,column=1,sticky=W)
	
	Button(score_top,text="Confirm",width=8,command=getscore).grid(row=4,column=1,sticky=E+N+W+S)
	Button(score_top,text="Print",width=8,command=printscore).grid(row=4,column=2,sticky=E+N+W+S)
	Button(score_top,text="Clear",width=8,command=clr_text).grid(row=4,column=0,sticky=E+N+W+S)

	Label(score_top,text="Win:2 points;Draw:1 point;Lose:0").grid(row=5,columnspan=3,sticky=W)	
	Label(score_top,text="Press confirm to record score in the order of rounds.").grid(row=6,columnspan=3,sticky=W)
	Label(score_top,text="Press print to see the score list.").grid(row=7,columnspan=3,sticky=W)

#由于没有研究出在Tkinter中如何放置并列的listbox的方法,用text展示比分
def printscore():
	global n,namelist,scorelist,pscorelist
	pscore_top = Toplevel()
	pscore_top.geometry("300x300")
	pscore_top.title("Score")
	
	Label(pscore_top,text="This is the score list:").grid(row=0,sticky=W)
	Label(pscore_top,text="Name-Score-ProScore*").grid(row=1,sticky=W)
	Label(pscore_top,text="* Proscore refers to progressive score:").grid(row=2,columnspan=3,sticky=W)
	Label(pscore_top,text="  the progressive addition of every round's score.").grid(row=3,columnspan=3,sticky=W)

	text = Text(pscore_top)
	
	if "Bye" in namelist:
		namelist.pop()
		scorelist.pop()
		pscorelist.pop()
	
		a = namelist
		b = scorelist
		c = pscorelist
		le = len(a)
		for i in range(0,le):
			k = "   " + a[i] + "---" + str(b[i]) + "---" + str(c[i]) + "\n"
			text.insert(INSERT, k)
			text.grid()

	else:
		a = namelist
		b = scorelist
		c = pscorelist
		le = len(a)
		for i in range(0,le):
			k = str(i+1) + "." + "---" + a[i] + "---" + str(b[i]) + "---" + str(c[i]) + "\n"
			text.insert(INSERT, k)
			text.grid()
	

root = Tk() 
root.title("Schedule Generator")
root.geometry("300x100")

e = Entry(root,width=21) 
e.grid(row=0,column=1,columnspan=2,sticky=W) 
e.focus_set()

Label(root,text="Name:").grid(row=0,column=0,columnspan=1,sticky=E)

b2 = Button(root, text="Clear", width=8, command=clr_text)
b2.grid(row=1,column=0)
b1 = Button(root, text="Comfirm", width=8,command=nameget)
b1.grid(row=1,column=1)
b3 = Button(root, text="Next", width=8, command=output)
b3.grid(row=1,column=2) 

Label(root,text="Confirm after input a name").grid(columnspan=2,sticky=W)

namelist = []
n = 19921003

mainloop()









