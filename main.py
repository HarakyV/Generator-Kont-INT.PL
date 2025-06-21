import sys
import customtkinter
import threading
from PIL import Image, ImageTk
import os
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import random
from CTkMessagebox import CTkMessagebox



now = datetime.now()
sys.stdout.reconfigure(encoding='utf-8')
# Ładowanie plików
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
def resource_path(relative_path):
    print(f"Wykryto Sciezke: " + os.path.join(SCRIPT_DIR, relative_path))
    return os.path.join(SCRIPT_DIR, relative_path)
#-----------------

#Wartośći Ekranu 

deafultScreen = customtkinter.CTk()
deafultScreen.title("INT.PL - Selenium Generator Kont")
deafultScreen.geometry("1000x500")
iconpath = "img/ico.ico"
deafultScreen.iconbitmap(resource_path(iconpath))
#--------------

#Utworzenie Ekranów
frameMain = customtkinter.CTkFrame(deafultScreen)
frameConfig = customtkinter.CTkFrame(deafultScreen)
frameInfo = customtkinter.CTkFrame(deafultScreen)

#Przełączanie Ekranów

def pokazGlowny():
    frameConfig.grid_forget()
    frameInfo.grid_forget()
    frameMain.grid(row=0, column=0, sticky="nsew")

def pokazKonfiguracja():
    frameMain.grid_forget()
    frameConfig.grid(row=0, column=0, sticky="nsew")

def pokazInfo():
    os.system("start info.txt")

#-------------
#Program tworzący konta


