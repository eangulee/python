# import math
# this is a python program test
# this is the first comment
# spam = 1  # and this is the second comment
# ... and now a third!
# text = "# This is not a comment because it's inside quotes."
'''
print(spam)
print(text)
print(str(spam) + text)
num = int(input('please input a number:'))
num = abs(num)
print('num:' + str(num))
# name = input('please enter your name: ')
# print('hello,', name)

'''
'''
from class_test import Student# from 文件 import 类
stu = Student('eangulee',100)
stu.print_score()
'''
from tkinter import *

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.helloLabel = Label(self, text='Hello, world!')
		self.helloLabel.pack()
		self.quitButton = Button(self, text='Quit', command=self.quit)
		self.quitButton.pack()

app = Application()
# 设置窗口标题:
app.master.title('Hello World')
# 主消息循环:
app.mainloop()