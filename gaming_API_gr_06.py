from random import randint
import gaming_tools

#agree to the evolution (default : False)
is_agree = False



def reset_the_game():
    """Reset database
    
    """
    
    #Reset the Database   
    try :
        gaming_tools.reset_game()
    except :
        print('Error DB : error to reset the database')

#reset the game        
reset_the_game()


def create_new_character(name , variety):
    """Adds a new character and money to the team (if the character is added successfully)
        
    Parameters
    ----------
    name: character name (str)
    variety: character variety (str)
    

    Returns
    -------
    variety_error_str : message if the character variety doesn't exist (str)
    added_str : message if the character is added without error (str)
    error_db : message if there is an error in the database (str)
    
    """
    variety_error_str = 'this variety doesn\'t exist please choose the correct variety'
    added_str = 'Character added successfully'
    error_db = 'Error DB : error to add the character in the database' 

    #test if the character exists or not 
    if (gaming_tools.character_exists(name)):
        print('the character is already exist please choose another name')
    else :

        #affect strength, life and reach to the character variety
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

            #add a new character in the DB
            gaming_tools.add_new_character(name , variety , reach , strength , life)
            #print informations
            print('%s \n' % (print_character_informations(name)))
            
            #add 50 pieces of gold to the team
            gaming_tools.set_team_money( gaming_tools.get_team_money() + 50 )

            

            return added_str

        except :
            return error_db








def is_die(name):

    """Returns if the character died or not

    Parameters
    ----------
    name : the name of the characters (str)

    return 
    ------
    die : True if the character died , False otherwise (bool)
    
    """
    #if a variable name is a character
    if gaming_tools.character_exists(name):

        #make the test for the character's life
        if gaming_tools.get_character_life(name) == 0 :
            die = True
        else : 
            die = False

        return die    

    #if a variable name is a creature
    elif gaming_tools.creature_exists(name):

        #make the test for the creature's life  
        if gaming_tools.get_creature_life(name) == 0 :
            die = True
        else : 
            die = False

        return die  

    #if a variable name is not a character or a creature
    else : 
        print('this name don\'t exists between characters and creatures')        





def get_random_creature_reach():

    """Gives a random reach 

    returns
    -------
    result : a random reach (str)
    """

    #get an random number between 0 and 1
    random_number = randint(0,1)

    #number 0 means that the reach is short and number 1 means that the reach is long
    if random_number == 0 :
        return 'short'
    else :
        return 'long'    





def generate_value_of_strength_or_life() :

    """Generates an initial value of strength and life

    Returns
    -------
    value : the value generated (str)

    """

    #calculate the value of the strength and the life
    value = int(randint(1,10)*(1+gaming_tools.get_nb_defeated()))
    return value


def create_new_creature() :

    """Creates a creature with random values

    Returns
    -------
    the creature's result is added successfully in the DB or not
    """

    
    #test if the creature exists or not 
    if gaming_tools.is_there_a_creature():
        print('you can\'t create a new creature there is a creature exists')
    else :    
        #generating name , reach , force , life of the creature
        name = gaming_tools.get_random_creature_name()
        reach = get_random_creature_reach()
        force = generate_value_of_strenght_or_life()
        life = generate_value_of_strenght_or_life()

        try :

            #add a new creature in the DB 
            gaming_tools.add_creature( name , reach , force , life )
            print('the creature %s is created successfully' % (name))
            print('%s \n' % (print_creature_informations(name)))

        except NameError:
            
            #print the error
            print(NameError)
             
   


