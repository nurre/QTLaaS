import requests

SERVER_URL = 'http://127.0.0.1:5000'
UPLOAD_URL = SERVER_URL + '/upload'
CREATE_URL = SERVER_URL + '/create'
DESTROY_URL = SERVER_URL + '/destory'
WORKERS_URL = SERVER_URL + '/workers'
STATUS_URL = SERVER_URL + '/status'

def upload_file(path_to_file):
	files = {'file':open(path_to_file, 'rb')}
	r=requests.post(UPLOAD_URL, files=files, timeout=60)
	status = r.raise_for_status()
	if (status == None):
		return 'Success!'
	else:
		print(status)
		return 'Something went wrong'

def start_service(number_of_workers):
	pass

def stop_service():
	pass

def configure_workers(new_number_of_workers):


def main_menu():
	print('Welcome to QTLaaS (Version 1.0.ACC.12)')
	while(True):
		main_menu_text = ''' 
Main menu: 
1. Start QTLaaS
2. Configure the number of workers
3. Upload file
4. Stop QTLaaS
5. Exit
'''
		user_input = input(main_menu_text)
		#user_input = input()
		if user_input == '1':
			number_of_workers=input('Number of workers: ')
			r = requests.get(CREATE_URL + '/' + number_of_workers, timeout=60)
			status = r.raise_for_status()
			if (status == None):
				print('Success!')
			else:
				print(status)
				print('Something went wrong')
		elif user_input == '2':
			print('Current number of workers: xx [NOT IMPLEMENTED YET]')
			new_number_of_workers = input("Enter a new number of")
		elif user_input == '3':
			path_to_file = input('Enter the filepath: ')
			print(upload_file(path_to_file))
		elif user_input == '4':
			r = requests.get(DESTROY_URL, timeout=60)
		elif user_input == '5':
			print("Good bye!")
			break
		else:
			print('Incorrect input. Try again!')




if __name__ == '__main__':
	main_menu()
	#print(upload_file('/home/nurre/Hämtningar/28580230_859221900929645_1575770519_o.png'))






