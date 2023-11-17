from picamera2 import Picamera2
import time

from picamera2.encoders import Encoder, MJPEGEncoder,H264Encoder, JpegEncoder,Quality


def record_video(output_path, duration):
    try:
        # Initialize the PiCamera
        camera = Picamera2()
        encoder = MJPEGEncoder()
        # Start recording video to the specified output file
        camera.start_recording(encoder,output_path)

        # Record for the specified duration (in seconds)
        time.sleep(duration)

        # Stop recording
        camera.stop_recording()

        print(f"Video recorded to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
output_file = "output_video3.mp4"  # Change this to your desired output file path
record_duration = 10  # Record for 10 seconds, you can change this value

record_video(output_file, record_duration)