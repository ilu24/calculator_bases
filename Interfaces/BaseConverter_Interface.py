#BaseConverter_Interface.py
###########################
# Importation des modules utiles
from tkinter import messagebox
import tkinter as tk
VALUES = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#Dictionnaire des options pour les menus
OPTIONS = {
    "Binary (2)" : 2,
    "Trinary (3)" : 3,
    "Quarternary (4)" : 4,
    "Quinary (5)" : 5,
    "Seximal (6)" : 6,
    "Septimal (7)" : 7,
    "Octal (8)" : 8,
    "Nonary (9)" : 9,
    "Decimal (10)" : 10,
    "Elevenary (11)" : 11,
    "Dozenal (12)" : 12,
    "Baker's Dozenal (13)" : 13,
    "Biseptimal (14)" : 14,
    "Triquinary (15)" : 15,
    "Hexadecimal (16)" : 16
}

def numberToBase(num,fromB = 10,toB = 10):
    '''Converts a number inputed as a string from one base to another
    Arguments:
    > num -- string
    > fromB, base to convert from -- int [2,36]
    > toB, base to convert to -- int [2,36]
    returns:
    - string
    '''
    #We make sure that the bases are integers and num is a string
    fromB = int(fromB)
    toB = int(toB)
    num = str(num)
    #We make sure that the bases are in between 2 and 36
    assert fromB >= 2 and fromB <= 36
    assert toB >= 2 and toB <= 36
    #we convert num to decimal, making num an integer
    num = int(num, fromB)
    result = ''
    #If num is 0 or we want base 10, then we are done
    if num == 0 or toB == 10:
      result = str(num)
    else:
      #we convert num to a string in the target base and store it in result
      #We remove the negative sign and add it back at the end
      negative = False
      if num < 0:
          num = abs(num)
          negative = True
      while num > 0:
          result = VALUES[num%toB] + result
          num //= toB
      if negative:
          result = '-' + result
    
    return result

def decToBase(saisieFlot,convert_to):
    """Convertit la partie flottante d'un nombre decimal en la base choisie

    Arguments:
    saisieFlot -- int, la partie flottante du nombre saisie
    convert_to -- int, la base dans laquelle convertir saisieFlot
    
    Return :
    int
    """
    
    #Define variables
    i=0
    res = ''
    temp = 0.1
    num = float('.'+saisieFlot)
    
    #Calculation loop
    while (i < 10) and temp!=int(temp):
        temp = float(num*convert_to)
        res += VALUES[int(temp)]
        num = temp - int(temp)
        i += 1
    return res

def baseToDec(saisieFlot,convert_from):
    """Convertit la partie flottante d'un nombre dans la base choisie en decimal

    Arguments:
    saisieFlot -- int, la partie flottante du nombre saisie
    convert_from -- int, la base dans laquelle est saisieFlot
    
    Return :
    int
    """
    res = 0
    #Calculation loop
    for i in range(len(saisieFlot)):
        value = VALUES.find(saisieFlot[i])
        assert value < convert_from, "invalid literal for baseToDec() with base %d: '%d'"%(convert_from,value)
        res += float(VALUES.find(saisieFlot[i])*(convert_from**(-(i+1))))
    
    res = str(res)
    return (res[2:])

def octets(bit_s):
    '''Complete with zeros to multiple of 4 bits'''
    if len(bit_s)%4 != 0:
        bit_s = '0'*(4-len(bit_s)%4) + bit_s
    return bit_s
 
def comp2(bit_s):
    '''Converts a binary number into a negative complement à deux number'''
    bit_s = str(bit_s)
    result = bit_s
    if int(bit_s) != 0:
        bit_s = octets('0'+bit_s)
        inverse_s = ''.join(['1' if i == '0' else '0' for i in bit_s])
        dec = int(inverse_s,2)+1
        result = bin(dec)[2:]
    result = octets(result)
    result = ' '.join(result[i:i+4] for i in range(0, len(result), 4))
    return result

