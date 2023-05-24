class Audio:
    '''
    Los datos que se introduzcan por la función de lectura se guardaran dentro de esta classe
    para que despues, al volver a codificarla, usar exactamente la misma cabecera
    ****no demasiado util si trabajamos con mas tipos de archivos de audio
    '''
    def Audio(self, chunkID, chunksize, format, subchunk1ID, subchunk1size, audioformat, numchanels,
              samplerate, byterate, blockalign, bitspersample, subchunk2ID, subchunk2size,data):
        self.chunkID=chunkID
        self.chunksize=chunksize
        self.format=format
        self.subchunk1ID=subchunk1ID
        self.subchunk1size=subchunk1size
        self.audioformat=audioformat
        self.numchanels=numchanels
        self.samplerate=samplerate
        self.byterate=byterate
        self.blockalign=blockalign
        self.bitspersample=bitspersample
        self.subchunk2ID=subchunk2ID
        self.subchunk2size=subchunk2size
        self.data=data
