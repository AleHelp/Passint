#!/usr/bin/env python3

import os

def delete_old_elements():
    for filename in os.listdir('./Output/'):
        file_path = os.path.join('./Output/', filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
def delete_reports():
    if not any(os.listdir('./Reports/')):
        print("[*] The /Reports folder is already empty.\n")
        return

    for filename in os.listdir('./Reports/'):
        file_path = os.path.join('./Reports/', filename)
        if os.path.isfile(file_path):
            os.remove(file_path)