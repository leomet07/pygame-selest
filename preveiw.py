import cv2
import json
LINES = []
data = []

#loading in the level
with open('level.json') as json_file:
    data = json.load(json_file)

current_level = 0
for i in data:

    # loading in the level
    with open('level.json') as json_file:
        data = json.load(json_file)
        LINES = data[current_level]["level"]
    SCORE = data[0]["time"]
    print(LINES)
    bg = cv2.imread("src/bg.png")

    bg = cv2.resize(bg, (500,500))
    #draw the level on the bg
    for line in LINES:
        lineThickness = 2
        [x1, y1] = line["xy"]
        [x2, y2] = line["x2y2"]
        cv2.line(bg, (x1, y1), (x2, y2), (0, 255, 0), lineThickness)

    cv2.imshow("window",bg)
    if cv2.waitKey(0) & 0xff == ord("q"):
        cv2.destroyAllWindows()

    current_level += 1

