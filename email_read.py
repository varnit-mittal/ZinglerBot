# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
from bs4 import BeautifulSoup
# import email

class email_main():
	def __init__(self) -> None:
		pass

	@staticmethod
	def getEmails():
		SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
		creds = None
		if os.path.exists('token.pickle'):
			with open('token.pickle', 'rb') as token:
				creds = pickle.load(token)
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
				creds = flow.run_local_server(port=0)

			with open('token.pickle', 'wb') as token:
				pickle.dump(creds, token)

		service = build('gmail', 'v1', credentials=creds)

		result = service.users().messages().list(userId='me').execute()

		messages = result.get('messages')

		m=[]
		if(len(messages)>5):
			j=1
			for msg in messages:
				l=[]
				# Get the message from its id
				txt = service.users().messages().get(userId='me', id=msg['id']).execute()

				try:
					payload = txt['payload']
					headers = payload['headers']

					for d in headers:
						if d['name'] == 'Subject':
							subject = d['value']
						if d['name'] == 'From':
							sender = d['value']

					parts = payload.get('parts')[0]
					data = parts['body']['data']
					data = data.replace("-","+").replace("_","/")
					decoded_data = base64.b64decode(data)

					soup = BeautifulSoup(decoded_data , "lxml")
					body = soup.text.strip()
					
					l.append(str(subject)) #type:ignore
					l.append(str(sender)) 	 #type:ignore
					l.append(body)
					m.append(l)
				except:
					pass
				j+=1
				# print(j)
				if(j>15):
					break
		else:
			for msg in messages:
				l=[]
				txt = service.users().messages().get(userId='me', id=msg['id']).execute()

				try:
					payload = txt['payload']
					headers = payload['headers']
					for d in headers:
						if d['name'] == 'Subject':
							subject = d['value']
						if d['name'] == 'From':
							sender = d['value']

					parts = payload.get('parts')[0]
					data = parts['body']['data']
					data = data.replace("-","+").replace("_","/")
					decoded_data = base64.b64decode(data)

					soup = BeautifulSoup(decoded_data , "lxml")
					body = soup.text.strip()
					
					l.append(str(subject)) #type:ignore
					l.append(str(sender)) 	 #type:ignore
					l.append(body)
					m.append(l)
				except:
					pass

		return m
