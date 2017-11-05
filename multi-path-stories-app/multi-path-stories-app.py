from flask import Flask, request, render_template, redirect

def get_sentence_for_story(story_id):
  if(story_id != None):
    return dict_of_stories[story_id]["main_sentence"]

def get_next_story_id():
    return ("a" + str(len(dict_of_stories) + 1))

def create_new_story_dict(sentence):
  return {"main_sentence": sentence, "top": None, "right": None, "bottom": None, "left": None }

def link_story_to_another(current_story_id, position, next_story_id):
  dict_of_stories[current_story_id][position] = next_story_id

def add_story(current_story_id, position, sentence):
  story_id = get_next_story_id()
  new_story_dict = create_new_story_dict(sentence)
  dict_of_stories[story_id] = new_story_dict
  link_story_to_another(current_story_id, position, story_id)
  return story_id

dict_of_stories = {}
dict_of_stories["a1"] = create_new_story_dict("Once upon a time there was a girl who wanted to fly.")


app = Flask(__name__, static_folder="static", static_path="")

@app.route('/')
def index():
    return redirect("story/a1")

@app.route('/new_story', methods=['POST'])
def new_story():
    position = request.form["position"]
    current_story_id = request.form["current_story_id"]
    new_sentence = request.form["new_sentence"]
    story_id = add_story(current_story_id, position, new_sentence)
    return redirect("/story/" + story_id)

@app.route('/story/<story_id>')
def show_story(story_id):

    current_story_dict = dict_of_stories.get(story_id)

    top_sentence = get_sentence_for_story(current_story_dict["top"])
    right_sentence = get_sentence_for_story(current_story_dict["right"])
    bottom_sentence = get_sentence_for_story(current_story_dict["bottom"])
    left_sentence = get_sentence_for_story(current_story_dict["left"])

    return render_template("index.html", main_sentence=current_story_dict["main_sentence"],
                           top_story_id=current_story_dict["top"],
                           bottom_story_id=current_story_dict["bottom"],
                           left_story_id=current_story_dict["left"],
                           right_story_id=current_story_dict["right"],
                           top_sentence=top_sentence,
                           right_sentence=right_sentence,
                           bottom_sentence=bottom_sentence,
                           left_sentence=left_sentence,
                           current_story_id = story_id)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
