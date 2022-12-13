# Importando algumas bibliotecas
import json
import os

# Adicionar um novo site à lista
def add_site():
  print("""
  _________

  Add website information:
  (follow the format -> WebSiteName MM/YYYY URL)
  (if you want to add more than one site, use comma ',' to separate)
        """)

  websites = input('  > ')
  websites = websites.split(', ')

  for website_data in websites:
    website_data = website_data.split()

    time = website_data[1].split('/')
    formatted_string = f'{{"name": "{website_data[0]}", "time": {{"month": "{time[0]}", "year": "{time[1]}"}}, "url": "{website_data[2]}"}}'
    data.append(json.loads(formatted_string))

  print("  _________\n")

# Apresentar a lista de sites
def show_all_sites():
  print("""
  _________

  The next sites are saved:
        """)
  
  for website_data in data:
    index = data.index(website_data)
    
    formatted_string = f'    {index + 1} - {website_data["name"]} {website_data["time"]["month"]}/{website_data["time"]["year"]} {website_data["url"]}'
    print(formatted_string)

  print("  _________\n")

# Editar um site da lista
def edit_site():
  print("""
  _________

  Enter the number of the website you want to edit
        """)

  number = input('  > ')

  try:
    number = int(number)
    website_data = data[number - 1]
    formatted_string = f'\n  {website_data["name"]} {website_data["time"]["month"]}/{website_data["time"]["year"]} {website_data["url"]}'
    print(formatted_string)

    print("""
  Choose the information you want to edit:
  1 - Name
  2 - Time
  3 - URL
          """)

    option = int(input("  > "))
    key = [*website_data][option - 1]
    print(f'\n  Old: {website_data[key]}')
    new_data = input('  New: ')

    index = data.index(website_data)
    website_data[key] = new_data 
    data[index] = website_data

  except (IndexError, ValueError):
    print('\n  /!\ Invalid number or input /!\ ')

  print("  _________\n")

# Deletar um site da lista
def delete_site():
  print("""
  _________

  Enter the number of the website you want to delete
        """)
  
  number = input('  > ')
  
  try:
    number = int(number)
    data.remove(data[number - 1])
    print("  Deleted site!\n")
  except (IndexError, ValueError):
    print('\n  /!\ Invalid number or input /!\ ')

  print("  _________\n")

# Carregando dados do arquivo
def file_data():
  file_path = 'data/preload_data.txt'

  with open(file_path, 'r') as file:
    data_string = file.read()

  if data_string:
    websites = data_string.split('\n')

    for website_data in websites:
      website_data = website_data.split()

      time = website_data[1].split('/')
      formatted_string = f'{{"name": "{website_data[0]}", "time": {{"month": "{time[0]}", "year": "{time[1]}"}}, "url": "{website_data[2]}"}}'
      data.append(json.loads(formatted_string))
  else:
    print("""  
  _________
  
  The file is empty!  
  _________  
  \n""")

# Apagando todos os dados carregados
def delete_loaded_data():
  data.clear()

# O menu
def menu_init():
  print("""
  ######## Galaxy menu ########
  #                           #
  #  1 - Add a new site       #
  #  2 - Show all sites       #
  #  3 - Edit a site          #
  #  4 - Delete a site        #
  #  5 - Data from file       #
  #  6 - Delete loaded data   #
  #  0 - Exit the menu        #
  #                           #
  #############################
      """)

# Estrutura que tenta reproduzir o comportamento de uma construção switch/case
def switch(option):
  menu_init()
  switcher = {
    1: add_site,
    2: show_all_sites,
    3: edit_site,
    4: delete_site,
    5: file_data,
    6: delete_loaded_data
  }
  switcher[option]()

# Caminho para o arquivo
path = 'data/data.txt'
# Lendo os dados do arquivo
with open(path, 'r') as file:
  data_string = file.read()

# Para limpar o terminal
clear = lambda: os.system("clear")
# Passando a string para JSON
data = json.loads('[]')
if data_string: data = json.loads(data_string)
option = 1 # Opção inicial (inicialmente diferente de zero)

menu_init() # Carregando o Menu 

# Laço principal
while option:
  try:
    print("  Enter the desired option:")
    option = int(input('  > '))
  except ValueError:
    print('\n  /!\ Invalid input! /!\ ')
    clear()
    continue

  clear()
  if option:
    try:
      switch(option)
    except KeyError:
      print('\n  /!\ Invalid option! /!\ ')

# Salvando os dados no arquivo
with open(path, 'w') as file:
  file.write(str(data).replace('\'', '"'))
