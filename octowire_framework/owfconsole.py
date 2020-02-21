# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


import argparse
import os
import platform
import shutil

from octowire_framework.core.Framework import Framework
from octowire.utils.Colors import Colors
from octowire.utils.Logger import Logger


def _print_logo(logo, terminal_width):
    centered_logo = ""
    for line in logo.splitlines():
        centered_logo += line.center(terminal_width)
    print(centered_logo)


def welcome(terminal_width):
    """
    Print the framework header.
    :return: Nothing
    """
    logos = ["""\x1b[38;5;92m
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣿⣿⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣴⠾⢶⡄⠀⠀⠀⣿⡍⠻⢿⣿⣿⣿⣿⡿⠟⢋⣿⠀⠀⠀⢠⡶⠷⣦⠀⠀
⣰⡞⠻⠶⠾⠃⠀⠀⠀⠙⢿⣤⣤⣾⣿⣿⣷⣤⣤⡾⠋⠀⠀⠀⠘⠷⠶⠟⢳⣆
⢿⣷⣄⢀⣀⣠⣤⣶⡶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢶⣶⣤⣄⣀⡀⣠⣾⡿
⠈⠛⠿⠿⠿⠿⠿⣫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣍⠿⠿⠿⠿⠿⠟⠁
⣰⡿⢷⡄⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⢠⡾⢿⣦
⢙⡷⠾⠃⠀⣰⡿⣾⣿⣷⣿⣿⡟⢡⣴⣦⡌⢻⣿⣿⡿⣿⣷⢻⣆⠀⠘⠷⢾⡋
⢸⣿⣀⣀⣴⣿⢷⣿⣿⣸⣿⣿⡇⠸⣧⣼⠏⢸⣿⣿⡇⣿⣿⡟⣿⣦⣀⣀⣾⡇
⠀⠙⠛⠿⠟⠛⢸⣿⣿⡇⣿⣿⣇⠀⠀⠀⠀⣸⣿⣿⢹⣿⣿⡇⠙⠻⠿⠟⠋⠀
⠀⠀⢀⣀⡀⠀⠈⣿⣿⣿⠘⣿⣿⣆⠀⠀⣰⣿⣿⠃⣿⣿⣿⡇⠀⢀⣀⡀⠀⠀
⠀⠀⣿⣉⣿⠀⢸⣿⣿⡇⠀⠘⣿⣿⡆⢰⣿⣿⠃⠀⢸⣿⣿⡇⠀⣿⣉⣿⠆⠀
⠀⢰⣏⠛⠉⠀⣼⣿⡿⠀⠀⠀⠘⣿⡇⢸⣿⠇⠀⠀⠀⢻⣿⣧⠀⠈⠛⣹⡆⠀
⠀⠀⠻⢿⣶⣿⡿⠋⠀⠀⠀⠀⣤⣿⠃⠘⢿⣠⡀⠀⠀⠀⠙⢿⣿⣶⡿⠟⠁⠀
⠀⠀⠀⠀⠀⠀⢀⣴⢶⣤⣴⡿⠛⠁⠀⠀⠈⠛⢿⣦⣤⡶⣶⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⢷⣴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣧⡾⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣴⡶⣶⡄⠀⢠⣴⡶⡶⠀⣿⣷⣶⠀⢠⣴⢶⣦⡄⢰⣶⠀⢰⣦⠀⣴⡖⢰⣶⠀⢠⣶⠶⡆⢀⣴⠶⣶⡄
⣿⡇⠀⢸⣿⠀⣿⡇⠀⠀⠀⣿⡇⠀⠀⣿⡇⠀⢸⣿⠀⢿⡇⣿⢿⣤⣿⠁⢸⣿⠀⢸⣿⠀⠀⣾⡿⠶⠾⠿
⠙⢿⣶⡾⠏⠀⠹⢷⣶⣶⠀⠻⣷⣶⡄⠹⢷⣶⡾⠏⠀⠘⣿⠇⠘⣿⠇⠀⢸⣿⠀⢸⣿⠀⠀⠘⢿⣶⣶⡆
            \x1b[0m""",
             """{}
                      ~yNNNNHNNNNy~.                         
                   oNHHHHHHHHHHHHHHHNw                       
                 (NHHHHHHHHHHHHHHHHHHHNp                     
                (HHHHHHHHHHHHHHHHHHHHHHHb                    
                NHHHHHHHHHHHHHHHHHHHHHHHH                    
                #HHHHHHHHHHHHHHHHHHHHHHHH                    
                `HHHHHHHHHHHHHHHHHHHHHHHL                    
                 (HHHHHHHHHHHHHHHHHHHHHN                     
      ~yy,       (HCVHHHHHHHHHHHHHHHN"HN       ,;y~          
     NH `HN      (NN,  "NHHHHHHHN"   NHN      @H" NH         
  (NN7HNNHN        7Hy. .#HHHHHN, .~NN        "HNNNN7Nw      
 &HH             .,~pHHHHHHHHHHHHHHHN~~.             @HN     
 (HHN~ ,,,~ypNNHHMNHHHHHHHHHHHHHHHHHHHNNNHNNNy~,,, ,NHHN     
  "NHHHNNHHHHHN.#NHHHHHHHHHHHHHHHHHHHHHHN,7NHHHHNNHHHH"      
      \"\"\"\"\"   NHHHHHHHHHHHHHHHHHHHHHHHHHHHN,  `"\"\"\"        
  NHNNN      NHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH,     #HNNN,     
 (Hb./HL    NHNHHHNHHHHHHM"   `7NHHHHHNHHHNNH    (HN.(HN     
  (HM=     NH NHHH HHHHH  pNNNN  NHHHH)NHHH,HN,    "7HN      
  NH,    ,NHN(HHHH(HHHHL (Hb (HN (HHHH)&HHHN(HH\\     HH      
  "HHwy0NHHH &HHHH HHHHb  "MNN"  (HHHH NHHHH HHHNNyyNHM      
    "*NNNM"  (HHHH,(HHHN         NHHHN NHHHH  "7NNN="        
             (HHHHN VNHHN       #HHHN NHHHHN                 
     .~;~    (HHHHH  7HHHN,    NHHHN  NHHHHN    ~;~,         
    (HC`7H,  (HHHHN   (HHHH   NHHHN   (HHHHN   NN "HN        
    (HNyNN   NHHHH     "HHHN (HHHL     NHHHH   NNwNHL        
    Nb      (HHHN       (HHH &HHN       NHHHb      (N        
    "HNw;;^qHHHN         HH' `HH         "NHHN`;;yNHN        
      "VNNHNM"        .NNH'   `NMN,        `7NHNNM"          
              ;0Ny .;NHN"       "NHNy, ;0Ny                  
             NH  NH="               "*HH  AH                 
             "NNNH"                   "NNNH"                 


                ,~                      #N                   
  .w#m,   .o#m, #Nmo,  ~mmo  ;o  :o  oo :m  ,ommc  omm,      
 #N   N# (NE    #N    #R  YN  NE #N, NE (N  #N   (NE..N#     
 AN, .NR (N,    #N    N#  #N  'N#E`N#R  (N  #N   `NE         
  `4MM"   `7MM=  7MM*  "MM=    "=  "=   *=  *=     7MMN'     
             {}""".format(Colors.MAGENTA, Colors.ENDC)
             ]
    environ = os.environ
    system = platform.system()
    uname = platform.uname()
    # Check if Linux WSL or Windows but not in a Windows Terminal session
    if "WT_SESSION" not in environ and (("Linux" in uname[0] and "Microsoft" in uname[2]) or "Windows" in system):
        _print_logo(logo=logos[1], terminal_width=terminal_width)
    else:
        # Check if the distribution is a Linux system and it has the TERM environment variable (WSL or Not)
        if "Linux" in system and "TERM" in environ:
            # Linux without x-term256color support
            if environ["TERM"] != "xterm-256color":
                _print_logo(logo=logos[1], terminal_width=terminal_width)
            # Linux with x-term256color support
            else:
                _print_logo(logo=logos[0], terminal_width=terminal_width)
        # Windows in a Windows Terminal session
        elif "Windows" in system:
            _print_logo(logo=logos[0], terminal_width=terminal_width)
        # Other
        else:
            _print_logo(logo=logos[1], terminal_width=terminal_width)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--file', help='A file containing framework commands (one per line)')
    args = parser.parse_args()
    t_width, _ = shutil.get_terminal_size()
    welcome(terminal_width=t_width)
    if t_width < 95:
        Logger().handle("Please consider using a terminal width >= 95 for a better experience.", Logger.WARNING)
    instance = Framework()
    instance.run(args.file)


if __name__ == "__main__":
    main()
