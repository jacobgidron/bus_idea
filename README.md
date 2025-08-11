# get bus information for google maps
## installation 
1) clone the repo 
2) create a new venv `python -m venv .venv`
3) install the requirements.txt   
  `pip install --upgrade pip && pip install -r requirements.txt`
4) run `python gui.py`
## useage
after searching your line bumber
and pressing make csv
<img width="621" height="341" alt="image" src="https://github.com/user-attachments/assets/076db4c1-1905-4e71-b66d-4020f6c6c4b2" />

go to google maps `saved -> Maps -> Create Map`

<img width="835" height="1222" alt="image" src="https://github.com/user-attachments/assets/fc16bc5a-6fad-41a4-adcf-5a79b41961f6" />

on the upper left menu press `Add layer` 
then preess import and load your csv 

<img width="618" height="580" alt="image" src="https://github.com/user-attachments/assets/86a9f750-bebc-4c52-99b3-a4c963faac47" />
you a dialog will appere, choose `WKT`
<img width="982" height="514" alt="image" src="https://github.com/user-attachments/assets/5df06d05-6fcd-451b-805e-6d7947627357" />
next select the `name`
<img width="905" height="473" alt="image" src="https://github.com/user-attachments/assets/a090ec83-3cda-4848-a9a8-29e033a95cba" />
done!, you can change the line width on the map and change the dots color  
<img width="1316" height="905" alt="image" src="https://github.com/user-attachments/assets/41602013-ccc2-4eb8-b0c7-be4b1f1c8143" />

## in the future i will
* might try to add more types of transportation (trains, bike lanes etc')
* merge 2 identical bus stops
* try to make the lines folow the rouds (insted of just being a line betwin all stops)
