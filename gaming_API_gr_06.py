

from random import randint
import gaming_tools



#Reseting the Databaase   
try :
    gaming_tools.reset_game()
except :
    print('Error DB : error to reset the database')




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

        #affect strength and life and reach in relation to character variety
        #if the character is a dwarf
        if (variety == 'dwarf'):

            reach = 'short'
            life = randint(10,50)
            strength = randint(10,50)

        #if the character is an elf
        elif (variety == 'elf'):

            reach = 'long'
            life = randint(15,25)
            strength = randint(15,25)

        #if the character is a healer
        elif (variety == 'healer'):

            reach = 'short'
            life = randint(5,15)
            strength = randint(5,15)
        
        #if the character is a wizard
        elif (variety == 'wizard'):

            reach = 'long'          
            life = randint(5,15)
            strength = randint(5,15)
        
        #if the character is a necromancer
        elif (variety == 'necromancer'):

            reach = 'short'
            life = randint(5,15)
            strength = randint(5,15)
        
        else:
            return variety_error_str 

        try : 

            #inserting a new character in the DB
            gaming_tools.add_new_character(name , variety , reach , strength , life)
            
            #add 50 piece of gold in the money team
            gaming_tools.set_team_money( gaming_tools.get_team_money() + 50 )

            

            return added_str

        except :
            return error_db







def is_die(name):

    """Functinon retrun is the character is die or not

    Parameters
    ----------
    name : the name of the characters (str)

    return 
    ------
    die : True if the character is die , False otherwise (bool)
    
    """
    #if variable name is a name of character
    if gaming_tools.character_exists(name):

        #do the test in the life of the character
        if gaming_tools.get_character_life(name) == 0 :
            die = True
        else : 
            die = False

        return die    

    #if variable name is a name of creature
    elif gaming_tools.creature_exists(name):

        #do the test in the life of the creature  
        if gaming_tools.get_creature_life(name) == 0 :
            die = True
        else : 
            die = False

        return die  

    #if variable name is not a of character and not a name of creature
    else : 
        print('this name don\'t exists between characters and creatures')        





def get_random_creature_reach():

    """ Function give a random reach 

    returns
    -------
    result : a random reach (str)
    """

    #get an random number between 0 and 1
    random_number = randint(0,1)

    #the number 0 means that the reach is short and the number 1 means that the reach is long
    if random_number == 0 :
        return 'short'
    else :
        return 'long'    





def generate_value_of_strenght_or_life() :

    """Function generate an initial value of strenght and life

    Returns
    -------
    value : the value generated (str)

    """

    #calculate the value of the strenght or the life
    value = int(randint(1,10)*(1+gaming_tools.get_nb_defeated()))
    return value


def create_new_creature() :

    """Function create a creature with the right values

    Returns
    -------
    the result of the creature is insered seccessfully in the DB or not
    """

    

    #generating name , reach , force , life of the creature
    name = gaming_tools.get_random_creature_name()
    reach = get_random_creature_reach()
    force = generate_value_of_strenght_or_life()
    life = generate_value_of_strenght_or_life()

    try :

        #inserting a new creature in the DB 
        gaming_tools.add_creature( name , reach , force , life )
        print('the creature %s is created successfully' % (name))

    except NameError:
        
        #print the error
        print(NameError)
             
   


def is_victory(character_name , creature_name) :

    """ boolean function test if the character win or not

    Parameters
    ----------
    character_name : the name of the character (str)
    creature_name : the name of the creature (str)

    Returns
    -------
    victory : True if the character win and False if character is died (bool)

    """

    #if character is alive and the creature is died
    if (not is_die(character_name)) and is_die(creature_name) :
        
        #increment the number of creatures defeated by the team
        gaming_tools.set_nb_defeated( gaming_tools.get_nb_defeated() + 1 )

        #add gift of money to the team 
        gaming_tools.set_team_money( gaming_tools.get_team_money() + (40 + (10 * gaming_tools.get_nb_defeated())))

        #remove the creature 
        gaming_tools.remove_creature(creature_name)

        return True

    #if the creature is not died
    else :
        return False    






