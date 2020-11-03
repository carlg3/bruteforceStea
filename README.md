# bruteforceStea


                                                                            
## Cos'è?                                                                             
                                                                            
Un programma per prendere le slide che mostrano a video durante le lezioni.       
                                                                            
## Come funziona?                                                                    
                                                                            
Il programma prende in ingresso un video o una cartella contenete uno o piu' video, estrae da ciascun video un frame ogni n secondi (vedere l'utilizzo dell'opzione --intervallo) e tenta di organizzare per numero di pagina i frame estratti ritagliando le immagini all'area specificata dall'utente e scegliendo sempre la versione piu' aggiornata di ogni frame fra quelle disponibili.                                                               
                                                                            
----------------------------------------------------------------------------------
                                                                            
L'utente deve selezionare la regione frame che intende ritagliare e eventualmente la porzione contente il numero di pagina, in caso questa non fosse specificata verra' usata una regione di default.                                              
                                                                            
----------------------------------------------------------------------------------
                                                                            
Una volta terminata l'esecuzione del programma e' consigliabile controllare nelle cartelle Non Classificate per accertarsi che il programma non abbia tralasciato pagine.
Fatto cio' e' possibile eseguire il programma una seconda volta specificando una cartella di immagini e l'opzione --convertiInPDF per trasformare le immagini nella cartella in un file PDF.                                                    
                                                                            
----------------------------------------------------------------------------------

## Come lo uso?

Puoi:
* Scaricare l'exe dalla repo.
* Clonare la repo ed usare:
```
python bruteforceStea.py "path/to/video"
```
* Compilare l'exe, dopo aver correttamente installato i moduli che bruteforceStea usa, con:
```
pyinstaller -c -F bruteforceStea.py
```
-----------------------------------------------------------------------------------

Passa al programma l'argomento -h per maggiori info sui comandi!  
