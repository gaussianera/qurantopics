
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from controllers.view_objects import TopicEditView, TopicAya, TopicLine
from controllers.entities import Sura, Aya, Topic, TopicAya
from controllers.page_controller import PageController


class ViewTopic(PageController):

    def get(self):
        topic_id = self.get_int("topic_id")
        topic = Topic.get_by_id(topic_id)
        topic_lines = self.make_topic_lines(topic.get_ayat())
    
        template_values = {
           'topic' : topic,
           'lines' : topic_lines
          }
    
        path = self.get_view_path('view_topic.html')
        self.response.out.write(template.render(path, template_values))
    
    
    def post(self):
        if (self.request.get('delete')):
            topic_id = self.get_int('topic_id')
            Topic.remove_by_id(topic_id)
            self.redirect("/")

    
    def make_topic_lines(self, ayat):
        topic_lines = []
        prev_sura = -1
        prev_aya = -1
        for aya in ayat:
            topic_line = TopicLine()
            if aya.sura.number != prev_sura or aya.number != prev_aya + 1:
                topic_line.separator = True
                topic_lines.append(topic_line)
                topic_line = TopicLine()

            topic_line.sura_number = aya.sura.number
            topic_line.aya_number = aya.number
            topic_line.aya_content = aya.content
            topic_lines.append(topic_line)
            prev_sura = aya.sura.number
            prev_aya = aya.number
        return topic_lines
