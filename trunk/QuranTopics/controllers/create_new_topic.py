# coding: utf8

import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from controllers.view_objects import TopicEditView, TopicAya, TopicLine
from controllers.entities import Sura, Aya, Topic, TopicAya
from controllers.page_controller import PageController


class CreateNewTopic(PageController):

    def get(self):
    
        template_values = {
          }
    
        path = self.get_view_path('edit_topic.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):

        topic_edit_view = self.populate_view()
        topic_ayat = topic_edit_view.ayat_display

        if (self.request.get('add')):
            sura = Sura.get_by_number(topic_edit_view.sura)
            ayat = sura.get_ayat_query_in_range(topic_edit_view.from_aya, topic_edit_view.to_aya)
            added_ayat = self.make_ayat_display_from_ayat(ayat)
            topic_edit_view.ayat_display = self.merge_added_ayat_to_topic_ayat(topic_ayat, added_ayat, topic_edit_view.position)
        elif (self.request.get('edit')):
            self.edit_topic(topic_edit_view)
        elif (self.request.get('remove')):
            topic_edit_view.ayat_display = self.remove_selected(topic_ayat)
        elif (self.request.get('move_to_position')):
            topic_edit_view.ayat_display = self.move_selected_to_position(topic_ayat, topic_edit_view.to_position)
        elif (self.request.get('save')):
            self.save_topic(topic_edit_view)
        else:
            logging.info("operation not handled")

        template_values = {
           'topic': topic_edit_view
          }
    
        path = self.get_view_path('edit_topic.html')
        self.response.out.write(template.render(path, template_values))
        
    def save_topic(self, topic_edit_view):
        title = self.request.get('title')
        if not title:
            topic_edit_view.error = "لم يتم إدخال عنوان الموضوع"
        elif not topic_edit_view.ayat_display:
            topic_edit_view.error = "الموضوع لا يتضمن أي آيات"
        else:
            if topic_edit_view.topic_id:
                logging.debug("topic_edit_view.topic_id = " + str(topic_edit_view.topic_id))
                topic = Topic.get_by_id(topic_edit_view.topic_id)
            else:
                topic = Topic()
                topic.put()
                topic.topic_id = topic.key().id()
                topic_edit_view.topic_id = topic.topic_id 
            topic.title = title
            topic.put()
            ayat = self.make_ayat_from_ayat_display(topic_edit_view.ayat_display)
            topic.set_ayat(ayat)

    
    def edit_topic(self, topic_edit_view):
        topic_id = self.get_int('topic_id')
        topic = Topic.get_by_id(topic_edit_view.topic_id)
        topic_edit_view.topic_id = topic_id
        topic_edit_view.title = topic.title
        topic_edit_view.ayat_display = self.make_ayat_display_from_ayat(topic.get_ayat())
        

    def populate_view(self):
        topics_edit_view = TopicEditView()
        topics_edit_view.topic_id = self.get_int('topic_id')
        topics_edit_view.title = self.request.get('title')
        topics_edit_view.sura = self.get_int('sura')
        topics_edit_view.from_aya = self.get_int('from_aya')
        topics_edit_view.to_aya = self.get_int('to_aya')
        topics_edit_view.position = self.get_int('position')
        topics_edit_view.to_position = self.get_int('to_position')
        self.populate_ayat(topics_edit_view)
        return topics_edit_view

    def populate_ayat(self, topics_edit_view):
        count = 1
        ayat_display = []
        while (self.request.get("sura_" + str(count))):
            topic_aya = TopicAya()
            topic_aya.selected = self.get_selected(count)
            topic_aya.sura_number = self.get_sura(count)
            topic_aya.aya_number = self.get_aya(count)
            topic_aya.aya_content = self.get_aya_content(count)
            ayat_display.append(topic_aya)
            count = count + 1
        
        topics_edit_view.ayat_display = ayat_display
        
    
    def make_ayat_display_from_ayat(self, ayat):
        ayat_display = []
        for aya in ayat:
            aya_display = TopicAya()
            aya_display.sura_number = aya.sura.number
            aya_display.aya_number = aya.number
            aya_display.aya_content = aya.content
            ayat_display.append(aya_display)
        return ayat_display

            
    def make_ayat_from_ayat_display(self, ayat_display):
        logging.debug("start: make_ayat_from_ayat_display")    
        ayat = []
        for aya_display in ayat_display:
            aya = Aya.get_by_sura_and_aya_number(aya_display.sura_number, aya_display.aya_number)
            ayat.append(aya)
        logging.debug("end: make_ayat_from_ayat_display")    
        return ayat
            
    
    def merge_added_ayat_to_topic_ayat(self, topic_ayat, added_ayat, position):
        ayat_to_add = []
        for aya_display in added_ayat:
            if not self.list_contains_aya(topic_ayat, aya_display):
                ayat_to_add.append(aya_display)
        
        if position >= 1 and position <= len(topic_ayat):
            position = position - 1
            topic_ayat = topic_ayat[:position] + ayat_to_add + topic_ayat[position:]
        else:
            topic_ayat.extend(ayat_to_add)
        return topic_ayat
    
    
    def list_contains_aya(self, ayat_display, aya_display):
        for list_aya in ayat_display:
            if self.same_aya(list_aya, aya_display):
                return True
        return False
    
    def remove_selected(self, topic_ayat):
        new_set = []
        for aya_display in topic_ayat:
            if (not aya_display.selected):
                new_set.append(aya_display)
        return new_set
    
    
    def move_selected_to_position(self, topic_ayat, to_position):
        before_position = []
        selected = []
        after_position = []
        count = 1
        for aya_display in topic_ayat:
            if aya_display.selected:
                selected.append(aya_display)
            elif count < to_position:
                before_position.append(aya_display)
            else:
                after_position.append(aya_display)
            count += 1
        return before_position + selected + after_position
    
    
    def same_aya(self, aya1, aya2):
        return aya1.sura_number == aya2.sura_number and aya1.aya_number == aya2.aya_number
        
    
    def get_sura(self, order):
        return self.get_int("sura_" + str(order))
    

    def get_aya(self, order):
        return self.get_int("aya_" + str(order))
    
    
    def get_aya_content(self, order):
        return self.request.get("aya_content_" + str(order))
    
    
    def get_selected(self, order):
        return self.request.get("selected_" + str(order)) == "on"
