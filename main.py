# IPND Stage 5 FINAL WEBAPP!!


import os
import jinja2
import webapp2
from google.appengine.ext import ndb

# Set up jinja environment
# os.path.join , This concatenates the current directory with the template directory (/mainpage/template)
template_dir = os.path.join(os.path.dirname(__file__), "templates")

##### A template library is a library to build complicated strings or HTML. We use jinja2 as our template library.

# this variable states that the jinja2 enviorment will look for the variable template_dir for its template file. This is a file system loader, when we render templates, jinja will look for the templates in this directory. autoescape = True sets the autoescaping for html.  

# using the pipe "escape" will escape the template, bot preferred to opt out, best to opt out using the autoescape true  ----  {% example | escape %}
# using the pipe "safe" allows you to opt out of escaping so that HTML will render.  {% example | safe %}

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


        # takes a filename and parameters, using jinja to get template.
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)


         # takes template, and parameters, uses self.write to send it back to the browswer.
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))



#########
#########


# Define FoodTruck Class to store truck name, allergens,links of pictures, and recipe name, etc.
class FoodTruck(ndb.Model):
    picture_link = ndb.StringProperty()
    service_type = ndb.StringProperty(indexed = True)
    truck_name = ndb.StringProperty(indexed = True)
    recipe_name= ndb.StringProperty(indexed = True)
    ingredient_list = ndb.StringProperty()
    chef_notes = ndb.StringProperty()
    pack_list = ndb.StringProperty()
    allergens = ndb.StringProperty()
    video_link = ndb.StringProperty()    
    date = ndb.DateTimeProperty(auto_now_add=True)
    doc_link = ndb.StringProperty()
    plating = ndb.StringProperty()



# --------------------------------------Handler Classes---------------------------------------------

class MainPage(Handler):
    def get(self):

      # error message
      error = self.request.get('error','')
      input_truck_name = self.request.get('foodtruck_name')
      
    # Query the Datastore and order earliest date first
      query = FoodTruck.query(FoodTruck.truck_name == input_truck_name)  # test line
      #query = FoodTruck.query().order(FoodTruck.date)
      query_num_list = 5  
      foodtruck_list = query.fetch(query_num_list) 
      self.render('index.html', query= query, error= error) 



class StageHandler(Handler):
    def get(self, stage_num):
        self.render('stage{0}.html'.format(stage_num))


class SuccessHandler(Handler):
    def get(self):
        self.render('/form_success.html')

class MenuHandler(Handler):
    def get(self):
        
      # error message
      error = self.request.get('error','')
    
    # Query the Datastore and order earliest date first
      query = FoodTruck.query().order(FoodTruck.date)
      query_num_list = 5  
      foodtruck_list = query.fetch(query_num_list) 
      self.render('menu_form.html', query= query, error= error) 

    def post(self):
      picture_link = self.request.get('picture_link')
      service_type = self.request.get('service_type')
      truck_name = self.request.get ('truck_name')
      recipe_name = self.request.get ('recipe_name')
      ingredient_list = self.request.get ('ingredient_list')
      chef_notes = self.request.get ('chef_notes')
      pack_list = self.request.get ('pack_list')
      allergens = self.request.get ('allergens')
      video_link = self.request.get ('video_link')
      doc_link = self.request.get('doc_link')
      plating = self.request.get('plating')

    # Allow ability to create food truck menu objects and save to Datastore

      if picture_link and service_type and recipe_name and ingredient_list and chef_notes and pack_list and allergens and truck_name and recipe_name and doc_link and plating:
        foodtruck_entity = FoodTruck(picture_link=picture_link, service_type = service_type, truck_name = truck_name, recipe_name = recipe_name, ingredient_list = ingredient_list, chef_notes = chef_notes, pack_list= pack_list, allergens = allergens, video_link = video_link, doc_link = doc_link, plating= plating)

        # put stores entry to datastore!
        foodtruck_entity.put()
        
        # DEBUG: For local development. Need to wait a little bit for the local Datastore to update
        import time
        sleep_time = 0.1
        time.sleep(sleep_time)
        self.redirect('/form_success')
      else:
        # redirects page if error
        self.redirect('/menu_form?error=*** ERROR!! Please be sure to fill out ALL the sections!!! ***')


class QueryHandler(Handler):
    def get(self):

      # Query the Datastore and order earliest date first
      query = FoodTruck.query().order(FoodTruck.date)
      input_truck_name = self.request.get('foodtruck_name')
      
    
      query = FoodTruck.query(FoodTruck.truck_name == input_truck_name)  
      query_num_list = 5  
      foodtruck_list = query.fetch(query_num_list) 
      self.render('index.html', query= query, error= error) 
      

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/menu_form', MenuHandler),
    ('/form_success', SuccessHandler),
    ('/query_return', QueryHandler),
    ('/stage(\d+)', StageHandler),
], debug=True)