def complement():
    complement = messagebox.askquestion("Complément à deux",
                            "Votre resultat est un nombre entier négatif binaire.\nVoulez-vous le convertir en complément à deux ?",
                           icon = 'question')
    return complement

def convertBase() :
    """Affiche la conversion de la base

    Arguments:
    None -- (fonction déclenchée par le bouton - pas de saisie)
    
    Return :
    None -- (remplissage d'une zone de texte)
    """
    
    #Gets entry from user
    saisie = champSaisie.get()
    
    #Gets the two bases for conversion from user
    convert_from = OPTIONS.get(clicked.get())
    convert_to = OPTIONS.get(clicked2.get())
    
    #Changes text in the base fields
    base1_label.config(text=convert_from)
    base2_label.config(text=convert_to)
    
    try:
        #We remove the negative sign and add it back at the end
        negative = False
        if saisie[0] == '-' and float(saisie) != 0:
            saisie = saisie[1:]
            negative = True
        
        resFlot = ''
        x = saisie.find('.')
        if x >= 0: #si il y a une virgule
            saisie += '0'
            saisieFlot = saisie[x+1:]
            saisie = saisie[:x]
        
        #Convert the decimal
        if x >= 0:
            if convert_from == 10:
                resFlot = '.' + decToBase(saisieFlot,convert_to)
            else:
                decRes = baseToDec(saisieFlot,convert_from)
                resFlot = '.' + decToBase(decRes,convert_to)
        
        #Convert the number
        result = numberToBase(saisie,convert_from,convert_to) + resFlot
        if negative:
            result = '-' + result
        
        #Checks if complement a deux is applicable
        if convert_to == 2 and result[0] == '-' and result.find('.') < 0:
            if complement() == 'yes':
                result = str(comp2(result[1:]))
                base2_label.config(text='Comp à 2')
                
        #Affiche resultat
        result_data.config(text=result)
        
    except Exception as e:
        messagebox.showerror(title='Erreur de saisie', message='Erreur de saisie. \nSaisissez un nombre valide.')
        result_data.config(text='Enter valid operation')
        print (e)
    
    return

def aide() :
    
    fonction_text = "Ce programme permet à l'utilisateur d'entrer un nombre réel dans n'importe\nquelle base (de 2 à 16) et de le convertir vers une autre base.\n\nSi le résultat du calcul est un nombre entier négatif binaire, l'utilisateur peut\nchoisir de le faire apparaître en complément à deux."
    utilisation_text = "L'utilisateur doit d'abord choisir la base dans laquelle se trouve le nombre\nsaisi et la base vers laquelle il veut convertir le nombre. Ensuite, l'utilisateur\ndoit saisir le nombre qu'il souhaite convertir et appuyer sur le bouton\n« Convertir » pour effectuer le calcul."
    remarques_text = "La zone de saisie ne fonctionne qu'avec les caractères possibles dans la base\nchoisie, et renvoie une erreur lorsque ce n'est pas le cas."
    
    popup2 = tk.Toplevel(root)
    popup2.geometry('460x330')
    popup2.title('Aide Convertisseur')
    popup2.configure(background='#e4e4e4')
    
    # Création d'une autre frame pour la centrer
    popup = tk.Frame(popup2)
    popup.pack()
    popup.configure(background='#e4e4e4')
        
    titre = tk.Label(popup, text='AIDE Convertisseur de bases', font=('Arial', 14, 'bold'), fg='#0c6bab', bg='#e4e4e4',anchor="center")
    titre.grid(row=0, column=0,pady=5)
    
    fonction = tk.Label(popup, text='Fonction',bg='#e4e4e4',font=('Arial', 10, 'bold'))
    fonction.grid(row=1, column=0,pady=2)
    
    utilisation = tk.Label(popup, text='Utilisation',bg='#e4e4e4',font=('Arial', 10, 'bold'))
    utilisation.grid(row=3, column=0,pady=2)
    
    remarques = tk.Label(popup, text='Remarques',bg='#e4e4e4',font=('Arial', 10, 'bold'))
    remarques.grid(row=5, column=0,pady=2)
    
    fonction_label = tk.Label(popup, text=fonction_text,bg='#e4e4e4',anchor="center",justify='left')
    fonction_label.grid(row=2, column=0,pady=2)
    
    utilisation_label = tk.Label(popup, text=utilisation_text,bg='#e4e4e4',anchor="center",justify='left')
    utilisation_label.grid(row=4, column=0,pady=2)
    
    remarques_label = tk.Label(popup, text=remarques_text,bg='#e4e4e4',anchor="center",justify='left')
    remarques_label.grid(row=6, column=0,pady=2)        

    return

