#!/usr/bin/env python3

import sys


_DIGITS = [["  ***  ",
            " *   * ",
            "*     *",        
            "*     *",
            "*     *",
            " *   * ",
            "  ***  "],   
           ["   *   ",
            "  **   ",
            "   *   ",        
            "   *   ",
            "   *   ",
            "   *   ",
            "  ***  "],
           ["  ***  ",
            " *   * ",
            " *  *  ",        
            "   *   ",
            "  *    ",
            " *     ",
            " ***** "],
           ["  ***  ",
            "     * ",
            "     * ",        
            "   **  ",
            "     * ",
            "     * ",
            "  ***  "],
           ["    *  ",
            "   **  ",
            "  * *  ",        
            " *  *  ",
            " ******",
            "    *  ",
            "    *  "],
           ["  **** ",
            "  *    ",
            "  *    ",        
            "  ***  ",
            "     * ",
            "     * ",
            "  ***  "],
           ["   *   ",
            "  *    ",
            " *     ",        
            " ****  ",
            " *   * ",
            " *   * ",
            "  ***  "],
           [" ***** ",
            "     * ",
            "    *  ",        
            "   *   ",
            "  *    ",
            " *     ",
            " *     "],
           ["  ***  ",
            " *   * ",
            " *   * ",        
            "  ***  ",
            " *   * ",
            " *   * ",
            "  ***  "],
           ["  ***  ",
            " *   * ",
            " *   * ",        
            "  **** ",
            "     * ",
            "    *  ",
            "   *   "]]

_MAX_DIGIT_LINES = 7

try:
    number = sys.argv[1]
    line_index = 0
    while line_index < _MAX_DIGIT_LINES:
        line = ""
        number_index = 0
        while number_index < len(number):
            digit = int(number[number_index])
            line += _DIGITS[digit][line_index] + " "
            number_index += 1
        print(line)
        line_index += 1
except IndexError:
    print("usage bigdigits.py <number>")
except ValueError as err:
   print(err)
 