def is_victory(character_name , creature_name) :

    """test if the character win or not

    Parameters
    ----------
    character_name : the name of the character (str)
    creature_name : the name of the creature (str)

    Returns
    -------
    victory : True if the character win and False if the character died (bool)

    """

    #if the character is alive and the creature died
    if (not is_die(character_name)) and is_die(creature_name) :
        
        #increment the number of defeated creatures by the team
        gaming_tools.set_nb_defeated( gaming_tools.get_nb_defeated() + 1 )

        #add money to the team 
        gaming_tools.set_team_money( gaming_tools.get_team_money() + (40 + (10 * gaming_tools.get_nb_defeated())))

        #remove the creature 
        gaming_tools.remove_creature(creature_name)

        print('')

        #create new creature
        create_new_creature()

        return True

    #if the creature is not died
    else :
        return False    






def attack(name1 , name2):

    """The character or the creature who has the name1 attacks the creature or the character who has the name2 
        (a character can't attack an other character )

    Parameters
    ----------
    name1 : the name of the character or the creature who attacks (str)    
    name2 : the name of the character or the creature who is attacked (str)
    
    """

    #if name1 & name2 exist one name is for a character and the other for a creature
    if (gaming_tools.character_exists(name1) or gaming_tools.creature_exists(name1)) and (gaming_tools.character_exists(name2) or gaming_tools.creature_exists(name2)):

        #if the name1 is a character
        if gaming_tools.character_exists(name1):

            character_reach = gaming_tools.get_character_reach(name1)
            creature_reach = gaming_tools.get_creature_reach(name2)
            character_life = gaming_tools.get_character_life(name1)

            #if they have the same reach
            if character_reach == creature_reach :

                #if the character is not died
                if (character_life > 0) and (gaming_tools.get_character_strength(name1) < gaming_tools.get_creature_life(name2)) :

                    #after every attack the creature looses 2 points from his life
                    gaming_tools.set_creature_life( name2 , gaming_tools.get_creature_life(name2) - gaming_tools.get_character_strength(name1) )
                    print('the attack was done')

                    #testing the victory
                    if is_victory(name1 , name2) :

                        print('There is a victory : %s win' % (name1))

                elif (character_life > 0) and (gaming_tools.get_character_strength(name1) > gaming_tools.get_creature_life(name2)) :
                    
                    #after every attack the creature looses life's points
                    gaming_tools.set_creature_life( name2 , 0 )
                    print('the attack was done')

                    #testing the victory
                    if is_victory(name1 , name2) :

                        print('There is a victory : %s win the creature is died' % (name1))

                #if the character died
                else :
                    print('the character is dead ... he can\'t attack')

            else : 
                print('the characters and the creature haven\'t the same reach')

        #if name1 is a creature
        else :                
    
            character_reach = gaming_tools.get_character_reach(name2)
            creature_reach = gaming_tools.get_creature_reach(name1)
            character_life = gaming_tools.get_character_life(name2)

            #if they have the same reach
            if character_reach == creature_reach :

                #if the character is not died
                if (character_life > 0) and (gaming_tools.get_creature_strength(name1) < gaming_tools.get_character_life(name2)):

                    #after every attack the character looses 2 points from his life
                    gaming_tools.set_character_life( name2 , gaming_tools.get_character_life(name2) - gaming_tools.get_creature_strength(name1) )
                    print('the attack was done')

                elif (character_life > 0) and (gaming_tools.get_creature_strength(name1) < gaming_tools.get_character_life(name2)):
                
                    #after every attack the character looses points from his life
                    gaming_tools.set_character_life( name2 , 0 )
                    print('the attack was done')

                    #testing the victory
                    if is_victory(name1 , name2) :

                        print('There is a victory : %s win the character is died' % (name1))
                #if the character died
                else :
                    print('the character is dead ... he can\'t attack')

            else : 
                print('the characters and the creature haven\'t the same reach')


