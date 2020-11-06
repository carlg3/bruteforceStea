import os, sys, argparse, cv2, subprocess, time, tkinter
from utilityStea import controllaEstensione, printError, printWarning, printGood, printNormal, printCyan, printInfo, convertiInPDF
from colorama import init, Fore
from immaginiStea import printStea, printSteaBW

init()

welcomeMessage = """

______            _        __                     _____ _             
| ___ \          | |      / _|                   /  ___| |            
| |_/ /_ __ _   _| |_ ___| |_ ___  _ __ ___ ___  \ `--.| |_ ___  __ _ 
| ___ \ '__| | | | __/ _ \  _/ _ \| '__/ __/ _ \  `--. \ __/ _ \/ _` |
| |_/ / |  | |_| | ||  __/ || (_) | | | (_|  __/ /\__/ / ||  __/ (_| |
\____/|_|   \__,_|\__\___|_| \___/|_|  \___\___| \____/ \__\___|\__,_|
                                                                      
																	                                                                        
																																			"""

def selezionaRiquadroImmagine(immagine, titolo): 
		# initialize the list of reference points and boolean indicating
		# whether cropping is being performed or not
		global refPt, cropping, mioclone, cancella, image
		refPt = []
		fattoreScala = 1
		cropping = False
		cancella = False

		def click_and_crop(event, x, y, flags, param):
			global refPt, cropping, mioclone, cancella, image

			# if the left mouse button was clicked, record the starting
			# (x, y) coordinates and indicate that cropping is being
			# performed
			if event == cv2.EVENT_LBUTTONDOWN:
				if cancella == True:
					cancella = False
					image = cv2.imread(immagine)

				refPt = [(x, y)]
				cropping = True

			# check to see if the left mouse button was released
			elif event == cv2.EVENT_LBUTTONUP:
				# record the ending (x, y) coordinates and indicate that
				# the cropping operation is finished
				if len(refPt) == 0:
					refPt = [(0,0)]
				refPt.append((x, y))
				cropping = False
				# draw a rectangle around the region of interest
				cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
				cv2.imshow(titolo, image)
				cancella = True
				

		# uso tkinter per prendere le dimensioni dello schermo
		root = tkinter.Tk()
		screenWidth = root.winfo_screenwidth()
		screenHeight = root.winfo_screenheight()

		# load the image, clone it, and setup the mouse callback function
		# image = cv2.imread(args[titolo])

		image = cv2.imread(immagine)
		

		clone = image.copy()
		mioclone = cv2.imread(immagine)

		imageWidth = image.shape[1]
		imageHeight = image.shape[0]

		
		fattoreScalaVerticale = screenHeight/imageHeight
		fattoreScalaOrizzontale = screenWidth/imageWidth
		'''
		print(imageWidth) # nuovo
		print(imageHeight)
		print(fattoreScalaOrizzontale)
		print(fattoreScalaVerticale)
		'''
		# scalo l'immagine se necesario per farla entrare nello schermo
		if fattoreScalaOrizzontale < 1 or fattoreScalaVerticale < 1:
			fattoreScala =  min(fattoreScalaVerticale, fattoreScalaOrizzontale)
			
			# print(fattoreScala)
			
			if fattoreScala > 0.05: # nuovo
				fattoreScala = fattoreScala - 0.05
			
			finalWidth = int(image.shape[1] * fattoreScala)
			finalHeight = int(image.shape[0] * fattoreScala)
			finalDim = (finalWidth, finalHeight)
			image = cv2.resize(image, finalDim)

		cv2.namedWindow(titolo)
		cv2.moveWindow(titolo, 20, 20)
		cv2.setMouseCallback(titolo, click_and_crop)

		# keep looping until the 'q' key is pressed
		while True:
			if cv2.getWindowProperty(titolo, cv2.WND_PROP_VISIBLE) < 1:
				break
			# display the image and wait for a keypress
			cv2.imshow(titolo, image)
			key = cv2.waitKey(1) & 0xFF
			# if the 'r' key is pressed, reset the cropping region
			if key == ord("r"):
				cv2.destroyAllWindows()
				return ("NV")

		# if there are two reference points, then crop the region of interest
		# from the image and display it
		if len(refPt) == 2:
			if fattoreScala != 1:
				r0 = list(refPt[0])
				r1 = list(refPt[1])
				'''
				print('***')
				print(r0[0])
				print(r0[1])
				print(r1[0])
				print(r1[1])
				'''	
				r0[0] = round(r0[0] * (1/(fattoreScala))) # ci andava 1 - fattoreScala nuovo
				r0[1] = round(r0[1] * (1/(fattoreScala)))
				r1[0] = round(r1[0] * (1/(fattoreScala)))
				r1[1] = round(r1[1] * (1/(fattoreScala)))
				refPt = [tuple(r0), tuple(r1)]
			# print(refPt) # nuovo
			return(refPt)
		else:
			return(False)

#########################################################################################################################################################################


def estraiEChiedi(video, titolo, ver, t = 15):
	loglevel = " -loglevel panic"
	tempo = time.strftime('%H:%M:%S', time.gmtime(t))

	if ver == True:
		loglevel = ""

	while True:
		# estrai il frame tot del video finche' l'utente dice che va bene
		try:
			subprocess.run('ffmpeg -i "%s" -ss %s %s -vframes 1 -y out.png' %(video, tempo, loglevel), check=True)
			# print('ffmpeg -i "%s" -ss %s %s -vframes 1 -y out.png' %(video, tempo, loglevel))
		except:
			return -1

		coordinate = selezionaRiquadroImmagine("out.png", titolo)
		if coordinate == False:
			return 1
		elif coordinate == "NV":
			return estraiEChiedi(video, titolo, ver, t + 15)
		else:
			return coordinate