# Création de la fenêtre tkinter
def create_window():
  global result_data, champSaisie, clicked, clicked2, base1_label, base2_label, root, fenetre
  
  root = tk.Tk()
  root.geometry('400x250')
  root.title('Convertisseur de bases')
  root.configure(background='#e4e4e4')
  
  # Création d'une autre frame pour la centrer
  fenetre = tk.Frame(root)
  fenetre.pack()
  fenetre.configure(background='#e4e4e4')
  
  #CREATION DES BOUTONS
  bouton_quitter = tk.Button(fenetre, text='Quitter', command=root.destroy)
  bouton_quitter.grid(row=6, column=0, padx=6, pady=6, ipadx=5)
  
  bouton_convertir = tk.Button(fenetre, text='Convertir', command=convertBase)
  bouton_convertir.grid(row=4, column=1, padx=6, pady=6, ipadx=5)
  
  bouton_aide = tk.Button(fenetre,text='?',command=aide)
  bouton_aide.grid(row=0,column=4,sticky='E')
  
  #CREATIONS DES ZONES DE TEXTE
  entete = tk.Label(fenetre, text='       Convertisseur de bases       ', font=('Arial', 14, 'bold'), fg='#0c6bab', bg='#e4e4e4')
  entete.grid(row=0, column=0, columnspan=4,pady=10)
  
  from_label = tk.Label(fenetre, text='From', bg='#e4e4e4')
  from_label.grid(row=1, column=0)
  
  to_label = tk.Label(fenetre, text='To', bg='#e4e4e4')
  to_label.grid(row=2, column=0)
  
  enter_label = tk.Label(fenetre, text='Saisie', bg='#e4e4e4')
  enter_label.grid(row=3, column=0)
  
  result_label = tk.Label(fenetre, text='Résultat', bg='#e4e4e4')
  result_label.grid(row=5, column=0)
  
  base1_label = tk.Label(fenetre, text='N/A', bg='#e4e4e4')
  base1_label.grid(row=3, column=2)
  
  base2_label = tk.Label(fenetre, text='N/A', bg='#e4e4e4')
  base2_label.grid(row=5, column=2)
  
  result_data = tk.Label(fenetre, text='',width=15, font=('Arial', 11), bg="#fff")  # par exemple
  result_data.grid(row=5, column=1)
  
  #CREATION DES CHAMPS DE SAISIE
  champSaisie = tk.Entry(fenetre, font='12', width=15)
  champSaisie.grid(row=3, column=1)
  
  #CREATION DES MENUS
  #clicked is variable for choice of base form user
  clicked = tk.StringVar(fenetre)
  clicked.set( "Choisis base" )
  #creation of menu using options from the keys of options dictionary
  base1_menu = tk.OptionMenu(fenetre, clicked, *OPTIONS.keys())
  base1_menu.grid(row=1, column=1)
  
  #clicked is variable for choice of base form user
  clicked2 = tk.StringVar(fenetre)
  clicked2.set( "Choisis base" )
  #creation of menu using options from the keys of options dictionary
  base2_menu = tk.OptionMenu(fenetre, clicked2, *OPTIONS.keys())
  base2_menu.grid(row=2, column=1)
  
  # Programme principal 
  fenetre.mainloop()    # Boucle d'attente des événements

def quitter():
    global root
    try:
        root.destroy()
    except:
        pass

def main():
    quitter()
    create_window()

if __name__ == "__main__":
    main()
