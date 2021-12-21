import streamlit as st
import tempfile
import cv2
from framer import Framer


def hash_framer(f):
    """Not a real hash function, but good enough for us."""
    return f.get_path()


@st.cache(hash_funcs={Framer: hash_framer}, suppress_st_warning=True)
def generate(framer):
    return framer.generate(st=True)


@st.cache(hash_funcs={Framer: hash_framer})
def get_vignette(framer):
    return framer.apply_vignette()


@st.cache(allow_output_mutation=True)
def init_framer():
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(input_file.read())
    return Framer(temp.name, (x, y))


if __name__ == "__main__":
    st.image("docs/banner.png")
    st.markdown("Generate a strip of colors based on the average color of each frame in a video.")
    st.markdown("**File**")
    input_file = st.file_uploader("Upload the video file that generates the color strip.", type=["mp4", "mkv", "mov", "m4v"])

    with st.expander("Help, I can't upload my movie file!"):
        st.markdown("""
            Unfortunately, due to the limitations of the free hosting I'm using, I can't offer larger upload limits. 
            You have a couple options for what you can do:

            1. Reduce the size of the file using a tool like [Handbrake](https://handbrake.fr/). Framer can work with 
            tiny resolutions, so you can significantly reduce the file size by reducing the resolution.

            2. Download the local version from the [GitHub repo](https://github.com/nstgeorge/Framer). This version 
            includes a `README.md` file that will tell you exactly how to use it.
        """)

    st.markdown("**Dimensions**: Input the desired dimensions of the strip. If you leave these at 0, "
                "there will be one pixel per frame horizontally and 1/5 of that number vertically, with a maximum of 2000.")

    col1, col2 = st.columns(2)
    x = col1.number_input("X", value=0)
    y = col2.number_input("Y", value=0)

    if input_file is not None:
        if st.button("Start"):
            status = st.empty()
            status.markdown("Starting...")
            framer = init_framer()
            status.markdown("Working...")
            progress = st.empty()
            result = generate(framer)
            result_vignette = get_vignette(framer)
            status.markdown("Done!")
            tmp_result = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            cv2.imwrite(tmp_result.name, result_vignette)
            st.image(tmp_result.read(), caption="Your completed image")
            # st.download_button("Download", tmp_result.read(), file_name="framer_strip.png", mime="image/png")


