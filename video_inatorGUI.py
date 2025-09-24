import subprocess
import os
import tkinter as tk
from tkinter import filedialog, messagebox

ffmpeg_path = os.path.join("ffmpeg", "ffmpeg.exe") ##ffmpeg path wants to be up here bc it just does

if not os.path.isfile(ffmpeg_path):
    messagebox.showinfo("notice", "you have not installed ffmpeg yet - the program will not be able to do anything. install ffmpeg first!")

def start():
    inputFile = file_path.get()
    mode = mode_var.get()

    if not inputFile:
        messagebox.showerror("error", "please select a file.")
        return

    command1 = [
        ffmpeg_path,
        "-i", inputFile,
        "-y",
        "-vf", "scale=320:240,eq=brightness=" + str(2 * intensity.get()) + ":saturation=" + str(5 * intensity.get()) + ":contrast=" + str(10 * intensity.get()) + ",noise=alls=100:allf=t+u,fps=" + str(24 / intensity.get()),
        "-r", "30",
        "-g", "60",
        "-bf", "2",
        "-b:v", "100k",
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",
        "-af", "bass=g=" + str(40 * intensity.get()) + ":f=" + str(35 * intensity.get()) + ",volume=" + str(10 * intensity.get()) + ",aresample=8000,asetnsamples=32",
        "-c:a", "aac",
        "-b:a", "64k",
        "-loglevel", "quiet",
        "output.mp4"
    ]


    command2 = [
        ffmpeg_path,
        "-i", inputFile,
        "-y",
        "-af", "bass=g=" + str(40 * intensity.get()) + ":f=" + str(35 * intensity.get()) + ",volume=" + str(10 * intensity.get()) + ",aresample=8000,asetnsamples=32",
        "-loglevel", "quiet",
        "output.mp3"
    ]

    command3 = [
        ffmpeg_path,
        "-i", inputFile,
        "-y",
        "-vf", "scale=320:240,eq=brightness=" + str(2 * intensity.get()) + ":saturation=" + str(5 * intensity.get()) + ":contrast=" + str(10 * intensity.get()) + ",noise=alls=100:allf=t+u,setpts=N/(FRAME_RATE*TB)",
        "-loglevel", "quiet",
        "output.png"
    ]

    popup = tk.Toplevel()
    popup.title("it's busy")
    popup.geometry("340x180")
    popup.resizable(False, False)
    
    img_path = os.path.join("data", "logo.png")
    img = tk.PhotoImage(file=img_path)
    img_label = tk.Label(popup, image=img)
    img_label.image = img
    img_label.pack(pady=5)

    # text
    txt_label = tk.Label(popup, text="murdering...", font=("Courier", 14))
    txt_label.pack()

    popup.update()

    if os.path.isfile(ffmpeg_path):
        try:
            if mode == "1":
                subprocess.run(command1, check=True)
            elif mode == "2":
                subprocess.run(command2, check=True)
            elif mode == "3":
                subprocess.run(command3, check=True)
            else:
                messagebox.showerror("Error", "invalid mode selected.")
            return
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"destruction failed:\n{e}")
        finally:
            popup.destroy()
            messagebox.showinfo("done", "your file has been annihilated!")
    else:
        popup.destroy()
        messagebox.showinfo("notice", "ffmpeg won't just magically appear! follow the instructions in HOW 2 FFMPEG.txt")

def browse_file():
    path = filedialog.askopenfilename()
    file_path.set(path)

# time to gui yay
root = tk.Tk()
root.title("video-inator GUI")
root.iconbitmap(os.path.join("data", "icon.ico"))

##other vars want to be down here because they just do
file_path = tk.StringVar()
mode_var = tk.StringVar(value="1")
intensity = tk.IntVar(value="1")

logo_path = os.path.join("data", "logo.png")
logo_img = tk.PhotoImage(file=logo_path)
logo_label = tk.Label(root, image=logo_img)
logo_label.pack(pady=10)

tk.Label(root, text="select input file:").pack(pady=5)
tk.Entry(root, textvariable=file_path, width=35).pack()
tk.Button(root, text="browse", command=browse_file).pack(pady=5)

tk.Label(root, text="choose destruction mode:").pack(pady=5)
tk.Radiobutton(root, text="1 - video & audio (mp4)", variable=mode_var, value="1").pack()
tk.Radiobutton(root, text="2 - audio only (mp3)", variable=mode_var, value="2").pack()
tk.Radiobutton(root, text="3 - images (png)", variable=mode_var, value="3").pack(pady=(0,10))

tk.Label(root, text="choose intensity:").pack()
tk.Scale(root, from_=1, to=3, orient=tk.HORIZONTAL, variable=intensity).pack()

tk.Button(root, text="DESTROY!!!!", command=start, bg="red", fg="white").pack(pady=20)

root.mainloop()