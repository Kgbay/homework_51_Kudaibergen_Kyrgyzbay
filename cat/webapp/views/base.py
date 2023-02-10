import random
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from webapp.json_w_r import JsonWriterReader


def index_view(request: WSGIRequest):
    name = request.GET.get('name')
    return render(request, 'index.html', context={
        'name': name
    })


class CatParams:
    age = random.randint(1, 18)
    happiness = random.randint(0, 100)
    satiety = random.randint(0, 100)
    state = random.choice(('спит', 'бодрствует'))

    def get_age_naming(self):
        if self.age == 1:
            age_naming = 'год'
        elif self.age > 1 and self.age < 5:
            age_naming = 'года'
        else:
            age_naming = 'лет'
        return age_naming


def cat_stat_view(request: WSGIRequest):
    name = request.GET.get('name')
    select = request.GET.get('select')
    catparams = CatParams()
    state = catparams.state
    mood = ''

    if name:
        json_data = JsonWriterReader(name, catparams.age, catparams.happiness, catparams.satiety, catparams.get_age_naming())
        json_data.write_into()
    else:
        json_data = JsonWriterReader(name, catparams.age, catparams.happiness, catparams.satiety, catparams.get_age_naming())

    json_reader = json_data.read_from()

    if select == 'feed':
        if state == 'спит':
            state = 'бодр'
        else:
            new_satiety = json_reader[-1]['satiety'] + 15
            new_happiness = json_reader[-1]['happiness'] + 5
            if new_happiness < 100:
                json_data = JsonWriterReader(json_reader[-1]['name'], catparams.age, new_happiness, new_satiety, catparams.get_age_naming())
                json_data.write_into()
            else:
                json_data = JsonWriterReader(name, catparams.age, catparams.happiness, catparams.satiety, catparams.get_age_naming())

    elif select == 'play':
        if state == 'спит':
            state = 'бодр'
        else:
            new_satiety = json_reader[-1]['satiety'] - 10
            new_happiness = json_reader[-1]['happiness'] + 15
            if new_happiness < 100:
                json_data = JsonWriterReader(json_reader[-1]['name'], catparams.age, new_happiness, new_satiety, catparams.get_age_naming())
                json_data.write_into()
            else:
                json_data = JsonWriterReader(name, catparams.age, catparams.happiness, catparams.satiety, catparams.get_age_naming())

    elif select == 'sleep':
        state = 'спит'
        json_data = JsonWriterReader(name, catparams.age, catparams.happiness, catparams.satiety, catparams.get_age_naming())
        json_data.write_into()

    if json_reader[-1]['happiness'] < 10:
        mood = 'очень злой'
    elif json_reader[-1]['happiness'] > 10 and json_reader[-1]['happiness'] < 30:
        mood = 'злой'
    elif json_reader[-1]['happiness'] > 30 and json_reader[-1]['happiness'] < 70:
        mood = 'хорошее настроение'
    elif json_reader[-1]['happiness'] > 70:
        mood = 'отличное настроение'

    img = ''
    if state == 'спит':
        img = "../static/img/sleep.jpg"
    else:
        if mood == 'очень злой':
            img = "../static/img/very_angry.jpg"
        elif mood == 'злой':
            img = "../static/img/angry.jpg"
        elif mood == 'хорошее настроение':
            img = "../static/img/normal.jpg"
        else:
            img = "../static/img/happy.jpg"

    return render(request, 'cat_stat.html', context={
        'name': json_reader[-1]['name'],
        'age': json_reader[-1]['age'],
        'happiness': json_reader[-1]['happiness'],
        'satiety': json_reader[-1]['satiety'],
        'age_naming': json_reader[-1]['age_naming'],
        'img': img,
        'state': state,
        'mood': mood,
    })
