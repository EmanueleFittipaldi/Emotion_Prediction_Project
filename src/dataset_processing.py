""" queste funzioni effettuano un'elaborazione del dataset, estraendo i landmark dalle immagini e aggiungendo le etichette mancanti"""

import os
import utils as utils
import cv2
from matplotlib import pyplot as plt
import pandas as pd

# path del dataset CK+
path_dataset = "Dataset/cohn-kanade-images"
# path label
path_label = "Dataset/Emotion"
Dataset_folders = utils.get_directories(path_dataset=path_dataset)
Emotion_folders = utils.get_directories(path_dataset=path_label)

def process_landmarks(Dataset_folders):
    """
                    funzione che estrae landmark dalle immagini

                   - **Returns**:
                   - **Value return** has type
                   - Parameter **values**:
                   - **Precondition**:
    """
    # loop nelle diverse cartelle per andare ad ottenere le singole immagini dei soggetti ed estrarre i landmark
    for dir in sorted(Dataset_folders):
        for img in os.listdir(dir):
            utils.extract_landmarks(dir,img)

def missing_emotion_labels():
    """
                    funzione che aggiunge le etichette delle emozioni mancanti

                   - **Returns**:
                   - **Value return** has type
                   - Parameter **values**:
                   - **Precondition**:
        """
    # ottenimento delle cartelle in cui non sono presenti le etichette dell'emozioni
    missing_EMlabels = [x for x in sorted(Emotion_folders) if len(x) == 0]

    if len(missing_EMlabels) == 0:
        print("Tutte le label per le emozioni sono state aggiunte")
    else:
        f = plt.figure()
        valueString = ".0000000e+00"
        for dir in Dataset_folders:
            for missing in missing_EMlabels:
                if dir.find(missing[16:]) != -1:
                    all_imges = sorted(os.listdir(dir))
                    image = cv2.imread(os.path.join(dir,all_imges[len(os.listdir(dir))-1]))
                    plt.imshow(image)
                    plt.show()
                    while(True):
                        val = input("Enter value of emotion: ")
                        if val != "":
                            filename = os.path.join(missing, all_imges[len(os.listdir(dir)) - 1].replace(".png","_emotion.txt"))
                            f = open(filename, 'w')
                            f.write(val + valueString)
                            f.close()
                            break

def missing_gender_labels():
    """
                    funzione che permette di aggiungere le etichette sui sessi

                   - **Returns**:
                   - **Value return** has type
                   - Parameter **values**:
                   - **Precondition**:
        """
    for dir in sorted(Dataset_folders):
        all_imges = sorted(os.listdir(dir))
        filename = os.path.join(dir, all_imges[len(os.listdir(dir)) - 1]) \
            .replace("cohn-kanade-images", "Emotion") \
            .replace(".png", "_gender.txt")

        if not os.path.exists(filename):
            while (True):
                # Uomo = 0
                # Donna = 1
                val = input("Enter value of gender: ")
                if val != "" or val != 0 or val != 1:
                    f = open(filename, 'w')
                    f.write(val)
                    f.close()
                    break

def insert_labels_to_csv(path_label, path_GDcsv):
    """
                    funzione che permette di aggiungere etichette di emozione e sesso ai csv delle distanze

                   - **Returns**:
                   - **Value return** has type
                   - Parameter **values**:
                   - **Precondition**:
        """
    dataset_labels = utils.get_directories(path_dataset=path_label)
    for dir in sorted(dataset_labels):
        for file in sorted(os.listdir(dir)):
            filename = os.path.join(dir, file)

            f = open(filename, "r")
            string_formatted = f.read().strip()
            f.close()

            csv = [c for c in os.listdir(path_GDcsv) if os.path.basename(c).startswith(file[:8])]
            df = pd.read_csv(os.path.join(path_GDcsv, csv), header=None)
            df[len(df.columns)] = string_formatted
            df.to_csv(os.path.join(path_GDcsv, csv), index=False, header=None)

# process_landmarks(Dataset_folders)
missing_emotion_labels()
missing_gender_labels()
# insert_labels_to_csv("Dataset/Emotion", "Global_Distances")
# insert_labels_to_csv("Dataset/Emotion", "Local_Distances")



