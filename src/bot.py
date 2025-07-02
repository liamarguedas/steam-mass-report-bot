
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyautogui
import random
import subprocess
import platform


class ReportBot:


    def __init__(self):

        self.edge = self.configure_driver()


    def kill_edge_processes(self):
        if platform.system() == "Windows":
            try:
                subprocess.run("taskkill /F /IM msedge.exe /T", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run("taskkill /F /IM msedgedriver.exe /T", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print("⚠️ Edge processes were not running or could not be killed.")
        else:
            print("⚠️ This method is designed for Windows only.")

    def configure_driver(self):

        self.kill_edge_processes()

        options = webdriver.EdgeOptions()

        edge_data_dir = "C:\\Users\\liams\\AppData\\Local\\Microsoft\\Edge\\User Data"
        profile_dir = "Default"
        options.add_argument(f"--user-data-dir={edge_data_dir}")
        options.add_argument(f"--profile-directory={profile_dir}")
        options.add_argument("--disable-blink-features=AutomationControlled")

        edge = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()),
        options=options)

        return edge 


    def read_list(self):
        with open("../file/list.txt", "r", encoding="utf-8") as file:
            lista_de_viados = file.readlines()

    
        lista_de_viados = [viado for viado in lista_de_viados if viado != "https://steamcommunity.com/profiles/76561198098549323"]

        return lista_de_viados


    def read_comments(self):

        with open("../file/commentarios.txt", "r", encoding="utf-8") as file:

            lista_de_comentarios = file.readlines()

        return lista_de_comentarios 





    def run(self):

        viados = self.read_list()
        comments = self.read_comments()

        for viado in viados:
            time.sleep(2)

            commentario_pro_viado = random.choice(comments) 

            self.edge.get(viado)


            btns = self.edge.find_elements(By.CLASS_NAME, "btn_profile_action.btn_medium")
            btns[1].click()
            self.edge.find_element(By.XPATH, '//*[@id="profile_action_dropdown"]/div[9]/a[4]').click()
            time.sleep(1)

            self.edge.find_element(By.XPATH, '//*[@id="step_content"]/div[6]').click()
            
            time.sleep(1)
            self.edge.find_element(By.XPATH, '//*[@id="report_button"]/div[1]').click()

            time.sleep(1)
            self.edge.find_element(By.XPATH, '//*[@id="report_txt_input"]').send_keys(commentario_pro_viado)

            time.sleep(1)

            jogos = self.edge.find_elements(By.CLASS_NAME,"game_button_label") 

            time.sleep(1)
            for jogo in jogos:

                if jogo.text == "Counter-Strike 2":
                    jogo.click()

                    time.sleep(1)
                    break

            self.edge.find_element(By.XPATH, '//*[@id="btn_submit_report"]/span').click()


if __name__ == "__main__":
    bot = ReportBot()
    bot.run()
