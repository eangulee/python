#class test
__author__ = 'eangulee'
class Student(object):
#same as construction functionc
	def __init__(self, name, score):
		self.name = name
		self.score = score

	def print_score(self):
		print('%s: %s' % (self.name, self.score))

	def get_function(self,x):
		return lambda: x ** 2

def main():
	stu = Student('eangulee',100)
	stu.print_score()
	f = stu.get_function(10)
	a = f()
	print(str(a))

if __name__ == '__main__':
	main()