import customtkinter as ctk
from classifiers.neuralnet_2l_lin import train_nn_2l_lin, dm_nn_2l_lin, predictor_nn_2l_lin
from classifiers.neuralnet_4l_relu_lin import train_nn_4l_relu_lin, dm_nn_4l_relu_lin, predictor_nn_4l_relu_lin
from classifiers.modifiers.data.augment import aug
from tkinter.filedialog import askopenfilename
from classifiers.modifiers.preprocessing import pp
from classifiers.modifiers.preprocessing import color
import torch
import os
import platform
from PIL import Image
import ctypes

if __name__ == '__main__':
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    dev = f'Device: {device.upper()}'
    print(dev)
    
    # adjust scaling due to issues at 150+%
    scaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    if scaleFactor == 1.25:
        ctk.set_window_scaling(0.95)
        ctk.set_widget_scaling(0.95)
    if scaleFactor == 1.5:
        ctk.set_window_scaling(0.75)
        ctk.set_widget_scaling(0.75)
    if scaleFactor == 1.75:
        ctk.set_window_scaling(0.55)
        ctk.set_widget_scaling(0.55)
    if scaleFactor == 2.0:
        ctk.set_window_scaling(0.35)
        ctk.set_widget_scaling(0.35)


    # running all models
    def predictor_all(input, stats_nn_1, stats_nn_2):
        if stats_nn_1 == 0:
            print(color.BOLD,color.RED,"\nPlease choose a model to use!",color.END)
            err = "\nPlease choose a model to use!\n"
            output.insert("1.0", err)
        if stats_nn_1 == 1:
            out = predictor_nn_2l_lin(input)
            output.insert("1.0", "".join(out))
        if stats_nn_2 == 0:
            print(color.BOLD,color.RED,"\nPlease choose a model to use!",color.END)
            err = "\nPlease choose a model to use!\n"
            output.insert("1.0", err)
        if stats_nn_2 == 1:
            out = predictor_nn_4l_relu_lin(input)
            output.insert("1.0", "".join(out))
            
    # training all models
    def train_all(stats_nn_1, stats_nn_2):
        if stats_nn_1 == 0 and stats_nn_2 == 0:
            print(color.BOLD,color.RED,"\nPlease choose a model to use!",color.END)
            err = "\nPlease choose a model to use!\n"
            output.insert("1.0", err)
        if stats_nn_1 == 1:
            train_nn_2l_lin()
            print(color.BLUE,color.BOLD,'NeuralNet_2l_lin trained.\n',color.END)
            info = '\nNeuralNet_2l_lin trained.\n\n'
            output.insert("1.0", info)
        if stats_nn_2 == 1:
            train_nn_4l_relu_lin()
            print(color.BLUE,color.BOLD,'NeuralNet_4l_relu_lin trained.\n',color.END)
            info = '\nNeuralNet_4l_relu_lin trained.\n\n'
            output.insert("1.0", info)
        
        
    # running all demo models
    def dm_predict_all():
        out = dm_nn_2l_lin()
        output.insert("1.0", "\n".join(out))
        print()
        out = dm_nn_4l_relu_lin()
        output.insert("1.0", "\n".join(out))
        

    # open the window to select file
    def openfilePP():
        try:
            file = askopenfilename(title='Select Training File', filetypes=[('Training File', '*.csv')], initialdir='./classifiers/modifiers/data/')
            out = pp(file)
            output.insert("1.0", "\n".join(out))
            # filename = os.path.basename(file)
            # # label for selected file
            # selectedTrainFile = tk.Label(root, text=filename, bg="white", font=("Calibri", 10), relief="ridge")
            # selectedTrainFile.place(width=220, height=40, x=350, y=331)
        except FileNotFoundError:
            print()
        
    def openfileAugment(size):
        try:
            file = askopenfilename(title='Select Training File', filetypes=[('Training File', '*.csv')], initialdir='./classifiers/modifiers/data/')
            filename = os.path.basename(file)
            selectedfile = './classifiers/modifiers/data/'+filename
            # selectedTrainFileLabel = tk.Label(root, text=filename, bg="white", font=("Calibri", 10), relief="ridge")
            # selectedTrainFileLabel.place(width=220, height=40, x=20, y=331)
            out = aug(int(size), selectedfile)
            output.insert("1.0", "\n".join(out))
        except ValueError:
            print(color.BOLD,color.RED,'\nPlease enter an integer (size) first, then select the desired file!',color.END)
            err = 'Please enter an integer (size) first, then select the desired file!\n'
            output.insert("1.0", err)

        
    # clear function for the shell / cmdlet
    def clear():
        if platform.system() == "Windows":
            os.system("CLS")
        elif platform.system() == "Linux":
            os.system("clear")
        output.delete("1.0", ctk.END)


    # initiating the  ctk module
    root = ctk.CTk()
    root.geometry("1600x800")
    root.title("slangID3 DL")
    root.grid_columnconfigure((0), weight=1)
    root.grid_columnconfigure((1), weight=1)

    root.grid_rowconfigure((0), weight=1)
    root.grid_rowconfigure((1), weight=1)
    root.grid_rowconfigure((2), weight=1)
    root.grid_rowconfigure((3), weight=1)
    root.grid_rowconfigure((4), weight=1)


    checkbox_frame = ctk.CTkFrame(root, width=771,fg_color="transparent", border_color="#e4e4e4", border_width=2)
    checkbox_frame.grid(row=2, rowspan=2, column=0, columnspan=2, padx=325, pady=(10, 10), sticky="nsw")

    # output window
    output = ctk.CTkTextbox(root, font=("Calibri", 20), width=860, fg_color="#3d3d3d", border_width=8, border_color="#c8c8c8", text_color="#e4e4e4", scrollbar_button_color="#e4e4e4")
    output.grid(row=0, column=1, rowspan=5, padx=15, pady=(10, 10), sticky="nwse")

    # field for text input
    phrase_entry = ctk.CTkTextbox(root, font=("Calibri", 20), width=580, height=50, fg_color="#3d3d3d", border_width=8, border_color="#f76700", text_color="#e4e4e4", scrollbar_button_color="#e4e4e4")
    phrase_entry.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 0), sticky="nsw")

    # field for augmentation size input
    aug_entry = ctk.CTkEntry(root, font=("Calibri", 20), width=80, height=80, fg_color="#3d3d3d", border_width=2, border_color="#e4e4e4", text_color="#e4e4e4", placeholder_text="size", placeholder_text_color="#e4e4e4")
    aug_entry.grid(row=2, column=0, padx=160, pady=(0, 0), sticky="w")

    icon = Image.open("./misc/gallery/slangID3_dl_icon.png")
    img = ctk.CTkImage(dark_image=icon, light_image=icon, size=(60,60))
    img_label = ctk.CTkLabel(root, image=img, text="")
    img_label.grid(row=4, column=0, padx=15, pady=(0, 10), sticky="sw")

    device_label = ctk.CTkLabel(root, text=dev, fg_color="transparent", text_color="white", font=("Calibri", 20))
    device_label.grid(row=4, column=0, padx=170, pady=(0, 5), sticky="sw")
    
    # version number
    version = ctk.CTkLabel(root, text="1.0", fg_color="transparent", text_color="white", font=("Calibri", 20))
    version.grid(row=4, column=0, padx=80, pady=(0, 5), sticky="sw")


    # Buttons and checkboxes
    ################################################################################################################################
    predict_button = ctk.CTkButton(root, command=lambda: predictor_all([phrase_entry.get("1.0",ctk.END)],nn_checkbox_1.get(), nn_checkbox_2.get()), text="Predict", font=("Calibri", 22,"bold"), text_color="white", fg_color="#f76700", hover_color="#eeb000", border_width=2, border_color="#e4e4e4", border_spacing=10)
    predict_button.grid(row=1, rowspan=1, column=0, padx=15, pady=10, sticky="nsw")

    train_button = ctk.CTkButton(root, command=lambda: [train_all(nn_checkbox_1.get(), nn_checkbox_2.get())], text="Train", font=("Calibri", 22,"bold"), text_color="white", fg_color="#f76700", hover_color="#eeb000", border_width=2, border_color="#e4e4e4", border_spacing=10)
    train_button.grid(row=1, rowspan=1, column=0, padx=170, pady=10, sticky="nsw")

    augment_button = ctk.CTkButton(root, command=lambda: openfileAugment(aug_entry.get()), text="Augment\nData", font=("Calibri", 20,"bold"), text_color="white", fg_color="#f76700", hover_color="#eeb000", border_width=2, border_spacing=10, border_color="#e4e4e4")
    augment_button.grid(row=2, column=0, rowspan=1, columnspan=2, padx=15, pady=10, sticky="nsw")

    preprocess_button = ctk.CTkButton(root, command=lambda: openfilePP(), text="Preprocess\nData", font=("Calibri", 20,"bold"), text_color="white", fg_color="#f76700", hover_color="#eeb000", border_width=2, border_spacing=10, border_color="#e4e4e4")
    preprocess_button.grid(row=3, column=0, rowspan=1, columnspan=2, padx=15, pady=10, sticky="nsw")

    demo_button = ctk.CTkButton(root, command=lambda: dm_predict_all(), text="DEMO", font=("Calibri", 20,"bold"), text_color="white", fg_color="#f76700", hover_color="#eeb000", border_width=2, border_spacing=10, border_color="#e4e4e4")
    demo_button.grid(row=3, column=0, rowspan=1, columnspan=2, padx=170, pady=10, sticky="nsw")

    clear_button = ctk.CTkButton(root, command=lambda: clear(), text="Clear Output", font=("Calibri", 20,"bold"), text_color="white", fg_color="#bf0606", hover_color="#930b0b", border_width=2, border_spacing=10, border_color="#e4e4e4")
    clear_button.grid(row=1, column=0, rowspan=1, columnspan=2, padx=325, pady=10, sticky="nsw")


    nn_checkbox_1 = ctk.CTkCheckBox(checkbox_frame, command=lambda: nn_checkbox_1.get(), text="NeuralNet (2 linear layers)", font=("Calibri", 20,"bold"), text_color="white", corner_radius=10, fg_color="#f76700", hover_color="#FFA300", border_color="white")
    nn_checkbox_1.grid(row=1, column=0, padx=10, pady=(10,0), sticky="nsw")

    nn_checkbox_2 = ctk.CTkCheckBox(checkbox_frame, command=lambda: nn_checkbox_1.get(), text="NeuralNet (4 linear layers \nand 3 ReLU layers)", font=("Calibri", 20,"bold"), text_color="white", corner_radius=10, fg_color="#f76700", hover_color="#FFA300", border_color="white")
    nn_checkbox_2.grid(row=2, column=0, padx=10, pady=(10,0), sticky="nsw")
    
    select_all_checkbox = ctk.CTkCheckBox(checkbox_frame, command=lambda: (nn_checkbox_1.toggle(), nn_checkbox_2.toggle()), text="All models", font=("Calibri", 20,"bold"), text_color="white", border_color="red", corner_radius=10, fg_color="#b6c2fe", hover_color="#99c8fc")
    select_all_checkbox.grid(row=6, column=0, padx=10, pady=(15,10), sticky="nsw")
    ################################################################################################################################

    root.mainloop()

