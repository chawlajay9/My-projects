"""YOUTUBE DOWNLOADER.

Demo URL:
https://www.youtube.com/watch?v=jxmzY9soFXg
https://www.youtube.com/watch?v=LCVOoY3_vGA
"""

# modules
import io
import os
import re
import requests
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube
from PIL import Image, ImageTk


FONT = "times new roman"

URL_PATTERN = r'(https?://)?(www\.)?'
'(youtube|youtu|youtube-nocookie).(com|be)/'
'(watch?v=|embed/|v/|.+?v=)?([^&=%?]{11})'

logging.basicConfig(
    filename='youtube_downloader_log.log',
    filemode='a',
    level=logging.INFO
)


class YoutubeApp:
    """Youtube Class."""

    def __init__(self, root):
        """Define GUI."""
        logging.info("Started : YouTube Downloader GUI Intialized")
        self.root = root
        self.root.title("Youtube Downloader | Developed By Jay")
        self.root.geometry("500x420+300+50")
        self.root.resizable(False, False)
        self.root.config(bg='white')

        tk.Label(
            self.root,
            text='YouTube Downloader | Developed By Jay',
            font=(FONT, 15),
            bg="#262626",
            fg='white'
        ).pack(
            side='top',
            fill='x'
        )

        tk.Label(
            self.root,
            text='Video URL',
            font=(FONT, 15),
            bg="white"
        ).place(
            x=10,
            y=50
        )
        self.var_url = tk.StringVar()
        tk.Entry(
            self.root,
            font=(FONT, 13),
            textvariable=self.var_url,
            bg="white"
        ).place(
            x=120,
            y=50,
            width=350
        )

        tk.Label(
            self.root,
            text='File Type',
            font=(FONT, 15),
            bg="white"
        ).place(x=10, y=90)

        self.var_filetype = tk.StringVar()
        self.var_filetype.set('Video')

        tk.Radiobutton(
            self.root,
            text="Video",
            variable=self.var_filetype,
            value='Video',
            font=(FONT, 15),
            bg="white",
            activebackground='white'
        ).place(x=120, y=90)

        tk.Radiobutton(
            self.root,
            text="Audio",
            variable=self.var_filetype,
            value='Audio',
            font=(FONT, 15),
            bg="white",
            activebackground='white'
        ).place(x=220, y=90)

        tk.Button(
            self.root,
            text='Search',
            command=self.search,
            font=(FONT, 15),
            bg='sky blue').place(
                x=350,
                y=90,
                height=30,
                width=120
        )

        frame_ = tk.Frame(self.root, bd=2, relief='ridge', bg='lightyellow')
        frame_.place(
            x=10,
            y=130,
            width=480,
            height=180
        )

        self.video_title = tk.Label(
            frame_,
            text='Video Title Here',
            font=(FONT, 12),
            anchor='w',
            bg="lightgray"
        )

        self.video_title.place(x=0, y=0, relwidth=1)

        self.video_image = tk.Label(
            frame_,
            text='Video \n Image',
            font=(FONT, 15),
            bg="lightgray",
            bd=2,
            relief='ridge'
        )

        self.video_image.place(x=5, y=30, width=180, height=140)

        tk.Label(
            frame_,
            text='Description',
            font=(FONT, 15),
            bg="lightyellow",
        ).place(x=190, y=30)

        self.video_desc = tk.Text(
            frame_,
            font=(FONT, 10),
            bg="lightyellow",
        )

        self.video_desc.place(x=190, y=60, width=280, height=110)

        self.lbl_size = tk.Label(
            self.root,
            text='Total Size : MB',
            font=(FONT, 12),
            bg="white"
        )
        self.lbl_size.place(
            x=10,
            y=320
        )

        self.lbl_percentage = tk.Label(
            self.root,
            text='Downloading : 0%',
            font=(FONT, 12),
            bg="white"
        )
        self.lbl_percentage.place(
            x=160,
            y=320
        )

        tk.Button(
            self.root,
            text='Clear',
            command=self.clear,
            font=(FONT, 13),
            bg='black',
            fg='white'
        ).place(
            x=320,
            y=320,
            height=25,
            width=80
        )

        self.btn_download = tk.Button(
            self.root,
            text='Download',
            command=self.download,
            font=(FONT, 13),
            bg='red',
            fg='white',
        )
        self.btn_download.place(
            x=410,
            y=320,
            height=25,
            width=80
        )

        self.prog = ttk.Progressbar(
            self.root,
            orient='horizontal',
            length=590,
            mode='determinate'
        )

        self.prog.place(
            x=10,
            y=360,
            width=485,
            height=25
        )

        self.lbl_message = tk.Label(
            self.root,
            text='',
            font=(FONT, 12),
            bg='white'
        )

        self.lbl_message.place(
            x=0,
            y=380,
            relwidth=1
        )

        if os.path.exists("Audios") is False:
            os.mkdir('Audios')

        if os.path.exists("Videos") is False:
            os.mkdir('Videos')
        logging.info("Finished : YouTube Downloader GUI Intialized")

    def search(self):
        """Search URL and fetch data."""
        logging.info('Search Method Called.')
        try:
            if self.var_url.get() == '':
                self.lbl_message.config(text='Video URL is required', fg='red')
            elif not re.search(URL_PATTERN, self.var_url.get()):
                self.lbl_message.config(text='Video URL is Invalid.', fg='red')
            else:
                yt = YouTube(self.var_url.get())

                # Convert image url into image
                response = requests.get(yt.thumbnail_url)
                img_byte = io.BytesIO(response.content)
                self.img = Image.open(img_byte)
                self.img = self.img.resize((180, 140), Image.ANTIALIAS)
                self.img = ImageTk.PhotoImage(self.img)
                self.video_image.config(image=self.img)

                # Fetch the File type
                if self.var_filetype.get() == 'Video':
                    select_file = yt.streams.filter(progressive=True).first()

                if self.var_filetype.get() == 'Audio':
                    select_file = yt.streams.filter(only_audio=True).first()

                # Calculate Size
                self.size_inbytes = select_file.filesize
                max_size = self.size_inbytes/1024000
                self.mb = str(round(max_size, 2))+'MB'

                # update frame elements
                self.lbl_message.config(text="", fg='black')
                self.lbl_size.config(text='Total Size: '+self.mb)
                self.video_title.config(text=yt.title)
                self.video_desc.delete('1.0', tk.END)
                self.video_desc.insert(tk.END, yt.description)
                self.btn_download.config(state=tk.NORMAL)
        except Exception:
            logging.warning("Unexpected URL provided.")
            messagebox.showwarning("Warning", "Unexpected URL")

    def progress_(self, streams, chunk, bytes_remaining):
        """Display Progress of Downloading."""
        # Calculate Percentage
        percentage = (float(
            abs(bytes_remaining-self.size_inbytes)/self.size_inbytes)
        )*float(100)

        # Update Progressbar
        self.prog['value'] = percentage
        self.prog.update()
        self.lbl_percentage.config(text='Downloading : {} %'.format(
            str(round(percentage, 2))
        ))
        if round(percentage, 2) == 100:
            self.lbl_message.config(text="Download Completed", fg='green')
            self.btn_download.config(state=tk.DISABLED)
            logging.info("Download Completed for : {}".format(
                self.var_url.get()
            ))

    def download(self):
        """Download Audio or Video File."""
        logging.info("Download Method Called")
        if self.var_url.get() == '':
            self.lbl_message.config(text='Video URL is required', fg='red')
        else:
            yt = YouTube(
                self.var_url.get(),
                on_progress_callback=self.progress_
            )
            if self.var_filetype.get() == 'Video':
                select_file = yt.streams.filter(progressive=True).first()
                file_exists = select_file.default_filename
                if file_exists in os.listdir("Videos/"):
                    self.lbl_message.config(
                        text="Video File Already Exists",
                        fg='red'
                    )
                else:
                    self.lbl_message.config(text="", fg='black')
                    logging.info("Video : Download Started For {}".format(
                        self.var_url.get()
                    ))
                    select_file.download('Videos/')

            if self.var_filetype.get() == 'Audio':
                select_file = yt.streams.filter(only_audio=True).first()
                file_exists = select_file.default_filename
                if file_exists in os.listdir('Audios/'):
                    self.lbl_message.config(
                        text="Audio File Already Exists",
                        fg='red'
                    )
                else:
                    self.lbl_message.config(text="", fg='black')
                    logging.info("Audio : Download Started For {}".format(
                        self.var_url.get()
                    ))
                    select_file.download('Audios/')

    def clear(self):
        """Clear the all Fields."""
        logging.info("Clear Method Called")
        self.var_filetype.set('Video')
        self.var_url.set('')
        self.prog['value'] = 0
        self.btn_download.config(state=tk.DISABLED)
        self.lbl_message.config(text='')
        self.video_title.config(text='Video Title Here')
        self.video_image.config(image='')
        self.video_desc.delete('1.0', tk.END)
        self.lbl_size.config(text='Total Size: MB')
        self.lbl_percentage.config(text='Downloading:0%')
        logging.info("Cleared all fields")


if __name__ == "__main__":
    root = tk.Tk()
    obj = YoutubeApp(root)
    root.mainloop()