def UI():
		try:
			os.system("cls")
		except:
			try:
				os.system("clear")
			except:
				pass
			pass
		erroreffmpeg = "ffmpeg ha avuto un problema, riprova con altre opzioni"
		
		descrizione = """
  -----------------------------------------------------------------------------------------
  |                                                                                       |
  |  Il programma prende in ingresso un video o una cartella                              |
  |  contenete uno o piu' video, estrae da ciascun video un frame ogni n secondi          |
  |  (vedere l'utilizzo dell'opzione --intervallo) e tenta di organizzare per             |
  |  numero di pagina i frame estratti ritagliando le immagini all'area specificata       |
  |  dall'utente e scegliendo sempre la versione piu' aggiornata di ogni frame fra        |
  |  quelle disponibili.                                                                  |
  |                                                                                       |
  |---------------------------------------------------------------------------------------|
  |                                                                                       |
  |  L'utente deve selezionare la regione frame che intende ritagliare e eventualmente    |
  |  la porzione contente il numero di pagina, in caso questa non fosse specificata       |
  |  verra' usata una regione di default.                                                 |
  |                                                                                       |
  |---------------------------------------------------------------------------------------|
  |                                                                                       |
  |  Una volta terminata l'esecuzione del programma e' consigliabile controllare nelle    |
  |  cartelle Non Classificate per accertarsi che il programma non abbia tralasciato      |
  |  pagine. Fatto cio' e' possibile eseguire il programma una seconda volta specificando |
  |  una cartella di immagini e l'opzione --convertiInPDF per trasformare le immagini     |
  |  nella cartella in un file PDF.                                                       |
  |                                                                                       |
  -----------------------------------------------------------------------------------------
		"""

		parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        		description=descrizione)
		printNormal(welcomeMessage)
		parser.add_argument("percorso",
				help="Specifica il percorso al video da bruteforceare oppure una cartella contenente piu' video. In questo caso verranno bruteforceati tutti i video presenti")

		parser.add_argument("-i", "--intervallo", 
				help="Ogni quanti secondi estrarre i frame dal video. Default = 10", type=int)

		parser.add_argument("-p", "--posizioneNumeroManuale", 
				help="Se settata l'utente puo' specificare manualmente la posizione del numero di pagina. Altrimenti viene utilizzata la posizione di default per le slide di STEA", action="store_true")

		parser.add_argument("-c", "--convertiInPDF", 
				help="Converte tutte le immagini nella cartella specificata in un unico file PDF", action="store_true")

		parser.add_argument("-v", "--verbose", 
				help="Regola il livello di output del programma", action="store_true")

		parser.add_argument("-s", "--sorpresa", 
				help="Sorpresa...", action="store_true")

		args = parser.parse_args()


		verbose = False
		if args.verbose:
			verbose = args.verbose

		videoDaElaborare = ""

		if args.convertiInPDF == True:
			if os.path.isdir(args.percorso):
				convertiInPDF(args.percorso)
			else:
				printError("Il percorso non e' una cartella") 			
			sys.exit(1)

		if os.path.isdir(args.percorso):
			for root, dirs, files in os.walk(args.percorso, topdown=True):
				for filename in files:
					if controllaEstensione(filename, "video") == True and os.path.isfile(root +'\\' + filename):
						printNormal("Uso " + filename + "\n")
						videoDaElaborare = root + '\\' + filename
						break

		elif os.path.isfile(args.percorso) and controllaEstensione(args.percorso, "video") == True:
			videoDaElaborare = args.percorso 
		if len(videoDaElaborare) == 0:
			printError("LA CARTELLA NON CONTIENE VIDEO O IL FORMATO NON E' SUPPORTATO\n")
			sys.exit(1)

		printGood("Seleziona l'area contenente la SLIDE e chiudi la finestra una volta finito (se la finestra non appare controlla che non sia in secondo piano)")
		printCyan("Premi 'R' sulla tastiera per selezionare un nuovo frame")
		time.sleep(2)

		coordinateSlide = estraiEChiedi(videoDaElaborare, "Area di interesse", verbose)
		coordinateNumeroPagina = ""

		if coordinateSlide == 1:
			printError("La selezione risulta vuota, esco\n")
			sys.exit(1)
		elif coordinateSlide == -1:
			printError(erroreffmpeg + "\n")
			sys.exit(1)

		if args.posizioneNumeroManuale == True:
			printGood("Seleziona l'area contenente il NUMERO DI PAGINA e chiudi la finestra una volta finito (se la finestra non appare controlla che non sia in secondo piano)")
			printCyan("Premi 'R' sulla tastiera per selezionare un nuovo frame")
			time.sleep(2)
			coordinateNumeroPagina = estraiEChiedi(videoDaElaborare, "Area numero pagina", verbose)
			if coordinateNumeroPagina == 1:
				printWarning("La selezione risulta vuota, uso i parametri di default\n")
				coordinateNumeroPagina = ""
			elif coordinateNumeroPagina == -1:
				printError(erroreffmpeg)
				sys.exit(1)
		
		percorso = args.percorso
		if not args.intervallo :
			intervallo = 10
		else:
			intervallo = args.intervallo

		if coordinateNumeroPagina == "":
			# non così coordinateNumeroPagina = [(950, 1700),(900, 1650)]  
			coordinateNumeroPagina = [(1650, 900),(1700, 950)]


		ris = [percorso, coordinateSlide, coordinateNumeroPagina, intervallo, verbose]
		time.sleep(2)
		if args.sorpresa:
			printSteaBW()
			# printStea()
			# printNormal("SE SONO APPARSI NUMERI A CASO MI SA CHE E' PERCHE' STAI USANDO ROBACCIA DI WINDOWS")
		return ris
