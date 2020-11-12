import os, cv2, pytesseract, shutil, sys,re
import UIstea as gui
from utilityStea import controllaEstensione, printError, printWarning, printGood, printInfo, printMagenta, printCyan, printNormal
from progress.bar import IncrementalBar

#########################################################################
#################### VARIABILI ##########################################
#########################################################################


# nomeFilePercorsoTesseract = os.path.dirname(os.path.realpath(__file__)) + "\\pathTesseract.txt"
nomeFilePercorsoTesseract = "pathTesseract.txt"

# faccio in modo che il file contentente il percorso a tesseract venga trovato indipendentemente da come e dove
#   viene eseguito questo script

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

nomeFilePercorsoTesseract = os.path.join(application_path, nomeFilePercorsoTesseract)

try:
    percorsoTesseract = open(nomeFilePercorsoTesseract, "r").read().partition('\n')[0]
    pytesseract.pytesseract.tesseract_cmd = percorsoTesseract
except FileNotFoundError:
    printError("pathTesseract.txt non e' stato trovato. Controlla che sia nella stessa cartella dell'eseguibile")
    sys.exit(1)

coordsSlide1 = 0
coordsSlide2 = 0
coordsSlide3 = 0
coordsSlide4 = 0
coordsNumeroPagina1 = 0
coordsNumeroPagina2 = 0
coordsNumeroPagina3 = 0
coordsNumeroPagina4 = 0
verbosity = False

########################################################################
############ FUNZIONI DI CONTROLLO E GESTIONE ##########################
########################################################################

def ritagliaImmaginiInCartella(cartella):

    if not os.path.isdir(cartella):
        printMagenta("Non e' una cartella")
    else:
        for root, dirs, files in os.walk(cartella, topdown=True):
            for filename in files:
                if controllaEstensione(filename, "immagine") and os.path.isfile(root +'\\'+ filename):
                    try:
                        image = cv2.imread(cartella +'\\'+ filename)
                        '''
                        print(coordsSlide2)
                        print(coordsSlide4)
                        print(coordsSlide1)
                        print(coordsSlide3)
                        '''
                        cropped = image[coordsSlide2:coordsSlide4, coordsSlide1:coordsSlide3]
                        nomeFile = re.split("([\d\w_?\-. \(\)]+).(..[\d\w]+)", filename)[1]
                        cv2.imwrite(root +'\\'+ nomeFile + ".jpg", cropped)
                    except TypeError:
                        pass

def controlloNumero(arrText):
    txt = arrText.split()
    for elem in txt:
        if elem.isdigit():
            return int(elem)
    return 'NC'

def most_frequent(List):
    return max(set(List), key = List.count)

def trovaPaginaSlide(percorso_foto):
    #print(percorso_foto)
    img = cv2.imread(percorso_foto)
    height, width, _ = img.shape
    '''
    print(img.shape)
    print("coords!!!! ----> ",  coordsNumeroPagina1) # nuovo
    print(coordsNumeroPagina1)
    print(coordsNumeroPagina2)
    print(coordsNumeroPagina3)
    print(coordsNumeroPagina4)
    '''    
    roi = img[coordsNumeroPagina2:coordsNumeroPagina4,coordsNumeroPagina1:coordsNumeroPagina3]
    '''
    print()
    print(roi.shape) # nuovo 
    '''
    try:  
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 5)
        adaptive_mean = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    except cv2.error: 
        printMagenta("\n Sembra che l'area del numero di pagina sia fuori dall'immagine. Se hai utilizzato l'opzione di default prova con quella manuale, senno' riprova comunque")
        sys.exit(1)
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    try:
        arr_adaptive_threshold = pytesseract.image_to_string(adaptive_threshold, config=custom_config) # 1. adaptive
        arr_gray = pytesseract.image_to_string(gray, config=custom_config) # 2. scala di grigi
        arr_img = pytesseract.image_to_string(roi, config=custom_config) # 3. normale
        arr_adaptive_mean = pytesseract.image_to_string(adaptive_mean,config=custom_config) #4. mean inverso
    except KeyboardInterrupt:
        raise
    except:
        printMagenta("\nTesseract non e' stato trovato, controlla di averlo installato e che il percorso " + nomeFilePercorsoTesseract + " sia corretto")
        sys.exit(1)


    arr_metodi = []
    arr_metodi.append(controlloNumero(arr_img))
    arr_metodi.append(controlloNumero(arr_gray))
    arr_metodi.append(controlloNumero(arr_adaptive_threshold))
    arr_metodi.append(controlloNumero(arr_adaptive_mean))

    return most_frequent(arr_metodi)


