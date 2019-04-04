import threading
import time
def func1():
	act = input('Please enter input')
	while act == '1':
		act = input('Please enter input')
	print('func1 over')

def func2():
	for i in range(5):
		print('i:',i)
		time.sleep(2)
if __name__ == '__main__':
	print('here is main')
	try:
		t1 = threading.Thread(target = func1)
		t2 = threading.Thread(target = func2)
	except:
		print('Error')
	t1.start()
	t2.start()

	input()