def attack(name1 , name2):

    """The character or the creature that have the name1 attackthe creature or the character that have the name2 
        (a character can't attack an other character )

    Parameters
    ----------
    name1 : the name of the character or the creature who attack (str)    
    name2 : the name of the character or the creature who is attacked (str)
    
    """

    #if name1 & name2 exists one is from the characters and the other from the creature
    if (gaming_tools.character_exists(name1) or gaming_tools.creature_exists(name1)) and (gaming_tools.character_exists(name2) or gaming_tools.creature_exists(name2)):

        #if the name1 is for character
        if gaming_tools.character_exists(name1):

            character_reach = gaming_tools.get_character_reach(name1)
            creature_reach = gaming_tools.get_creature_reach(name2)
            character_life = gaming_tools.get_character_life(name1)

            #if they have the same reach
            if character_reach == creature_reach :

                #if the character is not died
                if (character_life > 0) and (gaming_tools.get_character_strength() < gaming_tools.get_creature_life()) :

                    #after every attack the creature loose 2 points from his life
                    gaming_tools.set_creature_life( name2 , gaming_tools.get_creature_life(name2) - gaming_tools.get_character_strength(name1) )
                    print('the attack was done')

                    #testing the victory
                    if is_victory(name1 , name2) :

                        print('There is a victory : %s win' % (name1))

                elif (character_life > 0) and (gaming_tools.get_character_strength(name1) > gaming_tools.get_creature_life(name2)) :
                    
                    #after every attack the creature loose points from his life
                    gaming_tools.set_creature_life( name2 , 0 )
                    print('the attack was done')

                    #testing the victory
                    if is_victory(name1 , name2) :

                        print('There is a victory : %s win the creature is died' % (name1))

                #if the character is died
                else :
                    print('the character is died ... he can\'t attack')

            else : 
                print('the characters and the creature haven\'t the same reach')

        #if name1 is for creature
        else :                
    
            character_reach = gaming_tools.get_character_reach(name2)
            creature_reach = gaming_tools.get_creature_reach(name1)
            character_life = gaming_tools.get_character_life(name2)

            #if they have the same reach
            if character_reach == creature_reach :

                #if the character is not died
                if (character_life > 0) and (gaming_tools.get_creature_strength(name1) < gaming_tools.get_character_life(name2)):

                    #after every attack the character loose 2 points from his life
                    gaming_tools.set_character_life( name2 , gaming_tools.get_character_life(name2) - gaming_tools.get_creature_strength(name1) )
                    print('the attack was done')

                elif (character_life > 0) and (gaming_tools.get_creature_strength(name1) < gaming_tools.get_character_life(name2)):
                
                    #after every attack the character loose points from his life
                    gaming_tools.set_character_life( name2 , 0 )
                    print('the attack was done')

                    #testing the victory
                    if is_victory(name1 , name2) :

                        print('There is a victory : %s win the character is died' % (name1))
                #if the character is died
                else :
                    print('the character is die ... he can\'t attack')

            else : 
                print('the characters and the creature haven\'t the same reach')


def power_healer(name1 , name2) :
    """The healer that have the name1 add 10 points of life to a character not died with 5 piece of gold
        
    Parameters
    ----------
    name1 : name of the healer (str)    
    name2 : name of the character who want more life (str)    
    """

    #the money of the team 
    team_money = gaming_tools.get_team_money()

    #if the team have 5 piece of gold or more
    if team_money >= 5:

        #if name1 and name2 exists in the characters
        if gaming_tools.character_exists(name1) and gaming_tools.character_exists(name2) :

            #if the name1 is a name of a healer 
            if gaming_tools.get_character_variety() == 'healer' : 

                #adding 10 points of life to the character that have the name2
                gaming_tools.set_character_life( name2 , gaming_tools.get_character_life(name2) + 10 )

                #the team loose 5 piece of gold
                gaming_tools.set_team_money( team_money - 5)

            #if the name1 is not a name of a healer 
            else :
                print('Error : the name1 is not a healer')     

        #if name1 or name2  or both don't exists in the characters
        else :
            print('name1 or name2 or both are not exists between characters')  

    #if the team have not 5 piece of gold
    else :
        print('the team haven\'t money enough') 




