from random import randint
import gaming_tools


def create_new_character(name , variety):
    """Adds a new character to the game and add the money team if the character is added successfully
        
    Parameters
    ----------
    name: character name (str)
    variety: character variety (str)
    

    Returns
    -------
    variety_error_str : message si le type n'existe pas (str)
    added_str : message si le caractère est ajouté sans aucune erreur (str)
    error_db : message s'il aura une erreur dans l'insertion dans la base de données (str)
    
    """
    variety_error_str = 'this variety in not exist please choose the correct variety'
    added_str = 'Character added successfully'
    error_db = 'Error DB : error to add the character in the database' 

    #test if the character exist or not 
    if (gaming_tools.character_exists(name)):
        print('the character is already exist please choose another name')
    else :
        #affecter la force et la vie et la proté par rapport au type de caractère

        if (variety == 'nain'):

            reach = 'court'
            life = randint(10,50)
            strength = randint(10,50)

        elif (variety == 'elfe'):

            reach = 'longue'
            life = randint(15,25)
            strength = randint(15,25)

        elif (variety == 'soignant'):

            reach = 'court'
            life = randint(5,15)
            strength = randint(5,15)
        
        elif (variety == 'magicien'):

            reach = 'longue'          
            life = randint(5,15)
            strength = randint(5,15)
        
        elif (variety == 'necromancien'):

            reach = 'court'
            life = randint(5,15)
            strength = randint(5,15)
        
        else:
            return variety_error_str 

        try : 
            gaming_tools.add_new_character(name , variety , reach , strength , life)
            
            #ajouter 50 Pièce d'or dans le pot commun
            gaming_tools.set_team_money( gaming_tools.get_team_money() + 50 )

            

            return added_str

        except :
            return error_db






def creation_of_characters(name,variety):

    #in the begining of the game we should initialate the Database
    try :
        gaming_tools.reset_game()
    except :
        print('Error DB : error to reset the database')
    
    create_new_character(name,variety)  




def is_die(name):
    """Functinon retrun is the character is die or not

    Parameters
    ----------
    name : the name of the characters (str)

    return 
    ------
    die : True if the character is die , False otherwise (bool)
    
    """
    if gaming_tools.get_character_life() == 0 :
        die = True
    else : 
        die = False

    return die         