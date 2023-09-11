import cv2
import os
import time
import datetime
# Create directories if they don't exist


def main(touchDirectory="webcam/touch", noTouchDirectory="webcam/no_touch", mode=None, camera=1, saving=True):
    if not mode:
        print("No mode selected")
        return
    print(f"MODE: {mode}")
    

    if not os.path.exists(touchDirectory):
        os.makedirs(touchDirectory)
    if not os.path.exists(noTouchDirectory):
        os.makedirs(noTouchDirectory)

    print("WE OUT")


    if mode not in ["touch", "no_touch"]:
        return 


    cap = cv2.VideoCapture(camera)


    while cap.isOpened():
        success, img = cap.read()
        current_datetime = datetime.datetime.now()
        if not success:
            continue
        
        cv2.imshow("livefeed", img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break


        path = touchDirectory if mode == "touch" else noTouchDirectory
        filename = "{}/frame{}.jpg".format(path, current_datetime.strftime("%Y%m%d_%H%M%S"))

        ##cv2.putText(img, f"mode: {mode}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("livefeed", img)
        if saving:
            time.sleep(1)
            cv2.imwrite(filename, img)


    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(mode="touch", camera=1, saving=True)