def power_wizard(name1 , name2):
    """The wizard can devide by two the life of the creature for 20 pieces of gold
        
    Parameters
    ----------
    name1 : name of the wizard (str)    
    name2 : name of the creature (str)    
    """

    #the money of the team 
    team_money = gaming_tools.get_team_money()

    #if the team have 5 piece of gold or more
    if team_money >= 20:

        #if name1 exists in characters and name2 exists in creatures
        if gaming_tools.character_exists(name1) and gaming_tools.creature_exists(name2) :

            #if the name1 is a name of a wizard 
            if gaming_tools.get_character_variety(name1) == 'wizard' : 

                #devide by 2 the life of the creature 
                gaming_tools.set_creature_life( name2 , int( gaming_tools.get_creature_life(name2) / 2 ) )

                #the team loose 20 pieces of gold
                gaming_tools.set_team_money( team_money - 20)

                print('the power of wizard is used successfully')

            #if the name1 is not a name of a wizard 
            else :
                print('Error : the name1 is not a wizard')     

        #if name1 or name2  or both don't exists 
        else :
            print('name1 or name2 or both doesn\'t exists')  

    #if the team have not 20 piece of gold
    else :
        print('the team haven\'t money enough') 






def power_necromancer(name1 , name2):
    """The necromancer can resurrect a character died with 10 points of life for 75 pieces of gold
        
    Parameters
    ----------
    name1 : name of the necromancer (str)    
    name2 : name of the character died (str)    
    """

    #the money of the team 
    team_money = gaming_tools.get_team_money()

    #if the team have 75 piece of gold or more
    if team_money >= 75:

        #if name1 exists in characters and name2 exists in creatures
        if gaming_tools.character_exists(name1) and gaming_tools.character_exists(name2) :

            #if the name2 is died
            if gaming_tools.get_character_life(name2) <= 0 :

                #if the name1 is a name of a necromancer 
                if gaming_tools.get_character_variety(name1) == 'necromancer' : 

                    #resurrect a character died with 10 points of life 
                    gaming_tools.set_character_life( name2 , 10 )

                    #the team loose 75 pieces of gold
                    gaming_tools.set_team_money( team_money - 75)

                #if the name1 is not a name of a necromancer 
                else :
                    print('Error : the name1 is not a necromancer')     

            #if the name2 is not died
            else :
                print('Error : the %s is not died' %(name2))

        #if name1 or name2  or both don't exists 
        else :
            print('name1 or name2 or both doesn\'t exists')  

    #if the team have not 75 piece of gold
    else :
        print('the team haven\'t money enough') 



#il me reste la fonction de l'accord des autres joueurs
def evolution(name):
    """ have 25% of chance to evolute the strenght of the character with 4 and 50% of chance to evolute the life of 
        the character with 2 for 4 pieces of gold 

    Parameters 
    ----------
    name : the name of the character (str)
    """

    #faut faire un test d'abord sur l'accord des autre joueur

    #testing if the character exists 
    if gaming_tools.character_exists(name) :

        #if the character is not died
        if gaming_tools.get_character_life(name) > 0 :

            #realize the 50% with random
            random_number = randint(0,1)
            
            #number 1 mean yes he can evolute his life and number 0 means that he can't evolute his life
            if random_number == 0 : 
                
                print('Sorry they hasn\'t the chance to evolute the life')
           
            #random_number == 1
            else : 

                #evolute the life with 2
                gaming_tools.set_character_life( name , gaming_tools.get_character_life(name) + 2 )
                print('The life is evoluted with 2 points')


            #realize the 25% with random
            random_number = randint(0,3)
            
            #number 3 mean yes he can evolute his strenght and numbers 0,1,2 means that he can't evolute his strenght
            if random_number == 0 : 
                
                print('Sorry they hasn\'t the chance to evolute the strenght')
           
            if random_number == 1 : 
                
                print('Sorry they hasn\'t the chance to evolute the strenght')
            
            if random_number == 2 : 
                
                print('Sorry they hasn\'t the chance to evolute the strenght')
            
            #random_number == 3
            else : 

                #evolute the strenght with 4
                gaming_tools.set_character_strength( name , gaming_tools.get_character_strength(name) + 4 )
                print('The strenght is evoluted with 4 points')


        #if the character is died
        else :
            print('Error : this character is died')    

    #if the character don't exist
    else :     
        print('Error : %s is not exist' % (name))


#il me reste foncntions d'affichage de tt les attributs des caractères et des créatures            