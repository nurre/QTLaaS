import requests

SERVER_URL = "http://" + input("The address to the server (exclude \'http://\', include port): ")
UPLOAD_URL = SERVER_URL + '/upload'
CREATE_URL = SERVER_URL + '/create'
DESTROY_URL = SERVER_URL + '/destroy'
WORKERS_URL = SERVER_URL + '/workers'
TOKEN_URL = SERVER_URL + '/token'

def upload_file(path_to_file):
	try:
		files = {'file':open(path_to_file, 'rb')}
	except IOError:
		print("No such file! Try again.")
		return False
	r=requests.post(UPLOAD_URL, files=files, timeout=60)
	return check_status(r)


def check_status(r):
	status = r.raise_for_status()
	if (status == None):
		return True
	else:
		print(status)
		return False

def main_menu():
	print('Welcome to QTLaaS (Version 1.0.ACC.12)')
	while(True):
		main_menu_text = ''' 
Main menu: 
1. Start QTLaaS
2. Configure the number of workers
3. Upload file
4. Stop QTLaaS
5. Token
6. Exit
'''
		user_input = input(main_menu_text)
		#user_input = input()
		if user_input == '1':
			number_of_workers=input('Number of workers: ')
			r = requests.get(CREATE_URL + '/' + number_of_workers, timeout=60)
			status = check_status(r)

			if status:
				print("Successfully sent request to start ")

				print(r.content)
			else:
				print("Problems sending the requests. Please try again later.")

		elif user_input == '2':
			print('Current number of workers: xx [NOT IMPLEMENTED YET]')
			new_number_of_workers = input("Enter a new number of workers: ")
			r = requests.get(WORKERS_URL + '/' + new_number_of_workers)
			print(check_status(r))
			print(r.content)
		elif user_input == '3':
			path_to_file = input('Enter the filepath: ')
			print(upload_file(path_to_file))
		elif user_input == '4':
			r = requests.get(DESTROY_URL, timeout=60)
			print(check_status(r))
			print(r.content)
		elif user_input == '5':
			r.requests.get(TOKEN_URL, timeout=60)
			#print(check_status(r))
			print(r.content)
		elif user_input == '6':
			print("Good bye!")
			break
		else:
			print('Incorrect input. Try again!')


if __name__ == '__main__':
	main_menu()
	





