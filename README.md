# bruteforceStea


                                                                            
## Cos'è?                                                                             
                                                                            
Un programma per prendere le slide che vengono mostrate a video durante le lezioni.       
                                                                            
## Come funziona?                                                                    
                                                                            
Il programma prende in ingresso un video o una cartella contenete uno o più video, estrae da ciascun video un frame ogni n-secondi (vedere l'utilizzo dell'opzione --intervallo) e tenta di organizzare per numero di pagina i frame estratti ritagliando le immagini all'area specificata dall'utente e scegliendo sempre la versione più aggiornata di ogni frame fra quelle disponibili.                                                               
                                                                            
----------------------------------------------------------------------------------
                                                                            
L'utente deve selezionare la regione frame che intende ritagliare e eventualmente la porzione contente il numero di pagina, in caso questa non fosse specificata verrà usata una regione di default (valida per i video di Microsoft Stream).                                    
                                                                            
----------------------------------------------------------------------------------
                                                                            
Una volta terminata l'esecuzione del programma è consigliato controllare nelle cartelle NonClassificate per accertarsi che il programma non abbia tralasciato pagine.
Fatto ciò è possibile eseguire il programma una seconda volta specificando una cartella di immagini e l'opzione --convertiInPDF per trasformare le immagini nella cartella in un file PDF.                                                    
                                                                            
----------------------------------------------------------------------------------

## Come lo uso?
Scarica ed installa Tesseract da [qui](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe) e inserisci in pathTesseract.txt il percorso dov'è installato.
Puoi optare dopo per una di queste tre scelte:
* Scaricare bruteforceStea.exe dalla repo. *__(scelta consigliata)__* ed usare da CMD:
```
bruteforceStea.exe
```
* Clonare la repo ed usare:
```
python bruteforceStea.py "path/to/video"
```
* Compilare l'exe, dopo aver correttamente installato i moduli che bruteforceStea usa, con:
```
pyinstaller -c -F bruteforceStea.py
```
*__IMPORTANTE__*: Fare doppio click sull'exe non funziona, deve essere eseguito da terminale 
### Aggiungere l'eseguibile a Path
Per poter eseguire il programma senza doversi necessariamente trovare nella cartella che lo contiene è possibile aggiungerlo alla variabile d'ambiente "Path", assicurandosi che il file "pathTesseract.txt" si trovi sempre nella stessa cartella dell'eseguibile.
#### Windows
Pannello di controllo -> Sistema e sicurezza -> Sistema -> Impostazioni di sistema avanzate -> Variabili d'ambiente.

Cliccare su Path, poi su Modifica e su Nuovo. Incollare nella cartella di testo il percoros completo alla cartella contenente l'eseguibile (e pathTesseract.txt)

-----------------------------------------------------------------------------------

Passa al programma l'argomento -h per maggiori info sui comandi!  
