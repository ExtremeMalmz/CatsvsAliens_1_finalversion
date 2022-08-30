from GameFiles.main_menu import the_main
from GameFiles.main_json import create_json
from Levels.first_boss_fight import first_boss_fight_main
#from Levels.second_boss_fight import second_boss_fight_main

if __name__ == '__main__':
    '''
    if the name of the file is main.py it will run, otherwise not
    '''
    create_json()
    #first_boss_fight_main()
    #second_boss_fight_main()
    the_main()
    
