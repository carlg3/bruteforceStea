from colorama import init, Fore, Style
from PIL import Image
import os, sys

def printError(s):
	init()
	print(Fore.RED,s)
	print(Style.RESET_ALL)

def printNormal(s):
	init()
	print(Fore.WHITE,s)
	print(Style.RESET_ALL)

def printWarning(s):
	init()
	print(Fore.YELLOW , s)
	print(Style.RESET_ALL)

def printGood(s):
	init()
	print(Fore.GREEN , s)
	print(Style.RESET_ALL)


def printInfo(s):
	init()
	print(Fore.BLUE , s)
	print(Style.RESET_ALL)

def printMagenta(s):
	init()
	print(Fore.MAGENTA , s)
	print(Style.RESET_ALL)

def printCyan(s):
	init()
	print(Fore.CYAN , s)
	print(Style.RESET_ALL)

def controllaEstensione(s, tipo):
	estensioniVideoSupportate = [".mkv", ".mp4"]
	estensioniImmaginiSupportate = [".jpg", ".png"]

	if tipo == "video":
		estensioni = estensioniVideoSupportate
	elif tipo == "immagine":
		estensioni = estensioniImmaginiSupportate
	else:
		return None
	for e in estensioni:
		if s.endswith(e):
			return True
	return False


def convertiInPDF(cartella):
		cartella = sys.argv[1]
		listaImmagini = []
		nomePDF = "slides"
		if not os.path.isdir(cartella):
			printError("Il percorso non e' una cartella")
		else:
			for root, dirs, files in os.walk(cartella, topdown=True):
				for filename in files:
					if controllaEstensione(filename, "immagine") and os.path.isfile(cartella + "\\" + filename):
						immagine = Image.open(r'' + cartella + "\\" + filename)
						immagineConvertita = immagine.convert('RGB')
						listaImmagini.append(immagineConvertita)

		listaImmagini[0].save(r'' + cartella + "\\" + nomePDF +'.pdf', save_all=True, append_images=listaImmagini)
