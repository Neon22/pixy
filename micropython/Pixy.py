#!/usr/bin/python

# communication module for talking to the Pixy (CMUCam5) from micropython


#import SPI

class Pixy(object):
    """ Enable comms with Pixy to return blobs.
        - can filter blobs returned by model# and by area bounds.
        - blob is model#, x,y,w,h where x,y are center of blob
    """
    start_word = 0xaa55 # marks start of SPI packet for Pixy
    end_word   = 0xccaa # markes end of packet
    
    def __init__(self, spi_args, min_area=0, max_area=0xFFFF):
        " store recent blobs, area bounds "
        self.blobs = []
        self.min_area = min_area
        self.max_area = max_area
        # Open the port
        self.port = SPI(spiargs) # !! whatever this is
        self.port.open()         #!!

    def set_size_limit(self, min_area, max_area):
        """ set min, max area.
            - blobs smaller or larger will be ignored
        """
        self.min_area = min_area
        self.max_area = max_area

    #!! would be good to have timeout in here
    def sync(self):
        " read spi input until see start_word "
        start = self.get_spi_word()
        while start != Pixy.start_word:
            start = self.get_spi_word()

    #!! would be good to have timeout in here        
    def get_spi_word(self):
        " read two transfers and create word "
        return self.port.read() << 8 + self.port.read()

    #!! would be good to have timeout in here
    def get_blobs(self, model_ref=-1):
        """ Loop collecting blobs until done or error
            blob msg is start marker, checksum,model,x,y,w,h, end marker
            where x,y are coords of center. All are 16 bit words.
        """
        self.blobs = [] # clear pre-existing blobs
        start = self.get_spi_word()
        if start != Pixy.start_word:
            self.sync()
        #
        done = False
        while not done:
            blob = [] # one at a time
            checksum = self.get_spi_word()
            count = 0
            if count < 5:
                blob.append(self.get_spi_word())
            # read end marker
            if Pixy.end_word == self.get_spi_word():
                # ended so done
                done = True
            if checksum != sum(blobs):
                # checksum did not match so abort
                done = True
            area = blob[3] * blob[4]
            if self.min_area < area < self.max_area:
                if model_ref < 0 or model_ref == model:
                    self.blobs.append(blob)
        # done
        return self.blobs



###
if __name__ == '__main__':

    pixy = Pixy()
    blobs = pixy.get_blobs()
    print ("{} blobs found".format(len(blobs)))
    for (model,x,y,w,h) in blobs:
        print (model," ",x,y,w,h)
