import Adafruit_SSD1306
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Display():
    def __init__(self):

        # Raspberry Pi pin configuration:
        RST = 24
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

        # Initialize library.
        self.disp.begin()

        # Clear display.
        self.disp.clear()
        self.disp.display()

        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.title_height = 12

        # Create blank image for drawing.
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)
        
        # Load default font.
        self.font = ImageFont.load_default()

    def main_menu(self, selected_row=0):

        menu_items =  ["Start recording","Show sensor data","Set time"]

        row_height = 12
        item_pos = 20

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0,0, self.width-1, self.height-1), outline=1, fill=0)

        # Draw highlight of selected item
        self.draw.rectangle((0,0, 128 ,row_height), outline=1, fill=1)        # Draw a black filled box to clear the image.

        # Write two lines of text.
        self.draw.text((50, 0), 'Main',  font=self.font, fill=0)

        for idx, item in enumerate(menu_items):
            self.draw.text((4, item_pos+(idx*row_height)), menu_items[idx], font=self.font, fill=255)

        # Write two lines of text.
            self.draw.text((112, item_pos+(selected_row*row_height)), '<',  font=self.font, fill=255)

        # Display image.
        self.disp.image(self.image)
        self.disp.display()
    
    def recording_screen(self, duration, started=False):
        row_height = 12
        item_pos = 20

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0,0, self.width-1, self.height-1), outline=1, fill=0)

        # Draw highlight of selected item
        self.draw.rectangle((0,0, 128 ,row_height), outline=1, fill=1)

        # Write two lines of text.
        self.draw.text((23, 0), 'Start recording',  font=self.font, fill=0)

        self.draw.text((40, 18), f'Time: {duration}s',  font=self.font, fill=255)

        # Write two lines of text.
        if not started:
            self.draw.text((40, 35), 'Ready..',  font=self.font, stroke_width=3,  fill=255)
        else:
            self.draw.text((58, 35), 'Go!',  font=self.font, fill=255)

        # Display image.
        self.disp.image(self.image)
        self.disp.display()

    def splash_image(self, duration, id):
        # Load splash screen
        splash = Image.open(f'res/{id}.jpg').convert('1')

        # Display image.
        self.disp.image(splash)
        self.disp.display()
        time.sleep(duration)
    
    def countdown(self):
        for t in range(3):
            img = Image.open(f'res/{3-t}.jpg').convert('1')
            self.disp.image(img)
            self.disp.display()
            time.sleep(1)

        img = Image.open(f'res/0.jpg').convert('1')
        self.disp.image(img)
        self.disp.display()
            

    def sensor_screen(self, sensor_id, values):
        
        sensors = ["Kufendistanz", "Accelerometer", "Gyrosensor", "Fluxmeter"]

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0,0, self.width-1, self.height-1), outline=1, fill=0)

        # Titlebar
        self.draw.rectangle((0,0, 128 ,self.title_height), outline=1, fill=1)
        self.draw.text((4, 0), '<',  font=self.font, fill=0)
        self.draw.text((22, 0), f'{sensors[sensor_id]}',  font=self.font, fill=0)
        self.draw.text((120, 0), '>',  font=self.font, fill=0)
        
        if sensor_id == 0:

            row_space = 12

            #values = [25, 97, 12, 44]
            labels = ['vl','vr','hl','hr']

            for i, v in enumerate(values):
                self.draw.text((111, 14+(i*row_space)), f'{labels[i]}',  font=self.font, fill=1)
                self.draw.rectangle((5, 17+(i*row_space), 105, 22+(i*row_space)), outline=1, fill=0)
                self.draw.rectangle((5, 17+(i*row_space), v, 22+(i*row_space)), outline=1, fill=1)

        if sensor_id == 1:

            row_space = 17
            values = [46, 65, 78]
            labels = ['X','Y','Z']

            for i, v in enumerate(values):
                self.draw.text((113, 14+(i*row_space)), f'{labels[i]}',  font=self.font, fill=1)
                self.draw.rectangle((5, 17+(i*row_space), 105, 22+(i*row_space)), outline=1, fill=0)
                self.draw.rectangle((5, 17+(i*row_space), v, 22+(i*row_space)), outline=1, fill=1)

        if sensor_id == 2:

            row_space = 17
            values = [14, 65, 89]
            labels = ['X','Y','Z']

            for i, v in enumerate(values):
                self.draw.text((113, 14+(i*row_space)), f'{labels[i]}',  font=self.font, fill=1)
                self.draw.rectangle((5, 17+(i*row_space), 105, 22+(i*row_space)), outline=1, fill=0)
                self.draw.rectangle((5, 17+(i*row_space), v, 22+(i*row_space)), outline=1, fill=1)

        if sensor_id == 3:

            row_space = 17
            values = [33, 56, 9]
            labels = ['X','Y','Z']

            for i, v in enumerate(values):
                self.draw.text((113, 14+(i*row_space)), f'{labels[i]}',  font=self.font, fill=1)
                self.draw.rectangle((5, 17+(i*row_space), 105, 22+(i*row_space)), outline=1, fill=0)
                self.draw.rectangle((5, 17+(i*row_space), v, 22+(i*row_space)), outline=1, fill=1)

        # Display image.
        self.disp.image(self.image)
        self.disp.display()

    def set_time_screen(self, duration):

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0,0, self.width-1, self.height-1), outline=1, fill=0)

        # Titlebar
        self.draw.rectangle((0,0, 128 ,self.title_height), outline=1, fill=1)

        self.draw.text((22, 0), 'Set time',  font=self.font, fill=0)
        self.draw.text((22, 30), f'{duration} Sec.',  font=self.font, fill=1)

        # Display image.
        self.disp.image(self.image)
        self.disp.display()


if __name__ == "__main__":
    display = Display()

    while True:
        display.splash_image(1, 6)
    

        display.main_menu(selected_row=0)
        time.sleep(1)

        display.recording_screen(57, started=False)
        time.sleep(1)

        display.recording_screen(32, started=True)
        time.sleep(1)

        display.main_menu(selected_row=1)
        time.sleep(1)

        for x in range(4):
            display.sensor_screen(x,1)
            time.sleep(1)

        display.main_menu(selected_row=2)
        time.sleep(1)
        
        for t in range(50,56):

            display.set_time_screen(t)
            time.sleep(0.2)