def startAccountCreation():
    #Blokowanie przycisku
    przyciskStart.configure(state="disabled")
    #Dodawnie Informacji do LogsBoxa\
    now = datetime.now()
    logsBox.configure(state="normal")
    logsBox.insert("end","\nUruchomiono program tworzący konta : " + now.strftime("%H:%M:%S"))

    #Czytanie config.txt
    config_read = {}
    with open("config.txt","r") as przeczytacz:
        for linia in przeczytacz:
            linia = linia.strip()
            if linia == "":
                continue
            klucz,wartosc = linia.split("=")
            klucz = klucz.strip()
            wartosc = wartosc.strip()
            config_read[klucz] = wartosc    

    
    #Zamienainie stringow na int
    accounts_number = int(config_read["accountsNumber"])
    passwordLenghtInt = int(config_read["pswLen"])
    loginLenghtInt = int(config_read["loginLen"])

    print("ChromedriverPath: " + config_read["chromedriverpath"])
    print("saveaccounts:" + config_read["saveAccounts"])
    print("accountsNumber: " + config_read["accountsNumber"])
    print("timeLogged: " + config_read["timeLogged"])
    print(f"Password Lenght: {passwordLenghtInt}")
    print(f"Login Lenght: {loginLenghtInt}")

    

    #Dodwanie Informacji do logsboxa
    now = datetime.now()
    logsBox.insert("end","\nPrzeczytano Config.txt : " + now.strftime("%H:%M:%S"))

    #Rozpoczynanie tworzenia konta w pętli zaleznej od accounts_number
    now = datetime.now()
    logsBox.insert("end","\nRozpoczynanie tworzenia kont/konta : " + now.strftime("%H:%M:%S"))
    logsBox.insert("end",f"\nLiczba Kont: {accounts_number} ")

    #Konfiguracja Webdrivera

    browserOption = Options()
    if checkBox_headless_var.get() == "off":
        browserOption.add_argument("--headless")
    service = Service(config_read["chromedriverpath"])
    
    

    def start_petli():

        #Dane do generowania Loginow i hasel
        litery = "abcdez"
        litery_up = "ABCDEFGHIJKTUWXYZ"
        cyfry = "1234567890"
        combined = litery + litery_up + cyfry
        combined_bez_cyfr = litery + litery_up


        #Losowanie Hasła i Loginu
        def generatePasswords(loginLenght=loginLenghtInt,passwordLenght=passwordLenghtInt):
            global randomLogin
            global randomPassword
            randomLogin = ""
            randomPassword = ""
            
            for _ in range(loginLenght):
                losowanieLoginu = random.choice(combined_bez_cyfr)
                randomLogin += losowanieLoginu
            randomPassword += random.choice(cyfry)
            print(f"Wygenerowany Login: " + randomLogin)

            for _ in range(passwordLenght):
                losowanieHasla = random.choice(combined)
                randomPassword += losowanieHasla
            print(f"Wygenerowane Hasło: " + randomPassword)

        # Pętla tworzenia kont / konta
        for i in range(accounts_number):
            #Wygenerowanie Hasła
            generatePasswords()
            #Ładowanie strony do tworzenia konta
            browserRun = webdriver.Chrome(service=service, options=browserOption)
            browserRun.get("https://int.pl/#/register")
            time.sleep(0.5)
            #Wpisanie loginu
            wpiszLogin = browserRun.find_element(By.ID,"loginId")
            wpiszLogin.click()
            wpiszLogin.send_keys(randomLogin)
            time.sleep(0.5)
            #Wpisanie hasła
            wpiszHaslo1 = browserRun.find_element(By.ID,"passwordId")
            wpiszHaslo1.click()
            wpiszHaslo1.send_keys(randomPassword)
            time.sleep(0.5)
            #Powtórzenie Hasła
            wpiszHaslo2 = browserRun.find_element(By.CSS_SELECTOR, "input[ng-model='regData[inputs.rePassword]']")
            wpiszHaslo2.click()
            wpiszHaslo2.send_keys(randomPassword)
            #Zamknięcie ciasteczek
            ciasteczka = browserRun.find_element(By.CLASS_NAME , "cookie-policy-close")
            ciasteczka.click()
            #Zaakceptowanie Regulaminu (Klikniecie javascriptem bo jest schowany ten checkbox jakby)
            label = browserRun.find_element(By.CSS_SELECTOR, 'label[for="portalRulesId"]')
            browserRun.execute_script("arguments[0].click();", label)
            #Scroll w dół do przycisku załóż konto (javascript)
            browserRun.execute_script("window.scrollTo({ top: 500, behavior: 'auto' });")
            time.sleep(0.5)
            #Nacisnięcie przycisku zakładam konto
            zakladamKonto = browserRun.find_element(By.CSS_SELECTOR, ".button.button--left.button--mark.button--moema.ng-scope")
            zakladamKonto.click()
            time.sleep(4)

            #Koniec procesu tworzenia konta

            #Zapisywanie do accounts.txt jezeli uzytkownik tak chce w configu
            if config_read["saveAccounts"] == "tak":
                with open("accounts.txt", "a") as saveacc:
                    saveacc.seek(0, 2)  # przejdź na koniec pliku
                    if saveacc.tell() != 0:
                        saveacc.write("\n")  # jeśli plik NIE jest pusty, dodaj nową linię
                    saveacc.write(f"{randomLogin}@int.pl\n{randomPassword}\n------------")
                    saveacc.close() 
            else:
                print(f"Save Accounts jest ustawione na: " , config_read["saveAccounts"])
            logsBox.insert("end",f"\n---------\nWygenerowano konto\nLogin:{randomLogin + "@int.pl"}\nPassword:{randomPassword}")
            browserRun.quit()

        #Uruchamianie przicisku na nowo po zakonczenia loopa
        przyciskStart.configure(state="enabled")

    threadLoop = threading.Thread(target=start_petli)
    threadLoop.start()
#--------------

