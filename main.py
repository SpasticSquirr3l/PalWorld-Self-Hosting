from tkinter import messagebox, ttk

import tkinter
import customtkinter
import webbrowser
import os
import configparser
import requests, zipfile, io
import threading
import time
from winpty import PtyProcess
#import ptyprocess as PtyProcess
import subprocess
# from pages.steamcmddownload import SteamCMDStatusApp


    
config=configparser.ConfigParser()
config.optionxform=str
if not os.path.exists('config.ini'):
    config['steamCMD'] = {'runtime':'', 'steamcmdpath':'', 'installpath':''}
    config['palworld_management'] = {'AdminPassword':'""',
'AutoResetGuildTimeNoOnlinePlayers':'72',
'bActiveUNKO':'FALSE',
'BanListURL':'"https://api.palworldgame.com/api/banlist.txt"',
'BaseCampMaxNum':'128',
'BaseCampWorkerMaxNum':'15',
'bAutoResetGuildNoOnlinePlayers':'FALSE',
'bCanPickupOtherGuildDeathPenaltyDrop':'FALSE',
'bEnableAimAssistKeyboard':'FALSE',
'bEnableAimAssistPad':'TRUE',
'bEnableDefenseOtherGuildPlayer':'FALSE',
'bEnableFastTravel':'TRUE',
'bEnableFriendlyFire':'FALSE',
'bEnableInvaderEnemy':'TRUE',
'bEnableNonLoginPenalty':'TRUE',
'bEnablePlayerToPlayerDamage':'FALSE',
'bExistPlayerAfterLogout':'FALSE',
'bIsMultiplay':'FALSE',
'bIsPvP':'FALSE',
'bIsStartLocationSelectByMap':'TRUE',
'BuildObjectDamageRate':'1',
'BuildObjectDeteriorationDamageRate':'1',
'bUseAuth':'TRUE',
'CollectionDropRate':'1',
'CollectionObjectHpRate':'1',
'CollectionObjectRespawnSpeedRate':'1',
'CoopPlayerMaxNum':'4',
'DayTimeSpeedRate':'1',
'DeathPenalty':'All',
'Difficulty':'None',
'DropItemAliveMaxHours':'1',
'DropItemMaxNum_UNKO':'100',
'DropItemMaxNum':'3000',
'EnemyDropItemRate':'1',
'ExpRate':'1',
'GuildPlayerMaxNum':'20',
'NightTimeSpeedRate':'1',
'PalAutoHPRegeneRate':'1',
'PalAutoHpRegeneRateInSleep':'1',
'PalCaptureRate':'1',
'PalDamageRateAttack':'1',
'PalDamageRateDefense':'1',
'PalEggDefaultHatchingTime':'72',
'PalSpawnNumRate':'1',
'PalStaminaDecreaceRate':'1',
'PalStomachDecreaceRate':'1',
'PlayerAutoHPRegeneRate':'1',
'PlayerAutoHpRegeneRateInSleep':'1',
'PlayerDamageRateAttack':'1',
'PlayerDamageRateDefense':'1',
'PlayerStaminaDecreaceRate':'1',
'PlayerStomachDecreaceRate':'1',
'PublicIP':'""',
'PublicPort':'8211',
'RCONEnabled':'FALSE',
'RCONPort':'25575',
'Region':'""',
'ServerDescription':'""',
'ServerName':'"Default',
'ServerPassword':'""',
'ServerPlayerMaxNum':'32',
'WorkSpeedRate':'1',
}
    config.write(open('config.ini', 'w'))


config.read('config.ini')


DARK_MODE = "dark"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("dark-blue")




class WrappingLabel(tkinter.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tkinter.Label.__init__(self, master, **kwargs, bg='#000811', fg='#ffffff', font=("Segoe UI", 25))
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))



