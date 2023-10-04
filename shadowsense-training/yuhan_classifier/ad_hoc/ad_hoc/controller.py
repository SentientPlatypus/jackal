from threading import Condition, Lock
from video_stream import Player, CameraFinished
from train_classifier import Trainer, TrainerExited
import cv2
from ffpyplayer.player import MediaPlayer
import numpy as np
__all__ = ('Controller', )


class Controller(object):

    def run(self):
        condition = Condition()

        trainer = Trainer(train_path=r"W:\Code\workorinternship\jackal\shadowsense-training\trainingdata", test_path=r"W:\Code\workorinternship\jackal\shadowsense-training\testingdata", condition=condition)
        trainer.train()
        trainer.run_classification()


        opencv_image = cv2.imread(r"W:\Code\workorinternship\jackal\shadowsense-training\testingdata\no_touch\frame20230911_171756.jpg")
        # Get the dimensions of the image
        # height, width, channels = opencv_image.shape

        # # Create a video stream with a single frame (your image)
        # video_stream = np.zeros((height, width, channels), dtype=np.uint8)
        # video_stream[:, :, :] = opencv_image

        # # Create a MediaPlayer instance with the same dimensions as the image
        # player = MediaPlayer('', width=width, height=height)
        # player.set_frame(video_stream)
        # frame, val = player.get_frame()
        # if val != 'eof':
        # trainer.request_classification(opencv_image)


        print("Got here")
        try:
            classification_result = trainer.predict_image_opencv(opencv_image)
            print("got here", classification_result)
        except TrainerExited:
            print("failed trainer exited")
            return

        if classification_result is not None:
            print("trying classification")
            original_image,prediction = classification_result
            print('predicted', prediction)


        trainer.stop()
        print("done")

        # player = Player(condition=condition, url='rtsp://admin@192.168.0.100:554/12')
        # player.play()

        # try:
        #     image_result = player.get_next_frame()
        # except CameraFinished:
        #     return

        # try:
        #     with condition:
        #         while True:
        #             condition.wait()

        #             try:
        #                 image_result = player.get_next_frame()
        #             except CameraFinished:
        #                 return

        #             if image_result is not None:
        #                 image, t = image_result
        #                 print(t, image.get_pixel_format(), image.get_buffer_size())
        #                 trainer.request_classification(image)

        #             try:
        #                 classification_result = trainer.get_next_classification_result()
        #             except TrainerExited:
        #                 return

        #             if classification_result is not None:
        #                 original_image, (buffer, prediction) = classification_result
        #                 print('predicted', prediction)

        # finally:
        #     try:
        #         player.stop()
        #     finally:
        #         trainer.stop()


if __name__ == '__main__':
    controller = Controller()
    controller.run()
    print('exited')