def power_healer(name1 , name2) :
    """The healer who has the name1 add 10 life's point to a character alive with 5 piece of gold
        
    Parameters
    ----------
    name1 : name of the healer (str)    
    name2 : name of the character who wants more life (str)    
    """

    #the money of the team 
    team_money = gaming_tools.get_team_money()

    #if the team has 5 pieces of gold or more
    if team_money >= 5:

        #if name1 and name2 exists in the characters
        if gaming_tools.character_exists(name1) and gaming_tools.character_exists(name2) :

            #if the name1 is a healer
            if gaming_tools.get_character_variety() == 'healer' : 

                #adding 10 points of life to the character who has the name2
                gaming_tools.set_character_life( name2 , gaming_tools.get_character_life(name2) + 10 )

                #the team looses 5 pieces of gold
                gaming_tools.set_team_money( team_money - 5)

            #if the name1 is not a healer
            else :
                print('Error : the name1 is not a healer')     

        #if name1 or name2  or both don't exists in the characters
        else :
            print('name1 or name2 or both are not exists between characters')  

    #if the team has not 5 pieces of gold
    else :
        print('the team haven\'t money enough') 




def power_wizard(name1 , name2):
    """The wizard can divide by two the life of the creature for 20 pieces of gold
        
    Parameters
    ----------
    name1 : name of the wizard (str)    
    name2 : name of the creature (str)    
    """

    #the money of the team 
    team_money = gaming_tools.get_team_money()

    #if the team has 5 pieces of gold or more
    if team_money >= 20:

        #if name1 exists in the characters and name2 exists in the creatures
        if gaming_tools.character_exists(name1) and gaming_tools.creature_exists(name2) :

            #if name1 is a wizard 
            if gaming_tools.get_character_variety(name1) == 'wizard' : 

                #divide by 2 the creature's life 
                gaming_tools.set_creature_life( name2 , int( gaming_tools.get_creature_life(name2) / 2 ) )

                #the team looses 20 pieces of gold
                gaming_tools.set_team_money( team_money - 20)

                print('the power of wizard is used successfully')

            #if name1 is not a wizard 
            else :
                print('Error : the name1 is not a wizard')     

        #if name1 or name2  or both don't exists 
        else :
            print('name1 or name2 or both doesn\'t exists')  

    #if the team has not 20 piece of gold
    else :
        print('the team haven\'t money enough') 






def power_necromancer(name1 , name2):
    """The necromancer can resurrect a character died with 10 life's points for 75 pieces of gold
        
    Parameters
    ----------
    name1 : name of the necromancer (str)    
    name2 : name of the character died (str)    
    """

    #the money of the team 
    team_money = gaming_tools.get_team_money()

    #if the team has 75 pieces of gold or more
    if team_money >= 75:

        #if name1 exists in characters and name2 exists in creatures
        if gaming_tools.character_exists(name1) and gaming_tools.character_exists(name2) :

            #if name2 is died
            if gaming_tools.get_character_life(name2) <= 0 :

                #if name1 is a necromancer
                if gaming_tools.get_character_variety(name1) == 'necromancer' : 

                    #resurrect a character died with 10 points of life 
                    gaming_tools.set_character_life( name2 , 10 )

                    #the team looses 75 pieces of gold
                    gaming_tools.set_team_money( team_money - 75)

                #if the name1 is not a necromancer 
                else :
                    print('Error : the name1 is not a necromancer')     

            #if the name2 is not died
            else :
                print('Error : the %s is not died' %(name2))

        #if name1 or name2  or both don't exists 
        else :
            print('name1 or name2 or both doesn\'t exists')  

    #if the team has not 75 pieces of gold
    else :
        print('the team haven\'t money enough') 