def organizzaSlide(cartella_lezioni,cartella_frame,nome_lezione):

    pathSlides = cartella_frame + '\\' + nome_lezione # quindi prendo la cartella della lezione in temp

    tutteClassificate = []
    tutteNonclassificate = []

    with IncrementalBar('', max=len(os.listdir(pathSlides)), suffix='%(index)d/%(max)d [%(elapsed_td)s/%(eta_td)s]') as bar:
        for i,nome_file in enumerate(os.listdir(pathSlides)):
            bar.next()
        
            numeroP = trovaPaginaSlide(pathSlides+'\\'+nome_file)

            if(numeroP == 'NC'):
                numeroP = numeroP + str(i)

            elemento = {
                "nomeFile" : nome_file,
                "numeroPagina" : numeroP
            }

            if type(elemento["numeroPagina"]) is str:
                tutteNonclassificate.append(elemento)
            else:
                tutteClassificate.append(elemento)
        bar.finish()
        printNormal('')

    # GESTISCO LE PAGINE NON CLASSIFICATE
    pathFrameLezione = cartella_frame + '\\' + nome_lezione
    pathSlideLezioneNC = cartella_lezioni + '\\' + 'Slides' + '\\' + nome_lezione + '\\' + 'nonClassificate'

    try:
        os.mkdir(pathSlideLezioneNC)
    except FileExistsError:
        pass
    '''
    printNormal("newFolderPath1   " + pathFrameLezione)
    printNormal("newFolderPath2   " + pathSlideLezioneNC)
    printNormal("nome_lezione   " + nome_lezione)
    '''
    spostaSlide(tutteNonclassificate,pathFrameLezione,pathSlideLezioneNC)

    # GESTISCO LE CLASSIFICATE
    tutteClassificate.sort(key=lambda x: x["numeroPagina"]) # sort per numero pagina crescente

    return tutteClassificate

def prendiUltimeSlide(listSlide):
    aggiornate = []
    try:
        ultimaAggiornata = listSlide[0]
        ultimaPagina = listSlide[0]["numeroPagina"]
    except IndexError:
        return False

    for i in listSlide:
        if ultimaPagina != i["numeroPagina"]:
            aggiornate.append(ultimaAggiornata)
        ultimaAggiornata = i
        ultimaPagina = i["numeroPagina"]
    aggiornate.append(listSlide[-1])

    return aggiornate

def spostaSlide(slideDaPrendere, pathSorgente, nuovaPathDest):
    numeroSlide = 0
    for item in slideDaPrendere:
    numeroSlide = numeroSlide + 1
        nome = item['nomeFile']
        pg = item['numeroPagina']
        shutil.move(pathSorgente + '\\' + nome, nuovaPathDest + '\\' + str(pg) + '.jpg')
        
    printCyan("Sposto ", numeroSlide, " Slide in:  "+ nuovaPathDest)

#********************************* FUNZIONI FFMPEG E MAIN OCR *************************************************

def doFFMPEG(secondi,filenamePath,cartella_frame):
    nome = os.path.splitext(os.path.basename(filenamePath))[0]
    newPath = cartella_frame + "\\" + nome # nuova cartella col nome del video dove metto i frame della lezione

    loglevel = "-loglevel panic"
    if verbosity == True:
        loglevel = ""

    try:
       os.mkdir(newPath)
    except FileExistsError:
       pass

    if len(os.listdir(newPath)) == 0:
       printCyan("Sto elaborando i frame della lezione "+nome+"...")
       os.system('ffmpeg -ss 00:00:00 -i "%s" -start_number 0 %s -vf fps=1/%s "%s\out_%%03d.jpg" ' %(filenamePath, loglevel, secondi, newPath)) #% e.g. -r 1/25 1 frame ogni 25 secondi
    else:
       printWarning("La cartella per " + nome + " c'e' gia' e non e' vuota, quindi passo oltre.")


def estraiFrames(secondi, cartella_lezioni, cartella_frame):
    # creo cartella TEMP
    try:
        os.mkdir(cartella_frame)
    except FileExistsError:
        pass

    if os.path.isfile(cartella_lezioni): # cartella_lezioni e' un VIDEO
        doFFMPEG(secondi,cartella_lezioni,cartella_frame)
    else:    # cartella_lezioni e' una CARTELLA
        for filename in os.listdir(cartella_lezioni):
            if (controllaEstensione(filename, "video")):
                filenamePath = cartella_lezioni + "\\" + filename # prendo il path del video
                doFFMPEG(secondi,filenamePath,cartella_frame)

