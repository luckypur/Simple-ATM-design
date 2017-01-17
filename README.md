# Simple-ATM-design

* Assuming that input is validated by some other interface so not stress fully validating things like integer overflow, maximum limit of integer, initialization with negative values etc.

* System is running sample use cases from file use_cases.py

Does not have any external dependency. Compatible with python 2+.(Python 3 recommended)

If you do not have python installed then type following command
```
sudo apt-get install python3
```
then go into the project folder
```
 cd Simple-ATM-design
```
Simply type the following command at terminal to Run the program
```
python3 main.py
``` 

   OR

If you want to see the detailed information in console output then run
```
python3 main.py --log=DEBUG
```

To run the test cases type the following command
```
python3 test_atm.py
```

Happy Coding :)