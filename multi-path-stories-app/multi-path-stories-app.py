from flask import Flask, request, render_template, redirect

def get_sentence_for_story(story):
  if(story != None):
    return dictOfStories[story]["mainSentence"]

def get_next_story_id():
    return ("a" + str(len(dictOfStories) + 1))

def create_new_story_dict(sentence):
  return {"mainSentence": sentence, "top": None, "right": None, "bottom": None, "left": None }

def link_story_to_another(currentStory, position, nextStory):
  dictOfStories[currentStory][position] = nextStory

def add_story(currentStory, position, sentence):
  story_ID = get_next_story_id()
  new_story_dict = create_new_story_dict(sentence)
  dictOfStories[story_ID] = new_story_dict
  link_story_to_another(currentStory, position, story_ID)
  return story_ID

dictOfStories = {}
dictOfStories["a1"] = create_new_story_dict("Once upon a time there was a girl who wanted to fly.")
add_story("a1", "top", "A wolf ate her")
add_story("a1", "right", "And she also wanted to have pizza.")
add_story("a2", "top", "And she died.")

app = Flask(__name__, static_folder="static", static_path="")

@app.route('/')
def index():
    return redirect("story/a1")

@app.route('/new_story', methods=['POST'])
def new_story():
    position = request.form["position"]
    currentStory = request.form["currentStory"]
    newSentence = request.form["newSentence"]
    story_id = add_story(currentStory, position, newSentence)
    return redirect("/story/" + story_id)

@app.route('/story/<story>')
def show_story(story):

    currentStory = dictOfStories.get(story)

    topSentence = get_sentence_for_story(currentStory["top"])
    rightSentence = get_sentence_for_story(currentStory["right"])
    bottomSentence = get_sentence_for_story(currentStory["bottom"])
    leftSentence = get_sentence_for_story(currentStory["left"])

    return render_template("index.html", mainSentence=currentStory["mainSentence"],
                           topLink=currentStory["top"],
                           bottomLink=currentStory["bottom"],
                           leftLink=currentStory["left"],
                           rightLink=currentStory["right"],
                           topSentence=topSentence,
                           rightSentence=rightSentence,
                           bottomSentence=bottomSentence,
                           leftSentence=leftSentence,
                           currentStory = story)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
