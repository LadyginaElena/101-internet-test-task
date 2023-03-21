Test task for "101 internet" company.

[![black reformat](https://github.com/LadyginaElena/101-internet-test-task/actions/workflows/black%20reformat.yml/badge.svg)](https://github.com/LadyginaElena/101-internet-test-task/actions/workflows/black%20reformat.yml)

---
## Написать автотест на Python на отправку заявки с одного адреса. ##
1. Открыть сайт https://piter-online.net/, в поиске ввести улицу Тестовая линия, дом 1. 
2. На открывшейся странице кликнуть на ""подключить"" или ""подключить по акции"" на тарифе. 
3. На открывшейся странице ввести имя Автотест, номер телефона 1111111111. 
4. Повторить пункты 2-3 пять раз.
5. Убедиться, что у всех отправленных заявок статус 201."

---
##  How it works? ##
> ***1. Copy the repository with the command***

    git clone git@github.com:LadyginaElena/101-internet-test-task.git

> ***2. Create and activate a virtual environment in this folder(OS Windows)***

      python -m venv venv
      venv\Scripts\activate
> 
> ***3. Install dependencies from the project***
      
       pip install -r requirements.txt
      
> ***4. Start test execution***
      
       pytest

> ***You can use any flags***

      -s - prints desired output (pytest -s test_file_name)
      -v - shows test process' percentage (pytest -v test_file_name)
      -m - allows to run tests with specific marks (pytest -m mark_title test_file_name)


    