# class WrappingLabel(customtkinter.CTkLabel):
#     '''a type of Label that automatically adjusts the wrap to the size'''
#     def __init__(self, master=None, **kwargs):
#         customtkinter.CTkLabel.__init__(self, master, **kwargs, font=(...,20))
#         self.bind('<Configure>', lambda e: self.configure(wraplength=round(self.winfo_width()-(self.winfo_width()*.35))))











def callback(url):
    webbrowser.open_new(url)




class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        
        self.title("Palworld Server Manager")
        # remove title bar , page reducer and closing page !!!most have a quit button with app.destroy!!! (this app have a quit button so don't worry about that)
        # self.overrideredirect(True)
        # make the app as big as the screen (no mater wich screen you use) 
        # self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.geometry('1000x800')
        self.resizable(True,True)

        # root!
        self.main_container = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        # left side panel -> for frame selection
        self.left_side_panel = customtkinter.CTkFrame(self.main_container, width=150, corner_radius=10)
        self.left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)
        
        # self.left_side_panel.grid_columnconfigure(0, weight=1)
        # self.left_side_panel.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
        self.left_side_panel.grid_rowconfigure(5, weight=1)
        
        
        # self.left_side_panel WIDGET
        customtkinter.CTkLabel(self.left_side_panel, text="Navigation \n", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))

        customtkinter.CTkButton(self.left_side_panel, text="Install Servers", command=self.steamcmd, width=3).grid(row=1, column=0, padx=20, pady=10)

        customtkinter.CTkButton(self.left_side_panel, text="Server Configurations", command=self.config).grid(row=2, column=0, padx=20, pady=10)

        customtkinter.CTkButton(self.left_side_panel, text="Server Monitoring", command=self.statement).grid(row=3, column=0, padx=20, pady=10)
        
        customtkinter.CTkButton(self.left_side_panel, text="Help", command=self.help).grid(row=4, column=0, padx=20, pady=10)

        customtkinter.CTkLabel(self.left_side_panel, text="Appearance Mode:", anchor="w").grid(row=6, column=0, padx=20, pady=(10, 0))
        
        systemTheme = customtkinter.CTkOptionMenu(self.left_side_panel, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        systemTheme.grid(row=7, column=0, padx=20, pady=(10, 20), sticky = "s")
        systemTheme.set("Dark")

        self.scaling_label = customtkinter.CTkLabel(self.left_side_panel, text="UI Scaling:", anchor="w").grid(row=8, column=0, padx=20, pady=(10, 0))
        
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.left_side_panel, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20), sticky = "s")
        self.scaling_optionemenu.set("100%")

        self.bt_Quit = customtkinter.CTkButton(self.left_side_panel, text="Quit", fg_color= '#EA0000', hover_color = '#B20000', command= self.close_window)
        self.bt_Quit.grid(row=10, column=0, padx=20, pady=10)
        
    
        
        

        # right side panel -> have self.right_dashboard inside it
        self.right_side_panel = customtkinter.CTkFrame(self.main_container, corner_radius=10, fg_color="#000811")
        self.right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        
        
        self.right_dashboard = customtkinter.CTkScrollableFrame(self.main_container, corner_radius=10, fg_color="#000811")
        self.right_dashboard.pack(in_=self.right_side_panel, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

        
        self.welcomeMessage = WrappingLabel(self.right_dashboard, text="Welcome Palworld Server Manager!\n\nIf you have any issues please use github so we can all track them and improve.")
        self.welcomeMessage.pack(expand=False, fill=tkinter.X)
        # self.win.grid(row=1, column=0, padx=20, pady=(10, 0))
       

       # self.right_dashboard2 = customtkinter.CTkLabel(self.right_dashboard, text="Welcome to my newly created Palworld Server Manager! If you have any issues please use github so we can all track them and improve. This script will manage steamCMD behind the scene and will prompt you for all additional server options.", wraplength=self.main_container.winfo_width() - 20).grid(row=0, column=0, padx=20, pady=(10, 0))
        
        # self.right_dashboard2 = customtkinter.CTkLabel(self.right_dashboard, text="Welcome to my newly created Palworld Server Manager! If you have any issues please use github so we can all track them and improve. This script will manage steamCMD behind the scene and will prompt you for all additional server options.")
        # self.right_dashboard2.bind('<Configure>', lambda e: self.right_dashboard.config(wraplength=self.right_dashboard.winfo_width()))

















































    #  self.right_dashboard   ----> dashboard widget  
    def config(self):
        self.clear_frame()

        

        self.bt_from_frame1 = customtkinter.CTkButton(self.right_dashboard, text="Palworld", command=self.palworld).grid(row=1, column=0, padx=20, pady=(10, 0))
        self.bt_from_frame2 = customtkinter.CTkButton(self.right_dashboard, text="Other Steam Servers???\nTBD at best").grid(row=2, column=0, padx=20, pady=(10, 0))

        # self.bt_from_frame3 = customtkinter.CTkLabel(self.right_dashboard, text="Welcome to my newly created Palworld Server Manager! If you have any issues please use github so we can all track them and improve. This script will manage steamCMD behind the scene and will prompt you for all additional server options.")
        # self.bt_from_frame3.grid(row=3, column=0, padx=20, pady=(10, 0))

    #  self.right_dashboard   ----> statement widget
    def statement(self):
        self.clear_frame()

        customtkinter.CTkLabel(self.right_dashboard, text="Palworld Monitoring", font=customtkinter.CTkFont(size=20, weight="bold"), wraplength=550).grid(row=0, column=0, columnspan=3, padx=0, pady=0)


        customtkinter.CTkButton(self.right_dashboard, text="Start Server", command=lambda:self.runServer()).grid(row=1, column=0, padx=20, pady=(10, 0))

        customtkinter.CTkButton(self.right_dashboard, text="Stop Server", command=lambda:os.system(f'TASKKILL /im PalServer-Win64-Test-Cmd.exe /f')).grid(row=1, column=1, padx=20, pady=(10, 0))
        
    
    #  self.right_dashboard   ----> categories widget
    def help(self):
        self.clear_frame()
        # self.bt_from_frame4 = customtkinter.CTkButton(self.right_dashboard, text="categories", command=lambda:print("test cats") )
        # self.bt_from_frame4.grid(row=0, column=0, padx=20, pady=(10, 0))



        self.link1_txt = customtkinter.CTkLabel(self.right_dashboard, text="GitHub: ")
        
        self.link1_txt.grid(row=0, column=0, padx=20, pady=(10, 0))

        self.link1_url = customtkinter.CTkLabel(self.right_dashboard, text="https://github.com/SpasticSquirr3l/PalWorld-Self-Hosting", cursor="hand2", text_color="green")
        self.link1_url.bind("<Button-1>", lambda e: callback("http://www.example.com"))
        self.link1_url.grid(row=0, column=1, padx=20, pady=(10, 0))



    def change_appearance_mode_event(self, apperance):
        customtkinter.set_appearance_mode(apperance)


    # Change scaling of all widget 80% to 120%
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
        
    # close the entire window    
    def close_window(self): 
            App.destroy(self)
            
            
    # CLEAR ALL THE WIDGET FROM self.right_dashboard(frame) BEFORE loading the widget of the concerned page       
    def clear_frame(self):
        for widget in self.right_dashboard.winfo_children():
            widget.destroy()














    def installCMD(self):
        config['steamCMD']['steamcmdpath'] = customtkinter.filedialog.askdirectory()

        if config.get('steamCMD','steamcmdpath'):
            try:
                r = requests.get(r"https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip")
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall(config['steamCMD']['steamcmdpath'])
                
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                messagebox.showinfo("SteamCMD Installed!", "SteamCMD Installed!\n"+config['steamCMD']['steamcmdpath'])
            except Exception as e:
                messagebox.showinfo("SteamCMD Install Error", f'Error Log:\n{e}')
            self.steamCMDValue.set(config['steamCMD']['steamcmdpath'])

    def currentSteamCMD(self):
        config['steamCMD']['steamcmdpath'] = customtkinter.filedialog.askdirectory(title="SteamCMD Installation Directory")

        if config.get('steamCMD','steamcmdpath'):
            with open('config.ini', 'w') as configfile:
                    config.write(configfile)
            self.steamCMDValue.set(config['steamCMD']['steamcmdpath'])

    def installationPath(self):
        config['steamCMD']['installpath'] = customtkinter.filedialog.askdirectory(title="Game Installation Directory")

        if config.get('steamCMD','installpath'):
            with open('config.ini', 'w') as configfile:
                    config.write(configfile)
            self.installdir.set(config['steamCMD']['installpath'])

    def checkGame(self, choice):
        self.installGame = choice
        print("combobox dropdown clicked:", self.installGame)
    



    def runCMD(self):        
        print('runcmd starting')
        steamCMDEXE = [
            f'{config["steamCMD"]["steamcmdpath"]}\\steamCMD.exe ',
                        '+@ShutdownOnFailedCommand 1 ',
                        '+@NoPromptForPassword 1 ',
                        '+quit']
        if "/" in steamCMDEXE:
            steamCMDEXE = steamCMDEXE.replace("/", "\\\\")
        process = PtyProcess.spawn(steamCMDEXE)
        
        while process.isalive():
            print(process.readline())
            output = process.readline()
            if output:
                progress = self.extract_progress(output)   
                if progress is not None:
                    self.progress_var.set(progress)
                    time.sleep(.02)
                    
      
            
            # time.sleep(0.2)
            
        print('finished')

        self.status_var.set("SteamCMD First Run Complete")
        self.progress_var.set(100)
        config["steamCMD"]["runtime"] = "True"
        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        
        time.sleep(1)
        self.status_var.set(f"{self.installGame} Installing")
        self.progress_var.set(0)
        time.sleep(1)
        self.update_status()
            



    def installServer(self):
        self.status_var = tkinter.StringVar()
        self.status_var.set("Starting SteamCMD")

        self.status_label = ttk.Label(self.right_dashboard, textvariable=self.status_var, anchor="w")
        self.status_label.grid(row=0, column=3, sticky="ew")

        self.progress_var = tkinter.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.right_dashboard, length=150, maximum=100, mode="determinate", variable=self.progress_var)
        self.progress_bar.grid(row=1, column=3, sticky="ne")


        if config["steamCMD"]["runtime"] != "True":
            self.i=0
            self.t1 = threading.Thread(target=self.runCMD)
            self.t1.start()
        else:
            self.t1 = threading.Thread(target=self.update_status)
            self.t1.start()
        

    def runServer(self):
        serverSettings_TopLevel = f'{config["steamCMD"]["installpath"]}\Pal\Saved\Config\WindowsServer'
        os.makedirs(serverSettings_TopLevel, exist_ok=True)
        serverSettings_Path = f'{config["steamCMD"]["installpath"]}\Pal\Saved\Config\WindowsServer\PalWorldSettings.ini'

        if "/" in serverSettings_Path:
            serverSettings_Path = serverSettings_Path.replace("/", "\\")
        
        palworldSettings = config.items('palworld_management')

        

        with open(serverSettings_Path, "w") as palWorldSettings:
            palWorldSettings.write(f'[/Script/Pal.PalGameWorldSettings]\n')
            palWorldSettings.write('OptionSettings=(')
            for i, (param, value) in enumerate(palworldSettings): 
                palWorldSettings.write(f'{param}={value},')
        
        palWorldSettings.close()

        server = [
            f'{config["steamCMD"]["installpath"]}\PalServer.exe ',
            '-useperfthreads ',
            '-NoAsyncLoadingThread ',
            '-UseMultithreadForDS',
        ]

        if "/" in server:
            server = server.replace("/", "\\\\")
        
        self.server = subprocess.Popen(server)



    def update_status(self):
        
        steamCMDEXE = [
            f'{config["steamCMD"]["steamcmdpath"]}\\steamCMD.exe ',
            '+@ShutdownOnFailedCommand 1 ',
            '+@NoPromptForPassword 1 ',
            f'+force_install_dir "{config["steamCMD"]["installpath"]}" ',
            '+login anonymous ',
            f'+app_update {self.games[self.installGame]} ',
            'validate ',
            '+logoff ',
            '+quit'
        ]


        if "/" in steamCMDEXE:
            steamCMDEXE = steamCMDEXE.replace("/", "\\\\")
        
        process = PtyProcess.spawn(steamCMDEXE)

        while process.isalive():
            print(process.readline())
            output = process.readline()
            if output:
                progress = self.extract_progress(output)
                if progress is not None:
                    self.progress_var.set(progress)
                    time.sleep(0.2)  # Introduce a small delay to allow GUI updates

        # Update status when steamCMD.exe finishes
        # self.status_var.set("SteamCMD Finished")
        # self.progress_var.set(100)
            # process_stdout
        # i=0
        
        # while True:
        #     if process.poll() is not None:
        #         break
        #     for line in iter(process.stdout.readlines()):
        #         print (line)

        # while True:
        #     time.sleep(0.01) #do smth
        #     bytes_number = process.stdout.seek(0, 2)
        #     if bytes_number:
        #         print('number of new bytes: ', bytes_number)
        #         process.stdout.seek(0, 0)
        #         print(process.stdout.read(bytes_number))
        #     if process.poll() is not None and not bytes_number:
        #         break

        print('done!')


    def extract_progress(self, output):
        try:
            if "Downloading update" in output:
                self.status_var.set("SteamCMD Updating")
                progress = int(float((output[output.index('[') + 1:output.index('%', output.index('['))].strip()).replace(" ", "")))
            elif "Applying update" in output or "Extracting package" in output or "Installing update" in output:
                self.status_var.set("SteamCMD Applying Updates")
                progress = 10
            elif "Update complete:" in output:
                self.status_var.set("SteamCMD Update complete")
                progress = 20

            elif "reconfiguring, progress" in output:
                self.status_var.set(f"{self.installGame} Reconfiguring")
                progress = int(float((output[output.index(':') + 1:output.index('(', output.index(':'))].strip()).replace(" ", "")))
            elif "downloading, progress" in output:
                self.status_var.set(f"{self.installGame} Downloading")
                progress = int(float((output[output.index(':') + 1:output.index('(', output.index(':'))].strip()).replace(" ", "")))
                self.i=1

            elif "verifying update" in output:
                self.status_var.set(f"{self.installGame} Verifying")
                progress = int(float((output[output.index(':') + 1:output.index('(', output.index(':'))].strip()).replace(" ", "")))

            elif "OK" in output and self.i == 1:
                self.status_var.set(f"{self.installGame} SteamCMD Complete")
                progress = 100
            else:
                progress = None
        except:
            progress = None
        return progress
    





    def steamcmd(self):
        self.clear_frame()

        self.steamCMDValue = customtkinter.StringVar()
        self.installdir = customtkinter.StringVar()

        if config.get('steamCMD','steamcmdpath'):
            self.steamCMDValue.set(config['steamCMD']['steamcmdpath'])

        if config.get('steamCMD','installpath'):
            self.installdir.set(config['steamCMD']['installpath'])

        customtkinter.CTkButton(self.right_dashboard, text="Install SteamCMD", command=lambda:self.installCMD()).grid(row=0, column=0, columnspan=3, padx=20, pady=(10, 0), sticky="ew")

        customtkinter.CTkLabel(self.right_dashboard, text="SteamCMD should be installed to a folder. Many files are created.", text_color="yellow").grid(row=1, column=0, columnspan=3, padx=0, pady=(0, 40), sticky="ew")
        # ============================================================================
        # ============================================================================
        # ============================================================================
        customtkinter.CTkLabel(self.right_dashboard, text="Already Installed?\nSteamCMD Folder:").grid(row=2, column=0, padx=20, pady=(10, 0))
        
        customtkinter.CTkButton(self.right_dashboard, text="Browse", command= lambda:[self.currentSteamCMD()]).grid(row=2, column=1, padx=20, pady=(10, 0))
           
        customtkinter.CTkLabel(self.right_dashboard, textvariable=self.steamCMDValue).grid(row=2, column=2, padx=20, pady=(10, 0))
        # ============================================================================
        # ============================================================================
        # ============================================================================
        customtkinter.CTkLabel(self.right_dashboard, text="Directory for Game Installs:").grid(row=3, column=0, padx=20, pady=(10, 0))
        
        customtkinter.CTkButton(self.right_dashboard, text="Browse", command= self.installationPath).grid(row=3, column=1, padx=20, pady=(10, 0))
           
        customtkinter.CTkLabel(self.right_dashboard, textvariable=self.installdir).grid(row=3, column=2, padx=20, pady=(10, 0))
        # ============================================================================
        # ============================================================================
        # ============================================================================
        customtkinter.CTkLabel(self.right_dashboard, text="Install a Server?").grid(row=4, column=0, padx=20, pady=(10, 0))
        
        self.games={'palworld':'2394010'}
        

        self.gameSelection = customtkinter.CTkComboBox(self.right_dashboard,values=list(self.games.keys()),state='readonly',command=self.checkGame).grid(row=4, column=1, padx=20, pady=(10, 0))
        
        # print(self.gameSelected.current)

        # self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.right_dashboard, values=list(self.games.keys()))
        # self.scaling_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 20), sticky = "s")
        # self.scaling_optionemenu.set(list(self.games.keys())[0])

        customtkinter.CTkButton(self.right_dashboard, text="Install Server", command= self.installServer).grid(row=4, column=2, padx=20, pady=(10, 0))




        





    































    def save_config(self, param, value):
        config.set('palworld_management', param, value)
        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


    def palworld(self):
        self.clear_frame()
        customtkinter.CTkLabel(self.right_dashboard, text="Below are all of the DEFAULT palworld settings. Please take a moment to change at least the following: AdminPassword, PublicIP, ServerName, ServerPlayerMaxNum. \n\n YOU HAVE TO CLICK INTO ANOTHER BOX FOR THE VALUE TO SAVE!", text_color="yellow", wraplength=550).grid(row=0, column=0, columnspan=3, padx=0, pady=(0, 40), sticky="ew")
        
        palworldSettings = config.items('palworld_management')
        
        entries = {}
        
        customtkinter.CTkLabel(self.right_dashboard, text="Parameters", text_color="yellow").grid(row=1, column=0, padx=20, pady=(0), sticky="nesw")

        customtkinter.CTkLabel(self.right_dashboard, text="Values", text_color="yellow").grid(row=1, column=1, padx=(0,0), pady=(0), sticky="nesw")

        customtkinter.CTkLabel(self.right_dashboard, text="Description", text_color="yellow").grid(row=1, column=2, padx=(80), pady=(0), sticky="nesw")

        for i, (param, default_value) in enumerate(palworldSettings): 
            i += 2
            label = customtkinter.CTkLabel(self.right_dashboard, text=param)
            label.grid(row=i, column=0, padx=5, pady=0, sticky="W")
            entry = customtkinter.CTkEntry(self.right_dashboard)
            entry.insert(0, config.get('Addresses', param, fallback=str(default_value)))
            entry.grid(row=i, column=1, padx=5, pady=0, sticky="W")
            entry.bind("<FocusOut>", lambda event, param=param, entry=entry: self.save_config(param, entry.get()))
            entries[param] = entry
            

        description=[
            "Sets the password for server administration.",
            "Sets the time after which guilds with no online players are automatically reset.",
            "Activates or deactivates UNKO (Unidentified Nocturnal Knock-off).",
            "Sets the URL for the server's ban list.",
            "Sets the maximum number of base camps that can be built.",
            "Sets the maximum number of workers in a base camp.",
            "Automatically resets guilds with no online players.",
            "Enables or disables the pickup of death penalty drops from other guilds.",
            "Enables or disables aim assist for keyboards.",
            "Enables or disables aim assist for controllers.",
            "Enables or disables the defense of other guild players.",
            "Enables or disables fast travel.",
            "Enables or disables friendly fire.",
            "Enables or disables invader enemies.",
            "Enables or disables non-login penalties.",
            "Enables or disables player-to-player damage.",
            "Enables or disables the existence of players after logout.",
            "Enables or disables multiplayer mode.",
            "Enables or disables player versus player (PvP) mode.",
            "Enables or disables the selection of starting locations on the map.",
            "Adjusts the rate at which built objects take damage.",
            "Adjusts the rate at which built objects deteriorate.",
            "Enables or disables server authentication.",
            "Adjusts the drop rate of collected items.",
            "Adjusts the health of collected objects.install steamc",
            "Adjusts the respawn speed of collected objects.",
            "Sets the maximum number of cooperative players in a session.",
            "Modifies the speed of in-game time during the day.",
            "Defines the penalty upon player death (e.g., All, None).",
            "Adjusts the overall difficulty of the game.",
            "Sets the maximum time items remain alive after being dropped.",
            "Sets the maximum number of dropped items in the game.",
            "Sets the maximum number of dropped UNKO items in the game.",
            "Adjusts the drop rate of items from defeated enemies.",
            "Changes the experience gain rate for both players and creatures.",
            "Sets the maximum number of players in a guild.",
            "Modifies the speed of in-game time during the night.",
            "Adjusts the rate of automatic Pal creature health regeneration.",
            "Adjusts the rate of automatic Pal creature health regeneration during sleep.",
            "Adjusts the rate at which Pal creatures can be captured.",
            "Fine-tunes Pal creature damage dealt.",
            "Fine-tunes Pal creature damage received.",
            "Sets the default hatching time for Pal eggs.",
            "Adjusts the rate at which Pal creatures spawn.",
            "Adjusts the rate at which Pal creature stamina decreases.",
            "Adjusts the rate at which Pal creature stomach decreases.",
            "Adjusts the rate of automatic player health regeneration.",
            "Adjusts the rate of automatic player health regeneration during sleep.",
            "Fine-tunes player damage dealt.",
            "Fine-tunes player damage received.",
            "Adjusts the rate at which the player's stamina decreases.",
            "Adjusts the rate at which the player's stomach decreases.",
            "Sets the public IP address for the Palworld server.",
            "Sets the public port for the Palworld server.",
            "Enables or disables Remote Console (RCON) for server administration.",
            "Sets the port for Remote Console (RCON) communication.",
            "Sets the region for the Palworld server.",
            "Provides a description for the Palworld server.",
            "Sets the name of the Palworld server.",
            "Sets the password for joining the Palworld server.",
            "Sets the maximum number of players allowed on the server.",
            "Adjusts the overall work speed in the game.",

        ]
        for i, (descript) in enumerate(description):
            i += 2
            label = customtkinter.CTkLabel(self.right_dashboard, text=descript, wraplength=300)
            label.grid(row=i, column=2, padx=5, pady=10)

        
































a = App()
a.mainloop()






# app = CTk()
# app.geometry('500x400')

# set_appearance_mode('dark')
# btn = CTkButton(master=app, text='click me', corner_radius=32, fg_color='#4158d0', hover_color='#C850C0', border_color='#ffcc70', border_width=2)
# btn.place(relx=0.5, rely=0.5, anchor ='center')

# app.mainloop()