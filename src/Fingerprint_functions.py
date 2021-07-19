import time
from pyfingerprint.pyfingerprint import PyFingerprint #Sensor Library
import os


class fingerprint_sensor:

    def __init__(self):
        # Sensor Initialisation
        try:
            self.f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if (self.f.verifyPassword() == False):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
    def enrollment(self):
        try:
            print('Waiting for finger...')

            # Wait that finger is read
            while (self.f.readImage() == False):
                pass

            # Converts read image to characteristics and stores it in charbuffer 1
            self.f.convertImage(0x01)

            # Checks if finger is already enrolled
            result = self.f.searchTemplate()
            positionNumber = result[0]

            if (positionNumber >= 0):
                print('Template already exists at position #' + str(positionNumber))

            time.sleep(2)

            # Wait that finger is read again
            while (self.f.readImage() == False):
                pass

            # Converts read image to characteristics and stores it in charbuffer 2
            self.f.convertImage(0x02)

            # Compares the charbuffers
            if (self.f.compareCharacteristics() == 0):
                raise Exception('Fingers do not match')

            # Creates a template
            self.f.createTemplate()

            # Saves template at new position number
            positionNumber = self.f.storeTemplate()
            print('Finger enrolled successfully!')
            print('New template position #' + str(positionNumber))

            # Exports the template to a temporaryfile
            template = self.f.downloadCharacteristics()
            temp_file = open("template.txt", "w+")
            for item in template:
                temp_file.write(str(item) + "\n")
            temp_file.close()
            return os.path.abspath('temp_file.txt')

        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))

    def authentication(self,file_path):
        try:
            match_flag = 0
            # Uploading the template to the sensor
            temp_file = open(file_path, "r")
            template = []
            for x in temp_file:
                template.append(int(x))
            temp_file.close()
            self.f.uploadCharacteristics(characteristicsData=template)
            Index_template = self.f.storeTemplate()

            # Tries to search the finger
            print('Waiting for finger...')

            # Wait that finger is read
            while (self.f.readImage() == False):
                pass

            # Converts read image to characteristics and stores it in charbuffer 1
            self.f.convertImage(0x01)

            # Searches template
            result = self.f.searchTemplate()

            positionNumber = result[0]

            if (positionNumber == -1):
                print('No match found!')
                match_flag = 0
            elif (positionNumber == Index_template):
                print('Matched')
                match_flag = 1

            return match_flag


        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))

    def Clear_Sensor(self):
        # Deleting the database
        self.f.clearDatabase()


