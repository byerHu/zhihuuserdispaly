from flask import Flask,jsonify, request, abort,url_for,redirect
from flask import render_template
import pymongo
app = Flask(__name__)
mongo = pymongo.MongoClient('127.0.0.1', 27017)
db = mongo.haha

@app.route('/')
def index():
    datas = db.user.find()
    todos = []
    count = 0
    for data in datas:
        # print(data["locations"])
        # print(data["employments"])
        todos.append(data)
        count += 1
    return render_template('index.html', todos = todos, count = count)

@app.route('/info')
def info():
    datas = db.user.find()
    todos = []
    count = 0
    edus = []
    locs = []
    for data in datas:
        todos.append(data)
        if len(data['educations']) != 0:
            edus.append(data['educations'])
        if len(data['locations']) != 0:
            locs.append(data['locations'])
        count += 1
    locations = {}
    keys3 = []
    for loc in locs:
        if "name" in loc[0]:
            keys3.append(str(loc[0]["name"]).replace('\n', ""))
    key4 = set(keys3)
    for key in key4:
        locations[key] = 0
    for i in keys3:
        if i in key4:
            locations[i] += 1

    schools = {}
    keys = []
    for edu in edus:
        if "school" in edu[0]:
            keys.append(edu[0]["school"]["name"])
    keys2 = set(keys)
    for key in keys2:
        schools[key] = 0
    for i in keys:
        if i in keys2:
            schools[i] += 1


    # 查询articles_count前十的用户
    datas2 = db.user.find().sort([('follower_count', -1)]).limit(10)
    follower_tops = []
    for data in datas2:
        follower_tops.append(data)

    # 解答数量前十的用户
    data3 = db.user.find().sort([('answer_count', -1)]).limit(10)
    answer_tops = []
    for data in data3:
        answer_tops.append(data)
    # 文章数量前十的用户
    data4 = db.user.find().sort([('articles_count', -1)]).limit(10)
    article_tops = []
    for data in data4:
        article_tops.append(data)
    # 专栏数量前十用户
    data5 = db.user.find().sort([('columns_count', -1)]).limit(10)
    column_tops = []
    for data in data5:
        column_tops.append(data)
    # Live数量前十用户
    data6 = db.user.find().sort([('participated_live_count', -1)]).limit(10)
    live_tops = []
    for data in data6:
        live_tops.append(data)

    return render_template('info.html', todos=todos, follower_tops=follower_tops, answer_tops=answer_tops,
                           article_tops=article_tops, column_tops=column_tops, live_tops=live_tops, schools=schools, locations = locations,count=count)

if __name__ == '__main__':
    app.run(debug=True)