def doOCR(cartella_lezioni,cartella_frame,dataLezione,pathSlideLezioni):
    pathLezione = cartella_frame + '\\' + dataLezione # la cartella che contiene i frame della lezione
    if os.path.isdir(pathLezione):
        printCyan("Sto organizzando la lezione " + dataLezione + ".\nMettiti comodo, leggi un libro e fatti un bel tè caldo. Ci vorra un po'.\n")
        pathSlideLezione = pathSlideLezioni + '\\' + dataLezione
        # printNormal("pathSlideLezione    " + pathSlideLezione)
        try:
            os.mkdir(pathSlideLezione)
        except FileExistsError:
            if len(os.listdir(pathSlideLezione)) == 0:
                pass
            else:
                printWarning("La cartella per "+ dataLezione + " c'e' gia' e non e' vuota, quindi passo oltre.")

        slide1 = organizzaSlide(cartella_lezioni,cartella_frame,dataLezione)
        slide2 = prendiUltimeSlide(slide1)
        if slide2 == False:
            printError("\n C'e' stato un problema con le Slide di "+ dataLezione + "!\nControlla che non siano quelle di esercitazione Assembly e nel caso toglile, non ci sono slide e al programma questa cosa non piace\n") # se slide2 è false, quindi c'è stato qualche problema
        else:
            spostaSlide(slide2, pathLezione, pathSlideLezione)
            # printNormal(pathSlideLezione)
            ritagliaImmaginiInCartella(pathSlideLezione)
            ritagliaImmaginiInCartella(pathSlideLezione+'\\'+'NonClassificate')

def slideOCR(cartella_lezioni, cartella_frame):
    dirname,name = os.path.split(cartella_lezioni)
    filename = os.path.splitext(os.path.basename(cartella_lezioni))[0]

    if os.path.isfile(cartella_lezioni):
        pathSlideLezioni = dirname + '\\' + 'Slides' # destinatario
    else:
        pathSlideLezioni = cartella_lezioni + '\\' + 'Slides'

    # crea cartella per le Slide di tutte le lezioni
    try:
        os.mkdir(pathSlideLezioni)
    except FileExistsError:
        pass  

    if os.path.isfile(cartella_lezioni):
        doOCR(dirname,cartella_frame,filename,pathSlideLezioni)
    else:
        for dataLezione in os.listdir(cartella_frame): # dataLezione e' il nome della cartella (e.g. "2020-10-08 (1)")
            doOCR(cartella_lezioni,cartella_frame,dataLezione,pathSlideLezioni)
      
def controllaTesseract():

    if not os.path.isfile(percorsoTesseract):
        printError("\nSembra che tu non abbia installato Tessract o che il percorso specificato in " + percorsoTesseract +" non sia valido, controlla e riprova\n")
        sys.exit(1)

############################### MAIN ############################### 
def main():
    controllaTesseract()
    ris = gui.UI()
# print(ris)
    pathOL              = ris[0]
# printNormal(ris)
# printNormal(coordsSlide)

    global verbosity
    global coordsSlide1
    global coordsSlide2
    global coordsSlide3
    global coordsSlide4
    global coordsNumeroPagina1
    global coordsNumeroPagina2
    global coordsNumeroPagina3
    global coordsNumeroPagina4 
    
    coordsSlide1 = ris[1][0][0]
    coordsSlide2 = ris[1][0][1]
    coordsSlide3 = ris[1][1][0]
    coordsSlide4 = ris[1][1][1]
    coordsNumeroPagina1 = ris[2][0][0]
    coordsNumeroPagina2 = ris[2][0][1]
    coordsNumeroPagina3 = ris[2][1][0]
    coordsNumeroPagina4 = ris[2][1][1]

    tempo               = ris[3]
    verbosity           = ris[4]

    '''
    printNormal("pathOL            " + str(pathOL))
    printNormal("coordsSlide       " + str(coordsSlide))
    printNormal("coordsSlide1       " + str(coordsSlide1))
    printNormal("coordsSlide2      " + str(coordsSlide2))
    printNormal("coordsSlide3       " + str(coordsSlide3))
    printNormal("coordsSlide4       " + str(coordsSlide4))
    #printNormal("coordsNumeroPagina" + str(coordsNumeroPagina))
    printNormal("tempo             " + str(tempo))
    '''

    if os.path.isfile(pathOL): # se e' un file allora lo splitto col nome e do il percorso al file
        dirname,filename = os.path.split(pathOL)
        pathFrameLezioni = dirname + '\\' + 'temp'   # conterrà tutti i frame da elaborare
    else:   
        pathFrameLezioni = pathOL + '\\' + 'temp'   # conterrà tutti i frame da elaborare
 
   
    # SECONDA PARTE - ESTRAGGO FRAME
    estraiFrames(tempo,pathOL,pathFrameLezioni)
    # TERZA ED ULTIMA - LE ORGANIZZO E SALVO
    slideOCR(pathOL,pathFrameLezioni)

    printGood("Ho fatto tutto, non ti resta che controllare e sistemare le Non Classificate e creare il pdf delle slide.\n Se vuoi puoi cancellare la cartella \"temp\"")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
