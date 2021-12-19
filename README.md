![Framer banner](docs/banner.png)
Create a strip of color representing each frame in a video file.

[Try it out here!](https://share.streamlit.io/nstgeorge/framer/main/web.py)

## Setup

If you're making a strip using a small file (<500 MB), you should try the 
[web version](https://share.streamlit.io/nstgeorge/framer/main/web.py). This should be fine for individual scenes and some short films, or movies with reduced resolution. Framer can work with any resolution, so you can massively improve compute and upload time by reducing the resolution by 4-8x. I generated a strip for Blade Runner 2049 using a 240x100 file, which was small enough to easily be uploaded to the web UI. To generate a tiny video file, you can use a tool like [Handbrake](https://handbrake.fr).

### Local installation

If you want to create a strip for a full movie, you should download the local version from GitHub, then install the requirements.

```shell
# This will get the Framer code from GitHub, then install the requirements.
git clone git@github.com:nstgeorge/Framer.git && cd Framer && pip install -r requirements.txt
```

If you run into any issues with the above command, make sure you have **Python 3.6+** installed and running on your machine.

### Optional: Using the web UI locally

You can host your own version of the web UI. There are limited benefits to doing this over simply using the web version:

1. Set your own upload limit. In `.streamlit/config.toml`, set `maxUploadSize` to your desired limit in MB.
2. Lower upload times.

To start the local server, run the following command from the Framer folder after installation:

```shell
streamlit run framer.py
```

You will see a Local URL. Click on that to access the web UI.

**Important:** If you change the upload limit, keep in mind that the entire movie file is placed in RAM when you upload.
There's nothing I can do about this since it's on Streamlit's end, so make sure you **don't increase the file upload limit
beyond the amount of RAM in your machine.**

## Usage

Here is the usage statement for this program:

```
usage: framer.py [-h] [--vignette] path output size

Generate a strip of colors for each frame in a video file.

positional arguments:
  path        The path to the video file.
  output      Output file name.
  size        Dimensions of the output file, XxY (like 2000x400). If the X value is 0, it will automatically be 1 pixel per frame with a maximum of 2000. If Y is also 0 or no size is defined, it will default to a 5:1 aspect ratio.

optional arguments:
  -h, --help  show this help message and exit
  --vignette  Applies a vignette filter to the strip.

```

You can access this using `python framer.py -h`. I'll try to keep this updated, but it's possible I'll forget to change it.

**Note:** The vignette effect much improves the look of the result and I highly recommend it. It's on by default in the web version.

### Examples

If I have a video file called `video.mp4` and I want an output called `video_strip.png` with the default size and a vignette effect, I can use this command:
```shell
python framer.py output.mp4 video_strip.png --vignette
```

If I want the same output but 3000px long, I can use this:

```shell
python framer.py output.mp4 video_strip.png 3000x0 --vignette
```

Because the `y` is `0`, the program defaults to a 5:1 aspect ratio, and the end result is the same image scaled up.

If you have any problems or suggestions, feel free to [open an issue on GitHub](https://github.com/nstgeorge/Framer/issues)!
