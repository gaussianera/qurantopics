
class TopicEditView():
    message = None
    error = None

class TopicAyaView():
    selected = bool
    sura_number = int
    sura_name = unicode
    aya_number = int
    aya_content = unicode
    aya_key = str

class TopicLine():
    separator = bool
    sura_number = int
    sura_name = ""
    aya_number = int
    aya_content = unicode
    
