import customtkinter as ctk
import minecraft_launcher_lib as mll
import subprocess
import requests
import psutil
import json
import os
from string import ascii_letters, digits, punctuation
from tkinter import messagebox
from threading import Thread
from PIL import Image
from uuid import uuid1
from time import sleep
import language_loader
import ram_loader

minecraft_directory = '.minecraft'
ctk.set_appearance_mode(language_loader.data['appearance_mode'])
vanilla_version_list = []
show_flag = 0

unit = 'GB'
total_ram = psutil.virtual_memory().total
max_ram = ram_loader.convert_bytes(total_ram, unit)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        global vanilla_version_list
        global show_flag

        self.username = str(language_loader.data['username'])
        self.options = {
            'username': self.username,
            'uuid': str(uuid1()),
            'token': ''
        }

        self.installed_versions = mll.utils.get_installed_versions(minecraft_directory=minecraft_directory)
        self.available_versions: list = []

        self.vanilla_version_list = vanilla_version_list

        self.forge_versions = []
        self.forge_version_list = []
        for version in mll.forge.list_forge_versions():
            versionid = version.split('-')[0]
            if versionid not in self.forge_versions:
                self.forge_versions.append(versionid)
        for version in mll.utils.get_version_list():
            if version['id'] in self.forge_versions:
                self.forge_version_list.append(version['id'])

        self.fabric_version_list: list = []
        self.fabric_loader_versions: list = []
        for version in mll.fabric.get_all_minecraft_versions():
            self.fabric_version_list.append(version['version'])
        for version in mll.fabric.get_all_loader_versions():
            self.fabric_loader_versions.append(version['version'])

        self.quilt_version_list: list = []
        self.quilt_loader_versions: list = []
        for version in mll.quilt.get_all_minecraft_versions():
            self.quilt_version_list.append(version['version'])
        for version in mll.quilt.get_all_loader_versions():
            self.quilt_loader_versions.append(version['version'])

        self.WIDTH = 1000
        self.HEIGHT = 600
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x = int((self.screen_width - self.WIDTH) / 2.5)
        self.y = int((self.screen_height - self.HEIGHT) / 3.5)
        self.option_menu_width = 200

        self.title('Minecraft Launcher')
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}+{self.x}+{self.y}')
        self.resizable(False, False)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.iconbitmap('icon.ico')

        self.account_avatar = ctk.CTkImage(Image.open('images\\account_avatar.jpg'), size=(26, 26))
        self.background_image = ctk.CTkImage(Image.open('images\\bg_gradient.jpg'), size=(788, 535))
        self.down_arrow = ctk.CTkImage(light_image=Image.open('images\\down_arrow.png'),
                                       dark_image=Image.open('images\\down_arrow_light.png'),
                                       size=(25, 25))
        self.up_arrow = ctk.CTkImage(light_image=Image.open('images\\up_arrow.png'),
                                     dark_image=Image.open('images\\up_arrow_light.png'),
                                     size=(25, 25))
        self.logout_image = ctk.CTkImage(light_image=Image.open('images\\logout.png'),
                                         dark_image=Image.open('images\\logout_light.png'),
                                         size=(25, 25))

        # CREATE NAVIGATION FRAME
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=('gray89', 'gray17'),
                                             width=200, height=600)
        self.navigation_frame.grid_rowconfigure(5, weight=1)
        self.navigation_frame.grid(row=0, column=0, sticky='ns')

        # Account label
        self.account_label = ctk.CTkLabel(self.navigation_frame, text=f'  {self.username}',
                                          image=self.account_avatar,
                                          compound='left', width=212,
                                          font=ctk.CTkFont(size=20),
                                          fg_color='transparent')
        self.account_label.grid(row=0, column=0, pady=20, sticky='we')

        # Home button
        self.home_frame_button_1 = ctk.CTkButton(self.navigation_frame, text=f'  {language_loader.lang_['home']}',
                                                 text_color=('gray10', 'gray90'), height=40,
                                                 anchor='w', fg_color='transparent', corner_radius=7,
                                                 hover_color=('gray70', 'gray30'), command=self.home_button_event)
        self.home_frame_button_1.grid(row=1, column=0, pady=(10, 0), sticky='we')

        # Instance button
        self.home_frame_button_2 = ctk.CTkButton(self.navigation_frame,
                                                 text=f'  {language_loader.lang_['installations']}',
                                                 text_color=('gray10', 'gray90'), height=40,
                                                 anchor='w', fg_color='transparent', corner_radius=7,
                                                 hover_color=('gray70', 'gray30'), command=self.frame_2_button_event)
        self.home_frame_button_2.grid(row=2, column=0, sticky='we')

        # Skins button
        self.home_frame_button_3 = ctk.CTkButton(self.navigation_frame, text=f'  {language_loader.lang_['skins']}',
                                                 text_color=('gray10', 'gray90'), height=40,
                                                 anchor='w', fg_color='transparent', corner_radius=7,
                                                 hover_color=('gray70', 'gray30'), command=self.frame_3_button_event)
        self.home_frame_button_3.grid(row=3, column=0, sticky='we')

        # Settings button
        self.home_frame_button_4 = ctk.CTkButton(self.navigation_frame, text=f'  {language_loader.lang_['settings']}',
                                                 text_color=('gray10', 'gray90'), height=40,
                                                 anchor='w', fg_color='transparent', corner_radius=7,
                                                 hover_color=('gray70', 'gray30'), command=self.frame_4_button_event)
        self.home_frame_button_4.grid(row=4, column=0, sticky='we', pady=(0, 316))

        # Logout button
        self.home_frame_button_5 = ctk.CTkButton(self.navigation_frame, text=f'{language_loader.lang_['logout']}',
                                                 text_color=('gray10', 'gray90'), height=15,
                                                 anchor='w', fg_color='transparent',
                                                 hover_color=('gray89', 'gray17'), image=self.logout_image,
                                                 command=self.logout)
        self.home_frame_button_5.grid(row=5, column=0, sticky='we', padx=10, pady=(0, 100))

        # ==========CREATE HOME FRAME==========
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='transparent')
        self.home_frame.grid_rowconfigure(1, weight=1)

        # background image
        self.home_image_label = ctk.CTkLabel(master=self.home_frame, image=self.background_image, text='')
        self.home_image_label.grid(row=0, column=0, sticky='nsew')

        self.play_frame = ctk.CTkFrame(master=self.home_frame, width=800, height=80,
                                       corner_radius=0, fg_color=('gray80', 'gray20'))
        self.play_frame.grid(row=1, column=0, sticky='nsew')
        self.play_frame.grid_columnconfigure(2, weight=1)

        # Version menu
        self.version_menu = ctk.CTkOptionMenu(master=self.play_frame, height=30, width=180,
                                              values=self.available_versions, dynamic_resizing=False)
        self.version_menu.grid(row=0, column=0, padx=(20, 0), pady=20, sticky='n')

        # Play button
        self.play_button = ctk.CTkButton(master=self.play_frame, text=f'{language_loader.lang_['enter_the_game']}',
                                         width=200, height=40,
                                         command=self.play_button_event)
        self.play_button.grid(row=0, column=1, padx=(120, 0), pady=(15, 0), sticky='n')

        # ==========CREATE SECOND FRAME==========
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='transparent')
        self.second_frame.grid_rowconfigure(9, weight=1)

        self.second_frame_label = ctk.CTkLabel(master=self.second_frame,
                                               text=f'{language_loader.lang_['installations']}', width=600,
                                               fg_color='transparent', anchor='center',
                                               text_color=('gray10', 'gray90'), font=('Calibri', 33))
        self.second_frame_label.grid(row=0, column=0, padx=100, pady=(10, 25))

        # row 1
        self.frame_row_1 = ctk.CTkFrame(self.second_frame, fg_color='transparent')
        self.frame_row_1.columnconfigure(1, weight=1)
        self.frame_row_1.grid(row=1, column=0, sticky='wne', padx=100)

        # installed versions label
        self.version_list_label = ctk.CTkLabel(self.frame_row_1, text=f'{language_loader.lang_['installed_versions']}:',
                                               text_color=('gray10', 'gray90'), font=('Calibri', 16))
        self.version_list_label.grid(row=0, column=0, sticky='nsw')

        # installed versions menu
        self.version_list_menu = ctk.CTkOptionMenu(self.frame_row_1, height=30,
                                                   width=self.option_menu_width,
                                                   values=self.available_versions,
                                                   dynamic_resizing=False)
        self.version_list_menu.grid(row=0, column=1, sticky='nse')

        # row 2
        self.frame_row_2 = ctk.CTkFrame(self.second_frame, fg_color='transparent')
        self.frame_row_2.rowconfigure(5, weight=1)
        self.frame_row_2.columnconfigure(1, weight=1)
        self.frame_row_2.grid(row=2, column=0, sticky='nsew', padx=100, pady=(50, 0))

        # version choice label
        self.version_install_label = ctk.CTkLabel(self.frame_row_2,
                                                  text=f'{language_loader.lang_['choose_the_version']}:',
                                                  text_color=('gray10', 'gray90'), font=('Calibri', 16))
        self.version_install_label.grid(row=0, column=0, sticky='nw')

        # version choice menu
        self.version_install_menu = ctk.CTkOptionMenu(self.frame_row_2, height=30,
                                                      width=self.option_menu_width,
                                                      values=self.vanilla_version_list,
                                                      dynamic_resizing=False,
                                                      command=self.on_selection)
        self.version_install_menu.grid(row=0, column=1, pady=(0, 10), sticky='ne')

        # version type choice segmented button
        self.version_type_choice_segmented_button = ctk.CTkSegmentedButton(self.frame_row_2,
                                                                           values=['Vanilla', 'Forge',
                                                                                   'Fabric', 'Quilt'],
                                                                           height=30,
                                                                           command=self.change_version_list_type)
        self.version_type_choice_segmented_button.grid(row=1, column=0, columnspan=2, pady=(10, 15), sticky='nsew')
        self.version_type_choice_segmented_button.set('Vanilla')

        # install button
        self.install_button = ctk.CTkButton(self.frame_row_2, text='',
                                            text_color='gray90',
                                            width=170, command=self.install_button_event)
        self.install_button.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        self.update_label = ctk.CTkLabel(self.frame_row_2, text='', text_color=('gray10', 'gray90'))
        self.update_label.grid(row=3, column=0, columnspan=2)

        self.update_progress_bar = ctk.CTkProgressBar(self.frame_row_2, width=500)
        self.update_progress_bar.set(0)

        self.percent_label = ctk.CTkLabel(self.frame_row_2, text='', text_color=('gray10', 'gray90'))
        self.percent_label.grid(row=5, column=0, columnspan=2, pady=(0, 50))

        # row 3
        self.frame_row_3 = ctk.CTkFrame(self.second_frame, fg_color='transparent', width=600)
        self.frame_row_3.rowconfigure(5, weight=1)
        self.frame_row_3.columnconfigure(1, weight=1)
        self.frame_row_3.grid(row=3, column=0, sticky='nsew', padx=100)

        # advanced options button
        self.show_flag = show_flag
        self.advanced_options = ctk.CTkButton(self.frame_row_3, text=f'{language_loader.lang_['advanced_options']}',
                                              width=600,
                                              fg_color=('gray92', 'gray14'), text_color=('gray10', 'gray90'),
                                              hover_color=('gray92', 'gray14'), font=('Calibri', 20),
                                              image=self.down_arrow, compound='right', border_spacing=0,
                                              command=self.advanced_option_button_event)
        self.advanced_options.grid(row=0, column=0, columnspan=5, pady=(0, 10))

        # version type label
        self.load_versions_label = ctk.CTkLabel(self.frame_row_3, text=f'{language_loader.lang_['included_versions']}')

        # types frame
        self.types_frame = ctk.CTkFrame(self.frame_row_3, fg_color='transparent')
        self.types_frame.columnconfigure(2, weight=1)

        # snapshot
        self.snapshots_var = ctk.StringVar(value='off')
        self.snapshots = ctk.CTkCheckBox(self.types_frame, text=f'{language_loader.lang_['snapshots']}',
                                         variable=self.snapshots_var,
                                         onvalue='on', offvalue='off', command=self.version_type_button_event)
        self.snapshots.grid(row=0, column=0)

        # beta
        self.old_beta_var = ctk.StringVar(value='off')
        self.old_beta = ctk.CTkCheckBox(self.types_frame, text=f'{language_loader.lang_['beta']}',
                                        variable=self.old_beta_var,
                                        onvalue='on', offvalue='off', width=60, command=self.version_type_button_event)
        self.old_beta.grid(row=0, column=1, padx=50)

        # alpha
        self.old_alpha_var = ctk.StringVar(value='off')
        self.old_alpha = ctk.CTkCheckBox(self.types_frame, text=f'{language_loader.lang_['alpha']}',
                                         variable=self.old_alpha_var, width=80,
                                         onvalue='on', offvalue='off', command=self.version_type_button_event)
        self.old_alpha.grid(row=0, column=2)

        # loading version types
        with open('launch_options.json') as f:
            options = json.load(f)
            if options['include_snapshots'] == 'false':
                self.snapshots_var.set('off')
            elif options['include_snapshots'] == 'true':
                self.snapshots_var.set('on')
            if options['include_beta'] == 'false':
                self.old_beta_var.set('off')
            elif options['include_beta'] == 'true':
                self.old_beta_var.set('on')
            if options['include_alpha'] == 'false':
                self.old_alpha_var.set('off')
            elif options['include_alpha'] == 'true':
                self.old_alpha_var.set('on')

        # loader version frame
        self.loader_versions_label = ctk.CTkLabel(self.frame_row_3, text=f'{language_loader.lang_['loader_version']}')

        self.loader_versions_menu = ctk.CTkOptionMenu(self.frame_row_3, height=30, width=self.option_menu_width,
                                                      dynamic_resizing=False)
        self.loader_versions_menu.set('Error')

        # ==========CREATE THIRD FRAME==========
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='transparent')
        self.third_frame.grid_rowconfigure(1, weight=1)

        self.third_frame_label = ctk.CTkLabel(self.third_frame, text=f'{language_loader.lang_['skins']}', width=600,
                                              text_color=('gray10', 'gray90'), font=('Calibri', 33))
        self.third_frame_label.grid(row=0, column=0, padx=100, pady=(10, 200), sticky='nsew')

        self.section_not_available = ctk.CTkLabel(self.third_frame,
                                                  text=f'{language_loader.lang_['section_not_available']}',
                                                  text_color=('gray10', 'gray90'), font=('Calibri', 25))
        self.section_not_available.grid(row=1, column=0, sticky='n')

        # ==========CREATE FOURTH FRAME==========
        self.fourth_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='transparent')
        self.fourth_frame.grid_rowconfigure(10, weight=1)
        self.fourth_frame.grid_columnconfigure(1, weight=1)

        self.fourth_frame_label = ctk.CTkLabel(master=self.fourth_frame, text=f'{language_loader.lang_['settings']}',
                                               width=600,
                                               text_color=('gray10', 'gray90'), font=('Calibri', 33))
        self.fourth_frame_label.grid(row=0, column=0, padx=100, pady=(10, 25), sticky='wne')

        # row 1
        self.frame_row_1_4 = ctk.CTkFrame(self.fourth_frame, fg_color='transparent')
        self.frame_row_1_4.columnconfigure(1, weight=1)
        self.frame_row_1_4.grid(row=1, column=0, sticky='we', padx=100)

        # languages label
        self.language_list_label = ctk.CTkLabel(self.frame_row_1_4,
                                                text=f'{language_loader.lang_['interface_language']}:',
                                                text_color=('gray10', 'gray90'), font=('Calibri', 16))
        self.language_list_label.grid(row=0, column=0, sticky='wns')

        # available languages menu
        self.language_list_menu = ctk.CTkOptionMenu(self.frame_row_1_4, height=30, width=self.option_menu_width,
                                                    values=[f'{language_loader.lang_['ru']} (Русский)',
                                                            f'{language_loader.lang_['en']} (English)',
                                                            f'{language_loader.lang_['zh']} (中文)'],
                                                    command=self.change_language_event)
        self.language_list_menu.grid(row=0, column=1, sticky='nse')

        # checking statement
        if language_loader.data['language'] == 'ru':
            self.language_list_menu.set(f'{language_loader.lang_['ru']} (Русский)')
        elif language_loader.data['language'] == 'en':
            self.language_list_menu.set(f'{language_loader.lang_['en']} (English)')
        elif language_loader.data['language'] == 'zh':
            self.language_list_menu.set(f'{language_loader.lang_['zh']} (中文)')

        self.current_language = self.language_list_menu.get()

        # row 2
        self.frame_row_2_4 = ctk.CTkFrame(self.fourth_frame, fg_color='transparent')
        self.frame_row_2_4.columnconfigure(1, weight=1)
        self.frame_row_2_4.grid(row=2, column=0, sticky='we', padx=100, pady=10)

        # available themes label
        self.theme_list_label = ctk.CTkLabel(self.frame_row_2_4, text=f'{language_loader.lang_['interface_theme']}:',
                                             text_color=('gray10', 'gray90'), font=('Calibri', 16))
        self.theme_list_label.grid(row=0, column=0, sticky='nsw')

        # available themes menu
        self.theme_list_menu = ctk.CTkOptionMenu(self.frame_row_2_4, height=30, width=self.option_menu_width,
                                                 values=[f'{language_loader.lang_['light']}',
                                                         f'{language_loader.lang_['dark']}',
                                                         f'{language_loader.lang_['system']}'],
                                                 command=self.change_appearance_mode_event)
        self.theme_list_menu.grid(row=0, column=1, sticky='nse')

        # checking statement
        if language_loader.data['appearance_mode'] == 'light':
            self.theme_list_menu.set(f'{language_loader.lang_['light']}')
        elif language_loader.data['appearance_mode'] == 'dark':
            self.theme_list_menu.set(f'{language_loader.lang_['dark']}')
        elif language_loader.data['appearance_mode'] == 'system':
            self.theme_list_menu.set(f'{language_loader.lang_['system']}')

        self.current_theme = self.theme_list_menu.get()

        # row 3
        self.frame_row_3_4 = ctk.CTkFrame(self.fourth_frame, fg_color='transparent')
        self.frame_row_3_4.columnconfigure(1, weight=1)
        self.frame_row_3_4.grid(row=3, column=0, sticky='we', padx=100, pady=10)

        self.resolution_label = ctk.CTkLabel(self.frame_row_3_4, text=f'{language_loader.lang_['resolution']}',
                                             text_color=('gray10', 'gray90'), font=('Calibri', 16))
        self.resolution_label.grid(row=0, column=0, sticky='nsw')

        self.resolution_widgets = ctk.CTkFrame(self.frame_row_3_4, fg_color='transparent')
        self.resolution_widgets.columnconfigure(3, weight=1)
        self.resolution_widgets.grid(row=0, column=1, sticky='nse')

        self.enable_custom_resolution_var = ctk.Variable(value='off')
        self.enable_custom_resolution_checkbox = ctk.CTkCheckBox(self.resolution_widgets,
                                                                 text='', onvalue='on',
                                                                 offvalue='off', width=0,
                                                                 variable=self.enable_custom_resolution_var,
                                                                 command=self.switch_resolution_widgets)
        self.enable_custom_resolution_checkbox.grid(row=0, column=0, padx=(0, 5))

        self.width_entry = ctk.CTkEntry(self.resolution_widgets, placeholder_text=f'{language_loader.lang_['width']}')
        self.width_entry.grid(row=0, column=1)
        self.width_entry.insert(0, language_loader.data['width'])

        self.label_x = ctk.CTkLabel(self.resolution_widgets, text='X',
                                    text_color=('gray10', 'gray90'), font=('Calibri', 16))
        self.label_x.grid(row=0, column=2, padx=5)

        self.height_entry = ctk.CTkEntry(self.resolution_widgets, placeholder_text=f'{language_loader.lang_['height']}')
        self.height_entry.grid(row=0, column=3)
        self.height_entry.insert(0, language_loader.data['height'])

        with open('launch_options.json'):
            if language_loader.data['enable_custom_resolution'] == 'false':
                self.options['customResolution'] = False
                self.enable_custom_resolution_var.set('off')
                self.width_entry.configure(state='disabled')
                self.height_entry.configure(state='disabled')
            elif language_loader.data['enable_custom_resolution'] == 'true':
                self.options['customResolution'] = True
                self.enable_custom_resolution_var.set('on')
                self.width_entry.configure(state='normal')
                self.height_entry.configure(state='normal')

        self.enable_custom_resolution = self.enable_custom_resolution_var.get()

        # row 4
        self.frame_row_4_4 = ctk.CTkFrame(self.fourth_frame, fg_color='transparent')
        self.frame_row_4_4.rowconfigure(2, weight=1)
        self.frame_row_4_4.columnconfigure(1, weight=1)
        self.frame_row_4_4.grid(row=4, column=0, sticky='we', padx=100, pady=(30, 0))

        self.changing_launch_options_label = ctk.CTkLabel(self.frame_row_4_4,
                                                          text=f'{language_loader.lang_['edit_mode']}',
                                                          text_color=('gray10', 'gray90'), font=('Calibri', 20))
        self.changing_launch_options_label.grid(row=0, column=0, columnspan=2)

        self.change_launch_options_segmented_button = ctk.CTkSegmentedButton(self.frame_row_4_4,
                                                                             values=[
                                                                                 f'{language_loader.lang_['simple']}',
                                                                                 f'{language_loader.lang_['advanced']}'],
                                                                             command=self.change_launch_options)
        self.change_launch_options_segmented_button.grid(row=1, column=0, columnspan=2, sticky='we', pady=20)

        self.edit_launch_options_mode = self.change_launch_options_segmented_button.get()

        self.ram_slider = ctk.CTkSlider(self.frame_row_4_4, from_=1, to=int(max_ram), number_of_steps=(max_ram - 1),
                                        width=500, command=self.change_ram)
        if language_loader.data['ram_count'] == 0:
            self.ram_slider.set(max_ram // 2)
        else:
            self.ram_slider.set(language_loader.data['ram_count'])

        self.min_ram = int(self.ram_slider.get()) // 2
        self.max_ram = int(self.ram_slider.get())
        if self.max_ram == 1:
            self.min_ram = 1
        self.options['jvmArguments'] = [f'-Xms{self.min_ram}G', f'-Xmx{self.max_ram}G']

        self.current_ram = self.ram_slider.get()

        self.ram_entry = ctk.CTkEntry(self.frame_row_4_4, width=70)
        self.ram_entry.insert(0, str(int(self.ram_slider.get())) + f' {unit}')
        self.ram_entry.configure(state='disabled')

        self.jvm_args_label = ctk.CTkLabel(self.frame_row_4_4, text=f'{language_loader.lang_['java_args']}',
                                           text_color=('gray10', 'gray90'), font=('Calibri', 16))

        self.jvm_args_entry = ctk.CTkEntry(self.frame_row_4_4)
        self.jvm_args_entry.insert(2, language_loader.data['jvm_args'])

        if language_loader.data['choose_edit_mode'] == 'simple':
            self.change_launch_options_segmented_button.set(f'{language_loader.lang_['simple']}')
            self.ram_slider.grid(row=2, column=0, sticky='we', padx=(0, 20))
            self.ram_entry.grid(row=2, column=1, sticky='e')
        elif language_loader.data['choose_edit_mode'] == 'advanced':
            self.change_launch_options_segmented_button.set(f'{language_loader.lang_['advanced']}')
            self.jvm_args_label.grid(row=2, column=0, sticky='w', padx=(0, 10))
            self.jvm_args_entry.grid(row=2, column=1, sticky='we')

        self.open_minecraft_directory_button = ctk.CTkButton(self.fourth_frame,
                                                             text=f'{language_loader.lang_['open_minecraft_folder']}',
                                                             command=self.open_minecraft_directory)
        self.open_minecraft_directory_button.grid(row=5, column=0, columnspan=2, sticky='s', pady=(20, 0))

        self.save_changes_button = ctk.CTkButton(self.fourth_frame, text=f'{language_loader.lang_['save_changes']}',
                                                 command=self.save_changes)
        self.save_changes_button.grid(row=6, column=0, columnspan=2, sticky='s', pady=(100, 0))

        self.callback = {
            'setStatus': self.set_status,
            'setProgress': self.set_progress,
            'setMax': self.set_max
        }

        # appending versions
        for version in self.installed_versions:
            self.available_versions.append(version['id'])
        self.available_versions = self.available_versions[::-1]
        if self.available_versions == []:
            self.available_versions.append(f'{language_loader.lang_['no_versions']}')
        self.version_menu.configure(values=self.available_versions)
        self.version_list_menu.configure(values=self.available_versions)
        self.version_menu.set(self.available_versions[0])
        self.version_list_menu.set(self.available_versions[0])

        # appending different version types
        for version in mll.utils.get_version_list():
            if version['type'] == 'release':
                self.vanilla_version_list.append(version['id'])
            elif version['type'] == 'snapshot' and self.snapshots_var.get() == 'on':
                self.vanilla_version_list.append(version['id'])
            elif version['type'] == 'old_beta' and self.old_beta_var.get() == 'on':
                self.vanilla_version_list.append(version['id'])
            elif version['type'] == 'old_alpha' and self.old_alpha_var.get() == 'on':
                self.vanilla_version_list.append(version['id'])
        self.version_install_menu.configure(values=self.vanilla_version_list)
        self.version_install_menu.set(self.vanilla_version_list[0])
        self.current_version_list = self.vanilla_version_list

        # checking state
        if self.version_install_menu.get() in self.available_versions:
            self.install_button.configure(text=f'{language_loader.lang_['reinstall']}')
        else:
            self.install_button.configure(text=f'{language_loader.lang_['install']}')

        # ==========CREATE LOGIN FRAME==========
        self.login_frame = ctk.CTkFrame(self, corner_radius=20, fg_color=('gray80', 'gray20'),
                                        width=360, height=300)
        self.login_frame.rowconfigure(3, weight=1)

        self.login_frame_label = ctk.CTkLabel(self.login_frame,
                                              text=f'{language_loader.lang_['welcome_to_the_launcher']}', width=360,
                                              fg_color='transparent', anchor='center',
                                              text_color=('gray10', 'gray90'), font=('Calibri', 20))
        self.login_frame_label.grid(row=0, column=0, pady=(60, 10))

        self.enter_username_label = ctk.CTkLabel(self.login_frame,
                                                 text=f'{language_loader.lang_['enter_the_nickname']}', width=340,
                                                 fg_color='transparent', anchor='w',
                                                 text_color=('gray10', 'gray90'), font=('Calibri', 16))
        self.enter_username_label.grid(row=1, column=0, padx=10)

        self.enter_username_entry = ctk.CTkEntry(self.login_frame,
                                                 placeholder_text=f'{language_loader.lang_['nickname']}',
                                                 width=340)
        self.enter_username_entry.grid(row=2, column=0, padx=10)

        self.login_button = ctk.CTkButton(self.login_frame, text=f'{language_loader.lang_['login']}', width=340,
                                          command=self.change_username)
        self.login_button.grid(row=3, column=0, padx=10, pady=(10, 0), sticky='n')

        if self.username.split() == []:
            self.navigation_frame.grid_forget()
            self.home_frame.grid_forget()
            self.login_frame.grid(row=0, column=0, rowspan=2, columnspan=2, padx=320, pady=(150, 180), sticky='nsew')
        else:
            self.navigation_frame.grid(row=0, column=0, sticky='ns')
            self.select_frame_by_name('home')

    current_max = 0

    def set_status(self, status: str):
        if status == 'Download Libraries':
            status = status.replace('Download Libraries', f'{language_loader.lang_['download_libraries']}')
        elif status == 'Download Assets':
            status = status.replace('Download Assets', f'{language_loader.lang_['download_assets']}')
        elif status == 'Download modules':
            status = status.replace('Download modules', f'{language_loader.lang_['download_modules']}')
        elif status == 'Running fabric installer':
            status = status.replace('Running fabric installer', f'{language_loader.lang_['running_fabric_installer']}')
        elif status == 'Running quilt installer':
            status = status.replace('Running quilt installer', f'{language_loader.lang_['running_quilt_installer']}')
        elif 'Download' in status:
            status = status.replace('Download', f'{language_loader.lang_['download']}')
        elif status == 'Install java runtime':
            status = status.replace('Install java runtime', f'{language_loader.lang_['installing_java_runtime']}')
        elif status == 'Installation complete':
            status = status.replace('Installation complete', f'{language_loader.lang_['installation_completed']}')
        self.update_label.configure(text=f'{status}')

    def set_progress(self, progress: int):
        percent_progress = progress / current_max
        if current_max != 0:
            self.percent_label.configure(text=f'{int(percent_progress * 100)}%')
        self.update_progress_bar.set(percent_progress)

    def set_max(self, new_max: int):
        global current_max
        current_max = new_max

    def change_appearance_mode_event(self, new_appearance_mode):
        if self.theme_list_menu.get() == f'{language_loader.lang_['light']}':
            ctk.set_appearance_mode('light')
            language_loader.data['appearance_mode'] = 'light'
        elif self.theme_list_menu.get() == f'{language_loader.lang_['dark']}':
            ctk.set_appearance_mode('dark')
            language_loader.data['appearance_mode'] = 'dark'
        elif self.theme_list_menu.get() == f'{language_loader.lang_['system']}':
            ctk.set_appearance_mode('system')
            language_loader.data['appearance_mode'] = 'system'

        if self.theme_list_menu.get() != self.current_theme:
            self.save_changes_button.configure(state='normal')
        else:
            self.save_changes_button.configure(state='disabled')

        with open('launch_options.json', 'w') as f:
            json.dump(language_loader.data, f, ensure_ascii=False, indent=4)

    def change_language_event(self, language):
        if self.language_list_menu.get() == f'{language_loader.lang_['ru']} (Русский)':
            language_loader.data['language'] = 'ru'
        elif self.language_list_menu.get() == f'{language_loader.lang_['en']} (English)':
            language_loader.data['language'] = 'en'
        elif self.language_list_menu.get() == f'{language_loader.lang_['zh']} (中文)':
            language_loader.data['language'] = 'zh'

        if self.current_language != self.language_list_menu.get():
            self.save_changes_button.configure(state='normal')
        else:
            self.save_changes_button.configure(state='disabled')

        with open('launch_options.json', 'w') as f:
            json.dump(language_loader.data, f, ensure_ascii=False, indent=4)

    def select_frame_by_name(self, name):
        if name == 'home':
            self.home_frame.grid(row=0, column=1, sticky='nsew')
            self.home_frame_button_1.configure(fg_color=('#3B8ED0', '#1F6AA5'), hover_color=('#36719F', '#144870'))
        else:
            self.home_frame.grid_forget()
            self.home_frame_button_1.configure(fg_color='transparent', hover_color=('gray70', 'gray30'))
        if name == 'frame_2':
            self.second_frame.grid(row=0, column=1, sticky='nsew')
            self.home_frame_button_2.configure(fg_color=('#3B8ED0', '#1F6AA5'), hover_color=('#36719F', '#144870'))
        else:
            self.second_frame.grid_forget()
            self.home_frame_button_2.configure(fg_color='transparent', hover_color=('gray70', 'gray30'))
        if name == 'frame_3':
            self.third_frame.grid(row=0, column=1, sticky='nsew')
            self.home_frame_button_3.configure(fg_color=('#3B8ED0', '#1F6AA5'), hover_color=('#36719F', '#144870'))
        else:
            self.third_frame.grid_forget()
            self.home_frame_button_3.configure(fg_color='transparent', hover_color=('gray70', 'gray30'))
        if name == 'frame_4':
            self.fourth_frame.grid(row=0, column=1, sticky='nsew')
            self.home_frame_button_4.configure(fg_color=('#3B8ED0', '#1F6AA5'), hover_color=('#36719F', '#144870'))
        else:
            self.fourth_frame.grid_forget()
            self.home_frame_button_4.configure(fg_color='transparent', hover_color=('gray70', 'gray30'))

    def home_button_event(self):
        self.select_frame_by_name('home')

    def frame_2_button_event(self):
        self.select_frame_by_name('frame_2')

    def frame_3_button_event(self):
        self.select_frame_by_name('frame_3')

    def frame_4_button_event(self):
        self.select_frame_by_name('frame_4')

    def play_button_event(self):
        t1 = Thread(target=self.thread_1)
        t1.start()

    def thread_1(self):
        def return_configure():
            self.play_button.configure(state='normal')
            self.version_menu.configure(state='normal')

        if self.version_menu.get() != f'{language_loader.lang_['no_versions']}':
            try:
                self.play_button.configure(state='disabled')
                self.version_menu.configure(state='disabled')
                self.options['resolutionWidth'] = self.width_entry.get()
                self.options['resolutionHeight'] = self.height_entry.get()
                if self.change_launch_options_segmented_button.get() == f'{language_loader.lang_['simple']}':
                    self.options['jvmArguments'] = [f'-Xms{self.min_ram}G', f'-Xmx{self.max_ram}G']
                elif self.change_launch_options_segmented_button.get() == f'{language_loader.lang_['advanced']}':
                    self.options['jvmArguments'] = self.jvm_args_entry.get().split(' ')
                subprocess.call(mll.command.get_minecraft_command(version=self.version_menu.get(),
                                                                  minecraft_directory=minecraft_directory,
                                                                  options=self.options))
            except mll.exceptions.VersionNotFound:
                messagebox.showerror('Minecraft Launcher', f'{language_loader.lang_['version_not_found']}')
            except Exception as e:
                messagebox.showerror('Minecraft Launcher', f'{language_loader.lang_['unknown_error']}\n{e}')
            finally:
                return_configure()
        else:
            messagebox.showinfo('Minecraft Launcher', f'{language_loader.lang_['cant_enter_the_game']}')

    def install_button_event(self):
        t2 = Thread(target=self.thread_2)
        t2.start()

    def thread_2(self):
        def return_configure():
            self.install_button.configure(state='normal')
            self.version_install_menu.configure(state='normal')
            self.version_type_choice_segmented_button.configure(state='normal')
            self.advanced_options.configure(state='normal')
            self.snapshots.configure(state='normal')
            self.old_beta.configure(state='normal')
            self.old_alpha.configure(state='normal')
            self.home_frame_button_5.configure(state='normal')

        self.install_button.configure(state='disabled')
        self.version_install_menu.configure(state='disabled')
        self.version_type_choice_segmented_button.configure(state='disabled')
        self.advanced_options.configure(state='disabled')
        self.snapshots.configure(state='disabled')
        self.old_beta.configure(state='disabled')
        self.old_alpha.configure(state='disabled')
        self.home_frame_button_5.configure(state='disabled')
        if self.show_flag == 0:
            self.show_flag = 1
        self.advanced_option_button_event()
        self.update_progress_bar.grid(row=4, column=0, columnspan=2)
        try:
            if self.version_type_choice_segmented_button.get() == 'Vanilla':
                mll.install.install_minecraft_version(versionid=self.version_install_menu.get(),
                                                      minecraft_directory=minecraft_directory, callback=self.callback)
            elif self.version_type_choice_segmented_button.get() == 'Forge':
                messagebox.showinfo('Minecraft Launcher', f'{language_loader.lang_['under_development']}')
            elif self.version_type_choice_segmented_button.get() == 'Fabric':
                mll.fabric.install_fabric(minecraft_version=self.version_install_menu.get(),
                                          minecraft_directory=minecraft_directory,
                                          loader_version=self.loader_versions_menu.get(),
                                          callback=self.callback)
            elif self.version_type_choice_segmented_button.get() == 'Quilt':
                mll.quilt.install_quilt(minecraft_version=self.version_install_menu.get(),
                                        minecraft_directory=minecraft_directory,
                                        loader_version=self.loader_versions_menu.get(),
                                        callback=self.callback)
        except requests.exceptions.ConnectionError:
            messagebox.showerror('Minecraft Launcher',
                                 f'{language_loader.lang_['connection_error']}')
        finally:
            self.installed_versions = mll.utils.get_installed_versions(minecraft_directory=minecraft_directory)
            self.available_versions = []
            for version in self.installed_versions:
                self.available_versions.append(version['id'])
            self.available_versions = self.available_versions[::-1]
            self.version_menu.configure(values=self.available_versions)
            self.version_list_menu.configure(values=self.available_versions)
            if self.available_versions != []:
                self.version_menu.set(self.available_versions[0])
                self.version_list_menu.set(self.available_versions[0])
            return_configure()
        self.update_progress_bar.grid_forget()
        self.update_label.grid_forget()
        self.percent_label.configure(text='')
        sleep(2)
        self.update_label.grid(row=3, column=0, columnspan=2)
        self.update_label.configure(text='')

    def on_selection(self, value):
        if value in self.version_list_menu.cget('values'):
            self.install_button.configure(text=f'{language_loader.lang_['reinstall']}')
        else:
            self.install_button.configure(text=f'{language_loader.lang_['install']}')

        if self.version_type_choice_segmented_button.get() == 'Forge':
            loader_versions = []
            chosen_version = self.version_install_menu.get()
            for version in self.forge_version_list:
                if version == chosen_version:
                    for forge_version in mll.forge.list_forge_versions():
                        if forge_version[:len(chosen_version) + 1] == chosen_version + '-':
                            loader_versions.append(forge_version)
            self.loader_versions_menu.configure(values=loader_versions)
            self.loader_versions_menu.set(loader_versions[0])

    def change_version_list_type(self, value):
        vanilla_versions = self.vanilla_version_list
        if self.version_type_choice_segmented_button.get() == 'Vanilla':
            self.vanilla_version_list = []
            for version in mll.utils.get_version_list():
                if version['type'] == 'release':
                    self.vanilla_version_list.append(version['id'])
                elif version['type'] == 'snapshot' and self.snapshots_var.get() == 'on':
                    self.vanilla_version_list.append(version['id'])
                elif version['type'] == 'old_beta' and self.old_beta_var.get() == 'on':
                    self.vanilla_version_list.append(version['id'])
                elif version['type'] == 'old_alpha' and self.old_alpha_var.get() == 'on':
                    self.vanilla_version_list.append(version['id'])
            self.version_install_menu.configure(values=self.vanilla_version_list)
            self.version_install_menu.set(self.vanilla_version_list[0])
        elif self.version_type_choice_segmented_button.get() == 'Forge':
            self.vanilla_version_list = []
            for version in self.forge_version_list:
                self.vanilla_version_list.append(version)
            self.version_install_menu.configure(values=self.vanilla_version_list)
            self.version_install_menu.set(self.vanilla_version_list[0])

            loader_versions = []
            chosen_version = self.version_install_menu.get()
            for version in self.forge_version_list:
                if version == chosen_version:
                    for forge_version in mll.forge.list_forge_versions():
                        if forge_version[:len(chosen_version) + 1] == chosen_version + '-':
                            loader_versions.append(forge_version)
            self.loader_versions_menu.configure(values=loader_versions)
            self.loader_versions_menu.set(loader_versions[0])
        elif self.version_type_choice_segmented_button.get() == 'Fabric':
            self.vanilla_version_list = []
            for version in mll.utils.get_version_list():
                if version['id'] in self.fabric_version_list:
                    if version['type'] == 'release':
                        self.vanilla_version_list.append(version['id'])
                    elif version['type'] == 'snapshot' and self.snapshots_var.get() == 'on':
                        self.vanilla_version_list.append(version['id'])
            self.version_install_menu.configure(values=self.vanilla_version_list)
            self.version_install_menu.set(self.vanilla_version_list[0])
            self.loader_versions_menu.configure(values=self.fabric_loader_versions)
            self.loader_versions_menu.set(self.fabric_loader_versions[0])
        elif self.version_type_choice_segmented_button.get() == 'Quilt':
            self.vanilla_version_list = []
            for version in mll.utils.get_version_list():
                if version['id'] in self.quilt_version_list:
                    if version['type'] == 'release':
                        self.vanilla_version_list.append(version['id'])
                    elif version['type'] == 'snapshot' and self.snapshots_var.get() == 'on':
                        self.vanilla_version_list.append(version['id'])
            self.version_install_menu.configure(values=self.vanilla_version_list)
            self.version_install_menu.set(self.vanilla_version_list[0])
            self.loader_versions_menu.configure(values=self.quilt_loader_versions)
            self.loader_versions_menu.set(self.quilt_loader_versions[0])

        if self.version_type_choice_segmented_button.get() != 'Vanilla':
            if self.show_flag == 1:
                self.loader_versions_label.grid(row=2, column=0, sticky='w', pady=(10, 0))
                self.loader_versions_menu.grid(row=2, column=1, sticky='e', pady=(10, 0))
            if self.version_type_choice_segmented_button.get() == 'Forge':
                self.snapshots.configure(state='disabled')
            elif self.version_type_choice_segmented_button.get() != 'Forge':
                self.snapshots.configure(state='normal')
            self.old_beta.configure(state='disabled')
            self.old_alpha.configure(state='disabled')
        else:
            self.loader_versions_label.grid_forget()
            self.loader_versions_menu.grid_forget()
            self.snapshots.configure(state='normal')
            self.old_beta.configure(state='normal')
            self.old_alpha.configure(state='normal')

        if self.version_install_menu.get() in self.version_list_menu.cget('values'):
            self.install_button.configure(text=f'{language_loader.lang_['reinstall']}')
        else:
            self.install_button.configure(text=f'{language_loader.lang_['install']}')

    def advanced_option_button_event(self):
        if self.show_flag == 0:
            self.advanced_options.configure(image=self.up_arrow)
            self.load_versions_label.grid(row=1, column=0, sticky='w')
            self.types_frame.grid(row=1, column=1, sticky='e')
            if self.version_type_choice_segmented_button.get() != 'Vanilla':
                self.loader_versions_label.grid(row=2, column=0, sticky='w', pady=(10, 0))
                self.loader_versions_menu.grid(row=2, column=1, sticky='e', pady=(10, 0))
            self.show_flag = 1
        elif self.show_flag == 1:
            self.advanced_options.configure(image=self.down_arrow)
            self.load_versions_label.grid_forget()
            self.types_frame.grid_forget()
            self.loader_versions_label.grid_forget()
            self.loader_versions_menu.grid_forget()
            self.show_flag = 0

    def version_type_button_event(self):
        self.vanilla_version_list = []
        for version in mll.utils.get_version_list():
            if self.version_type_choice_segmented_button.get() == 'Vanilla':
                if version['type'] == 'release':
                    self.vanilla_version_list.append(version['id'])
                elif version['type'] == 'snapshot' and self.snapshots_var.get() == 'on':
                    self.vanilla_version_list.append(version['id'])
                elif version['type'] == 'old_beta' and self.old_beta_var.get() == 'on':
                    self.vanilla_version_list.append(version['id'])
                elif version['type'] == 'old_alpha' and self.old_alpha_var.get() == 'on':
                    self.vanilla_version_list.append(version['id'])
            elif self.version_type_choice_segmented_button.get() == 'Fabric':
                if version['id'] in self.fabric_version_list:
                    if version['type'] == 'release':
                        self.vanilla_version_list.append(version['id'])
                    elif version['type'] == 'snapshot' and self.snapshots_var.get() == 'on':
                        self.vanilla_version_list.append(version['id'])
            elif self.version_type_choice_segmented_button.get() == 'Quilt':
                if version['id'] in self.quilt_version_list:
                    if version['type'] == 'release':
                        self.vanilla_version_list.append(version['id'])
                    elif version['type'] == 'snapshot' and self.snapshots_var.get() == 'on':
                        self.vanilla_version_list.append(version['id'])
        self.version_install_menu.configure(values=self.vanilla_version_list)
        self.version_install_menu.set(self.vanilla_version_list[0])

        if self.version_install_menu.get() in self.available_versions:
            self.install_button.configure(text=f'{language_loader.lang_['reinstall']}')
        else:
            self.install_button.configure(text=f'{language_loader.lang_['install']}')

        if self.snapshots_var.get() == 'off':
            language_loader.data['include_snapshots'] = 'false'
        elif self.snapshots_var.get() == 'on':
            language_loader.data['include_snapshots'] = 'true'
        if self.old_beta_var.get() == 'off':
            language_loader.data['include_beta'] = 'false'
        elif self.old_beta_var.get() == 'on':
            language_loader.data['include_beta'] = 'true'
        if self.old_alpha_var.get() == 'off':
            language_loader.data['include_alpha'] = 'false'
        elif self.old_alpha_var.get() == 'on':
            language_loader.data['include_alpha'] = 'true'

        with open('launch_options.json', 'w') as f:
            json.dump(language_loader.data, f, ensure_ascii=False, indent=4)

    def switch_resolution_widgets(self):
        if self.enable_custom_resolution_var.get() == 'on':
            self.width_entry.configure(state='normal')
            self.height_entry.configure(state='normal')
            self.options['customResolution'] = True
            language_loader.data['enable_custom_resolution'] = 'true'
        else:
            self.width_entry.configure(state='disabled')
            self.height_entry.configure(state='disabled')
            self.options['customResolution'] = False
            language_loader.data['enable_custom_resolution'] = 'false'

        if self.enable_custom_resolution != self.enable_custom_resolution_var.get():
            self.save_changes_button.configure(state='normal')
        else:
            self.save_changes_button.configure(state='disabled')

        with open('launch_options.json', 'w') as f:
            json.dump(language_loader.data, f, ensure_ascii=False, indent=4)

    def change_ram(self, value):
        self.options['jvmArguments'] = []
        min_ram = int(self.ram_slider.get()) // 2
        max_ram = int(self.ram_slider.get())
        if max_ram == 1:
            min_ram = 1
        self.ram_entry.configure(state='normal')
        self.ram_entry.delete(0, last_index=len(self.ram_entry.get()))
        self.ram_entry.insert(0, str(int(value)) + ' GB')
        self.ram_entry.configure(state='disabled')
        self.options['jvmArguments'] = [f'-Xms{min_ram}G', f'-Xmx{max_ram}G']

        if self.current_ram != self.ram_slider.get():
            self.save_changes_button.configure(state='normal')
        else:
            self.save_changes_button.configure(state='disabled')

    def change_launch_options(self, value):
        if value == f'{language_loader.lang_['simple']}':
            self.ram_slider.grid(row=2, column=0, sticky='we', padx=(0, 20))
            self.ram_entry.grid(row=2, column=1, sticky='e')
            self.jvm_args_label.grid_forget()
            self.jvm_args_entry.grid_forget()
            self.change_ram(value=self.ram_slider.get())
        elif value == f'{language_loader.lang_['advanced']}':
            self.jvm_args_label.grid(row=2, column=0, sticky='w', padx=(0, 10))
            self.jvm_args_entry.grid(row=2, column=1, sticky='we')
            self.ram_slider.grid_forget()
            self.ram_entry.grid_forget()
            self.options['jvmArguments'] = self.jvm_args_entry.get().split(' ')

        if self.edit_launch_options_mode != value:
            self.save_changes_button.configure(state='normal')

    def open_minecraft_directory(self):
        path = minecraft_directory
        path = os.path.relpath(path)
        os.startfile(path)

    def save_changes(self):
        language_loader.data['width'] = self.width_entry.get()
        language_loader.data['height'] = self.height_entry.get()
        if self.change_launch_options_segmented_button.get() == f'{language_loader.lang_['simple']}':
            language_loader.data['choose_edit_mode'] = 'simple'
            self.change_ram(value=self.ram_slider.get())
        elif self.change_launch_options_segmented_button.get() == f'{language_loader.lang_['advanced']}':
            language_loader.data['choose_edit_mode'] = 'advanced'
            self.options['jvmArguments'] = self.jvm_args_entry.get().split(' ')
        language_loader.data['ram_count'] = int(self.ram_slider.get())
        language_loader.data['jvm_args'] = self.jvm_args_entry.get()

        self.current_language = self.language_list_menu.get()
        self.current_theme = self.theme_list_menu.get()
        self.enable_custom_resolution = self.enable_custom_resolution_var.get()
        self.current_ram = self.ram_slider.get()

        with open('launch_options.json', 'w') as f:
            json.dump(language_loader.data, f, ensure_ascii=False, indent=4)

    def logout(self):
        self.navigation_frame.grid_forget()
        self.home_frame.grid_forget()
        self.second_frame.grid_forget()
        self.third_frame.grid_forget()
        self.fourth_frame.grid_forget()
        self.login_frame.grid(row=0, column=0, rowspan=2, columnspan=2, padx=320, pady=(150, 180), sticky='nsew')
        self.enter_username_entry.delete(0, len(self.enter_username_entry.get()))
        self.enter_username_entry.insert(0, self.username)

    def change_username(self):
        def validate_username(text):
            valid_chars = set(ascii_letters + punctuation + digits)
            for char in text:
                if char not in valid_chars:
                    return False
                    break

        self.username = str(self.enter_username_entry.get())
        if len(self.username) > 16:
            self.account_label.configure(text=f'  {self.username[:12]}...', font=ctk.CTkFont(size=16))
        elif len(self.username) > 13:
            self.account_label.configure(text=f'  {self.username}', font=ctk.CTkFont(size=16))
        elif len(self.username) > 10 and self.username.lower()[:10] == 'wwwwwwwwww':
            self.account_label.configure(text=f'  {self.username}', font=ctk.CTkFont(size=16))
        else:
            self.account_label.configure(text=f'  {self.username}', font=ctk.CTkFont(size=20))

        if self.username.split() != []:
            if validate_username(self.username) == False:
                pass
            else:
                self.login_frame.grid_forget()
                self.navigation_frame.grid(row=0, column=0, sticky='ns')
                self.select_frame_by_name('home')

                language_loader.data['username'] = self.username
                with open('launch_options.json', 'w', encoding='UTF-8') as f:
                    json.dump(language_loader.data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    if mll.utils.is_platform_supported() == True:
        try:
            app = App()
            app.mainloop()
        except requests.exceptions.ConnectionError:
            messagebox.showerror('Minecraft Launcher', f'{language_loader.lang_['connection_error']}')
    elif mll.utils.is_platform_supported() == False:
        messagebox.showinfo('Minecraft Launcher', f'{language_loader.lang_['platform_not_supported']}')