def evolution(name):
    """25% of chance to evolute the character's strenght for 4 pieces of gold and 50% of chance to evolute the character's life with 2 for 4 pieces of gold 

    Parameters 
    ----------
    name : the name of the character (str)
    """

    #test if all the players are agree for the evolution of a character
    if (is_agree) :

        #testing if the character exists 
        if gaming_tools.character_exists(name) :

            #if the character is not died
            if gaming_tools.get_character_life(name) > 0 :

                #realize the 50% with random
                random_number = randint(0,1)
                
                #(1) means he can evolute his life and (0) means he can't 
                if random_number == 0 : 
                    
                    print('Sorry they hasn\'t the chance to evolute the life')
            
                #random_number == 1
                else : 

                    #evolute the life with 2
                    gaming_tools.set_character_life( name , gaming_tools.get_character_life(name) + 2 )
                    print('The life evolute with 2 points')


                #realize the 25% with random
                random_number = randint(0,3)
                
                #(3) means he can evolute his strenght and (0,1,2) means that he can't 
                if random_number == 0 : 
                    
                    print('Sorry they hasn\'t the chance to evolute the strength')
            
                if random_number == 1 : 
                    
                    print('Sorry they hasn\'t the chance to evolute the strength')
                
                if random_number == 2 : 
                    
                    print('Sorry they hasn\'t the chance to evolute the strength')
                
                #random_number == 3
                else : 

                    #evolute the strenght with 4
                    gaming_tools.set_character_strength( name , gaming_tools.get_character_strength(name) + 4 )
                    print('The strength evolutes with 4 points')


            #if the character is died
            else :
                print('Error : this character died')    

        #if the character don't exist
        else :     
            print('Error : %s is not exist' % (name))

    #if other players are not agree
    else :

        #print he can't evoluate
        print('Sorry we can\'t evoluate the %s because other player are not agree with that' % (name))   



def fight(name1,name2):

    """name 1 attacks and name 2 reply
    
    Paramaters
    ----------
    name1 : the name of the first hero (str)
    name2 : the name of the second hero (str)
    """

    #name1 attack and name2 reply 
    attack(name1,name2)
    attack(name2,name1)
    
    

def print_character_informations(name):
    """print the life , the reach , the variety and the strength of a character 
    
    Parameters
    ----------
    name : the name of the character (str)

    Returns 
    -------

    infos : the character's informations (str)

    """
    
    #test if this name exists in the characters
    if gaming_tools.character_exists(name) :

        #print the properties of this character
        variety = gaming_tools.get_character_variety(name)
        reach = gaming_tools.get_character_reach(name)
        life = gaming_tools.get_character_life(name)
        strength = gaming_tools.get_character_strength(name)

        return 'Name : %s | variety : %s | reach : %s | life : %s | strength : %s' % (name,variety,reach,life,strength)

    #if it's not exists     
    else :
        #print a error
        return 'Sorry %s not exists in the characters' % (name)  
        



def print_creature_informations(name):
    """print the life , the reach , the variety and the strength of a creature 
    
    Parameters
    ----------
    name : the creature's name (str)

    Returns 
    -------

    infos : the creature's informations (str)

    """
    
    #test if this name exists in the creatures
    if gaming_tools.creature_exists(name) :

        #print the properties of this character
        reach = gaming_tools.get_creature_reach(name)
        life = gaming_tools.get_creature_life(name)
        strength = gaming_tools.get_creature_strength(name)

        return 'Name : %s | reach : %s | life : %s | strength : %s' % (name,reach,life,strength)

    #if it's not exists     
    else :
        #print a error
        return 'Sorry %s not exists in the creatures' % (name) 


def set_agree(response):
    """function uses when all characters are agree for a character's evolution
    
    Parameters
    ----------
    response : the response of name1 True if he is agree (bool)

    """
    is_agree = response
    
    
def print_all_functions():
    """procedure to print all the functions use by the player for playing 
    """    
    print("\n\n\nThe list of the functions availables in this module :\n")
    print("reset_the_game() *** create_new_character(name , variety) *** is_die(name) *** create_new_creature() *** power_necromancer(name1 , name2) *** power_healer(name1 , name2) *** power_wizard(name1 , name2) *** evolution(name) *** fight(name1,name2) *** set_agree(response) *** print_creature_informations(name) *** print_character_informations(name) *** print_all_functions()\n\n\n")

print_all_functions()    