#Program logujacy sie na konto
def logIn():
    #Czytanie config.txt
    config_read = {}
    with open("config.txt","r") as przeczytacz:
        for linia in przeczytacz:
            linia = linia.strip()
            if linia == "":
                continue
            klucz,wartosc = linia.split("=")
            klucz = klucz.strip()
            wartosc = wartosc.strip()
            config_read[klucz] = wartosc
    time_logged = int(config_read["timeLogged"])
    print("ChromedriverPath: " + config_read["chromedriverpath"])
    print(f"Czas zalogowany: {time_logged}")

    #Czytanie pliku accounts.txt (loginu i hasla pierwszego konta z gory)
    with open("accounts.txt","r") as read_acc:
        liniaLogin = read_acc.readline()
        liniaHaslo = read_acc.readline()
        print(f"Login: {liniaLogin}")
        print(f"Haslo: {liniaHaslo}")


    #Usuwanie maila na którego będziemy sie logować
    with open("accounts.txt","r") as delete_accs:
        linie = delete_accs.readlines()
    resztaLinie = linie[3:]
    with open("accounts.txt","w") as delete_accs1:
        delete_accs1.writelines(resztaLinie)

    #Rozpoczynanie Procesu Logowania
    logsBox.configure(state="normal")
    logsBox.insert("end","\nDane konta do logowania")
    logsBox.insert("end","\nLogin: " + liniaLogin)
    logsBox.insert("end","\nHaslo" + liniaHaslo)


    #Startowanie Logowania

    browserOption = Options()
    service = Service(config_read["chromedriverpath"])

    browserRun = webdriver.Chrome(service=service, options=browserOption)
    browserRun.get("https://int.pl/#/login-clear")
    #Dodano Delay dla załadowania
    time.sleep(2.5)
    #Wpisywanie Loginu
    wpiszLoginSinco = browserRun.find_element(By.ID , "emailId")
    wpiszLoginSinco.click()
    wpiszLoginSinco.send_keys(liniaLogin)
    time.sleep(0.5)
    #Wpisywanie Hasla
    wpiszHasloTrinco = browserRun.find_element(By.ID,"passwordId")
    wpiszHasloTrinco.click()
    wpiszHasloTrinco.send_keys(liniaHaslo)
    time.sleep(0.5)
    #Klikanie przycisku zaloguj sie
    zalogujSie = browserRun.find_element(By.XPATH, "//*[text()='loguję się']")
    zalogujSie.click()
    time.sleep(3)  #Większy delay zeby sie załadowała poczta
    #Klikniecie komunikatu przejdz do poczty

    przejdzDoPoczty = browserRun.find_element(By.XPATH , "//*[text()='Przejdź do poczty']")   
    przejdzDoPoczty.click()

    #Powiadomienie
    CTkMessagebox(title="Komunikat", message="Po zakonczeniu uzywania e-maila zamknij przegladarke")
    #Zakonczony proces logowania   
    


  
def logInThread():
    threadLoop = threading.Thread(target=logIn)
    threadLoop.start()

#--------------



#Główny Ekran

logsBoxLabel = customtkinter.CTkLabel(frameMain,text="Logi",font=("Comic Sans MS",25),text_color="Lime")
logsBoxLabel.grid(row=0, column=1, padx=700, pady=(15, 20))
logsBox = customtkinter.CTkTextbox(frameMain,width=300,height=200)
logsBox.insert("end","Uruchomiono program : " + now.strftime("%H:%M:%S"))
logsBox.configure(state="normal")
logsBox.grid(row=1, column=1, padx=700, pady=(30, 20), sticky="w")


# Przyciski Ekran Główny
przyciskConfig = customtkinter.CTkButton(frameMain,text="Konfiguruj Wartości",text_color="lime",font=("Comic Sans MS",12),command=pokazKonfiguracja)
przyciskConfig.grid(row=0, column=1, padx=50, pady=(15, 20), sticky="w")

przyciskStart = customtkinter.CTkButton(frameMain,text="Wystartuj program tworzący",text_color="red",font=("Comic Sans MS",12),command=startAccountCreation)
przyciskStart.grid(row=0, column=1, padx=50, pady=(75, 20), sticky="w")

przyciskLogin = customtkinter.CTkButton(frameMain,text="Uruchom program logujacy sie",text_color="yellow",font=("Comic Sans MS",12),command=logInThread)
przyciskLogin.grid(row=0, column=1, padx=50, pady=(150, 20), sticky="w")

przyciskInfo = customtkinter.CTkButton(frameMain,text="Przeczytaj o programie",font=("Comic Sans MS",12),command=pokazInfo)
przyciskInfo.grid(row=0, column=1, padx=50, pady=(225, 20), sticky="w")

checkBox_headless_var = customtkinter.StringVar(value="off")
def checkBox_headless_event():
    print("Zmienione headless check na: ", checkBox_headless_var.get())

checkBox_headless = customtkinter.CTkCheckBox(frameMain,text="Pokazac przegladarke podczas tworzenia kont?",text_color="Blue",command=checkBox_headless_event,variable=checkBox_headless_var,onvalue="on", offvalue="off")
checkBox_headless.grid(row=0, column=0, columnspan=3, pady=(20, 20), sticky="n")

#----------------

#Ekran Info

powrotDoMenu = customtkinter.CTkButton(frameInfo,text="Powrót Do Menu ",text_color="lime",font=("Comic Sans MS",15),command=pokazGlowny)
powrotDoMenu.grid()



#----------------
#Ekran Config

powrotDoMenu = customtkinter.CTkButton(frameConfig,text="Powrót Do Menu ",text_color="lime",font=("Comic Sans MS",15),command=pokazGlowny)
powrotDoMenu.grid()

check_var_acc = customtkinter.BooleanVar(value=False)
saveAccountsCheckBox = customtkinter.CTkCheckBox(frameConfig,text="Zapisywać Konta w accounts.txt?",text_color="lime",font=("Comic Sans MS",15), variable=check_var_acc)
saveAccountsCheckBox.grid(padx=30)

