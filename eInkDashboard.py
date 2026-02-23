from canvas import canvas

EDP_WIDTH: int = 800
EDP_HEIGHT: int = 480

def main()->None:
    print("Test", flush=True)
    fr = canvas.Canvas(200, 100)
    fr.showImage()
    fr.saveImage()

if __name__ == '__main__':
    main()