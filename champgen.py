from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, QTimer, QThread
import requests
from io import BytesIO
import shutil,os
from lists import champs, roless
from random import*
import threading
from pathlib import Path
from time import sleep

a = 75
pix = []


def imag(champion):
    champion = champion.replace(" ", "")
    
    # Mapping special characters to their standard counterparts
    champion_mapping = {
        "Kai'Sa": "Kaisa",
        "Dr.Mundo": "DrMundo",
        "Rek'Sai": "RekSai",
        "Vel'Koz": "Velkoz",
        "Cho'Gath": "Chogath",
        "LeBlanc": "Leblanc",
        "Kog'Maw": "KogMaw",
        "Kha'Zix": "Khazix",
        "K'Sante": "KSante",
        "Bel'Veth": "Belveth"
    }
    
    if champion in champion_mapping:
        champion = champion_mapping[champion]

    if "RenataGlasc" in champion:
        url = "https://static.wikia.nocookie.net/leagueoflegends/images/5/58/Renata_Glasc_OriginalCentered.jpg/revision/latest?cb=20220202013811"
    elif "Wukong" in champion:
        url = "https://static.wikia.nocookie.net/leagueoflegends/images/c/c1/Wukong_OriginalCentered.jpg/revision/latest?cb=20180414203728"
    elif "Nunu&Willump" in champion:
        url = "https://static.wikia.nocookie.net/leagueoflegends/images/0/09/Nunu_OriginalCentered.jpg/revision/latest?cb=20180828194858"
    else:
        url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_0.jpg"

    response = requests.get(url, stream=True)
    
    if not(Path(champion).is_file()):
        with open(f"images/{champion}.jpg", 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
            
    # Load the image from the local file
    windows.loading.setText(f"Loading Images: {champion}...")
    pixmap = QPixmap(f"images/{champion}.jpg")
    return pixmap



def roles(r):
    pixmap = QPixmap()
    pixmap.load(".png")
    windows.role1.setPixmap(pixmap)
    windows.role2.setPixmap(pixmap)
    windows.role3.setPixmap(pixmap)
    windows.role4.setPixmap(pixmap)
    
    r = r.split()
    for i, role in enumerate(r[:4]):
        pixmap.load(f"roles/{role}.png")
        role_widget = getattr(windows, f"role{i + 1}")
        role_widget.setPixmap(pixmap)


def show():
    try:
        global a
        windows.generate.setEnabled(False)
        windows.roles.setEnabled(False)

        if a == 75:
            windows.generate.setText("PLAYING...")
            windows.generate.setStyleSheet("color: white; background-color: green; font-size: 20px; font-weight: bold;")
            timer.start(a)
            
        n = generate_click()
        pixmap = pix[n]
        windows.img.setPixmap(pixmap)
        windows.champ.setText(champs[n])
        roles(roless[n])

        a = a + 1
        if a >= 200:
            timer.stop()
            windows.generate.setText("PLAY")
            windows.generate.setStyleSheet("color: white; background-color: red; font-size: 20px; font-weight: bold;")
            a = 75
            windows.generate.setEnabled(True)
            windows.roles.setEnabled(True)
    except Exception as e:
        print(f"An error occurred: {e}")



def generate_click():
    try:
        if windows.roles.currentText() == "Random":
            n = randint(0, len(pix) - 1)
            return n
        else:
            while True:
                n = randint(0, len(pix) - 1)
                if windows.roles.currentText() in roless[n]:
                    return n
    except:
        pass
def fill():
    for i in range(len(champs)):
        pix.append(imag(champs[i]))
    windows.loading.setText("All Images Loaded!⚡")

app = QApplication([])
windows = loadUi("generchamp.ui")
response = requests.get("https://www.thesun.co.uk/wp-content/uploads/2023/01/League-of-Legends-key-art.jpg")
image_data = BytesIO(response.content)
pixmap = QPixmap()
pixmap.loadFromData(image_data.getvalue())
windows.img.setPixmap(pixmap)
icon_size = QSize(35, 35)
windows.roles.setIconSize(icon_size)
windows.roles.addItem(QIcon(QPixmap('roles/Random.png')), 'Random')
windows.roles.addItem(QIcon(QPixmap('roles/Top.png')), 'Top')
windows.roles.addItem(QIcon(QPixmap('roles/Jungle.png')), 'Jungle')
windows.roles.addItem(QIcon(QPixmap('roles/Mid.png')), 'Mid')
windows.roles.addItem(QIcon(QPixmap('roles/ADC.png')), 'ADC')
windows.roles.addItem(QIcon(QPixmap('roles/Support.png')), 'Support')
timer = QTimer()
timer.timeout.connect(show)

filling = threading.Thread(target=fill)
filling.start()


windows.generate.clicked.connect(show)
windows.setWindowTitle("League of Legends Champs Generator")
if not os.path.exists('images'):
    # Create the folder
    os.makedirs('images')
sleep(0.10)
windows.show()
app.exec_()