chromedriverPathLabel = customtkinter.CTkLabel(frameConfig,text="Podaj scieżke do chromedrivera: ⏬",text_color="lime",font=("Comic Sans MS",15))
chromedriverPathLabel.grid(padx=50,pady=10)

chromedriverPathEntry = customtkinter.CTkEntry(frameConfig,text_color="lime")
chromedriverPathEntry.grid(padx=140)

accountsNumberLabel = customtkinter.CTkLabel(frameConfig,text="Ile kont chcesz tworzyć na raz? ⏬ ",text_color="lime",font=("Comic Sans MS",15))
accountsNumberLabel.grid(padx=140)

accountsNumberEntry = customtkinter.CTkEntry(frameConfig,text_color="lime")
accountsNumberEntry.grid(pady=5)


loggedTimeLabel = customtkinter.CTkLabel(frameConfig,text="Ile czasu chcesz pozostawać na zalogowanych kontach?⏬ ",text_color="lime",font=("Comic Sans MS",15))
loggedTimeLabel.grid(pady=5)

loggedTimeEntry = customtkinter.CTkEntry(frameConfig,text_color="lime")
loggedTimeEntry.grid(pady=5)

loginLenghtLabel =  customtkinter.CTkLabel(frameConfig,text="Ile znakowe loginy maja być generowane? (minimum 7 max 32) ",text_color="lime",font=("Comic Sans MS",15))
loginLenghtLabel.grid(pady=5)

loginLenghtEntry = customtkinter.CTkEntry(frameConfig,text_color="lime")
loginLenghtEntry.grid(pady=5)

passwordLenghtLabel = customtkinter.CTkLabel(frameConfig,text="Ile znakowe hasla maja być generowane? (minimum 13 max 32) ",text_color="lime",font=("Comic Sans MS",15))
passwordLenghtLabel.grid(pady=5)

passwordLenghtEntry = customtkinter.CTkEntry(frameConfig,text_color="lime")
passwordLenghtEntry.grid(pady=5)



def deafultValuesCommand():
    logsBox.configure(state="normal")
    now = datetime.now()
    logsBox.insert("end","\nPokazano Domyślne wartości : " + now.strftime("%H:%M:%S"))

    CTkMessagebox(title="Domyślne Wartości", message="Zapisywać konta: ✔\nChromeDriverPath: chromedriver.exe\nIlość kont na raz: 1\nCzas na zalogowanych kontach: 120", width=500, option_1="Zamknij")
    



    


deafultValues = customtkinter.CTkButton(frameConfig,text="Pokaż Domyślne wartośći",text_color="lime",font=("Comic Sans MS",15),command=deafultValuesCommand)
deafultValues.grid(column=1,row=2)


warningLabel = customtkinter.CTkLabel(frameConfig,text="Przed zapisaniem wypełnij wszystkie pola! ",text_color="red",font=("Comic Sans MS",25))
warningLabel.grid(pady=5)

def saveConfig():
    #Pobieranie Entry
    chromedriverPathEntryGet = chromedriverPathEntry.get()
    accountsNumberEntryGet = accountsNumberEntry.get()
    loggedTimeEntryGet = loggedTimeEntry.get()
    loginLenghtEntryGet = loginLenghtEntry.get()
    passwordLenghtEntryGet = passwordLenghtEntry.get()

    #Zapisywanie Configu
    config = {
        "saveAccounts": "tak" if check_var_acc.get() else "nie",
        "chromedriverpath": chromedriverPathEntryGet,
        "accountsNumber": accountsNumberEntryGet,
        "timeLogged": loggedTimeEntryGet,
        "pswLen": passwordLenghtEntryGet,
        "loginLen": loginLenghtEntryGet,
    }
    with open("config.txt","w") as config_file:
        for klucz, wartosc in config.items():
            config_file.write(f"{klucz} = {wartosc}\n")
        
        logsBox.configure(state="normal")
        now = datetime.now()
        logsBox.insert("end","\nZapisano Config do pliku config.txt : " + now.strftime("%H:%M:%S"))

    

saveConfigButton = customtkinter.CTkButton(frameConfig,text="Zapisz Config",text_color="red",font=("Comic Sans MS",15),command=saveConfig)
saveConfigButton.grid(pady=5)
















pokazGlowny()
deafultScreen.mainloop()
