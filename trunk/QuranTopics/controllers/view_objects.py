
class TopicEditView():
    message = None
    error = None

class TopicAyaView():
    position = int
    selected = bool
    sura_number = int
    sura_name = unicode
    aya_number = int
    aya_content = unicode
    aya_key = str

class TopicLine():
    new_section = bool
    sura_number = int
    sura_name = ""
    aya_number = int
    aya_content = unicode
    

