import argparse
import cv2
import numpy as np
from tqdm import tqdm
from stqdm import stqdm


class Framer:
    def __init__(self, path, dim):
        self.__path = path
        self.__current_frame = 0
        self.__frame_count = self.__get_frame_count()
        self.__x = int(dim[0]) if int(dim[0]) != 0 else self.__frame_count
        self.__y = int(dim[1]) if int(dim[1]) != 0 else int(self.__x / 5)
        self.__result = False

        self.__capture = cv2.VideoCapture(path)

        if self.__frame_count == 0:
            print(
                "Failed to read video file. Is the path correct? If so, check that OpenCV has the codecs required to "
                "read this file.")
            exit(1)

    def __get_frame_count(self):
        """Get the number of frames in the video either using the metadata or counting manually."""
        frame_count = 0
        try:
            frame_count = int(self.__capture.get(cv2.CAP_PROP_FRAME_COUNT))
        except:
            frame_count = self.__slow_frame_count()
        return frame_count

    def __slow_frame_count(self):
        """Calculate the number of frames in the video manually."""
        frame_count = 0
        temp_capture = cv2.VideoCapture(self.__path)
        while True:
            success, frame = temp_capture.read()
            if not success:
                break
            frame_count += 1
        temp_capture.release()
        return frame_count

    def __read_next_frame(self):
        """Read the next frame in the video file."""
        self.__current_frame += 1
        return self.__capture.read()

    def get_path(self):
        return self.__path

    def apply_vignette(self):
        """Apply a vignette filter to the image result. Returns 0 if an image hasn't been generated yet."""
        x_modifier = np.ones((self.__x, 1))
        y_kernel = cv2.getGaussianKernel(self.__y, self.__y / 4)
        kernel = y_kernel * x_modifier.T
        mask = 255 * kernel / np.linalg.norm(kernel)
        if self.__result is not False:
            output = np.copy(self.__result)
            for i in range(3):
                output[:, :, i] = output[:, :, i] * mask
            output = cv2.convertScaleAbs(output, alpha=3.5, beta=5)
            return output
        else:
            return 0

    def generate(self, st=False):
        progress_func = stqdm if st else tqdm
        """Generate the image."""
        print("Beginning generation on {} ({} frames)...".format(self.__path, self.__frame_count))
        mean_colors = np.empty((self.__frame_count, 1, 3))
        for i in progress_func(range(self.__frame_count)):
            success, frame = self.__read_next_frame()
            if not success:
                print("Failed to read frame {}.".format(i))
                return 1
            mean_colors[i][0] = np.asarray(cv2.mean(frame)[:3])

        # Make the strip horizontal, then resize to the user's expected size
        mean_colors = cv2.rotate(mean_colors, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.__result = cv2.resize(mean_colors, (self.__x, self.__y))
        return self.__result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a strip of colors for each frame in a video file.")
    parser.add_argument("path", help="The path to the video file.")
    parser.add_argument("output", help="Output file name.")
    parser.add_argument("size", help="Dimensions of the output file, XxY (like 2000x400). "
                                     "If the X value is 0, it will automatically be 1 pixel per frame. "
                                     "If Y is also 0, it will default to a 5:1 aspect ratio.")
    parser.add_argument("--vignette", action="store_true", help="Applies a vignette filter to the strip.")

    args = parser.parse_args()

    framer = Framer(args.path, args.size.split("x"))
    result = framer.generate()
    if args.vignette:
        result = framer.apply_vignette()

    if cv2.imwrite(args.output, result):
        print("Saved to {}".format(args.output))
    else:
        print("File not saved. Check permissions for the location you're trying to save to.")

