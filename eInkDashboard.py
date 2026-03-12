from mod_jokes import jokes

EDP_WIDTH: int = 200
EDP_HEIGHT: int = 480

def main()->None:

    j = jokes.Jokes(EDP_WIDTH, EDP_HEIGHT)
    j.write_joke_on_canvas(0)

if __name__ == '__main__':
    main()