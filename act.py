from flask import Flask, render_template, jsonify, request, redirect, send_file
import json
import base64
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/api/v1/acts',methods=['POST'])
def upload_act():
    if request.method!='POST':
        return jsonify({}),405
    try:
        r=request.get_json()
        actId=r['actId']
        username=r['username']
        caption=r['caption']
        name=r['name']
        imgB64=r['imgB64']
        timestamp=r['timestamp']
        vote=0
    except:
        pass

    try:
        username=request.form['username']
        actId=request.form['actId']
        caption=request.form['caption']
        name=request.form['name']
        imgB64=request.form['imgB64']
        timestamp=request.form['timestamp']
        vote=0
    except:
        pass

    with open('acts.txt') as acts_file:
        data=json.load(acts_file)
    for i in data:
        if(i["actId"]==actId):
            return jsonify({}),400
    image_data=imgB64[10:-2]
    image_list=image_data.split(',')
    imgstr=image_list[1]
    #img_extension=image_list[0].split(';')[0].split('/')[1]
    #print(img_extension)

    with open("images/"+str(actId),"wb") as f:
        try:
            image_data=base64.b64decode(imgstr)
        except:
            return jsonify('Failed base64'),400
        f.write(image_data)

    with open('categories.txt','r') as categories_file:
        data=json.load(categories_file)
    if actId not in data[name]:
        data[name].append(actId)
	
    with open('categories.txt','w') as categories_file:
        json.dump(data,categories_file)
    
    with open('acts.txt','r') as acts_file:
        acts_old_data=json.load(acts_file)
    
    dicti={}
    dicti['actId']=actId
    dicti['username']=username
    dicti['caption']=caption
    dicti['imgB64']=imgB64
    dicti['vote']=vote
    dicti['timestamp']=timestamp
    acts_old_data.append(dicti)
    acts_new_data=acts_old_data
    with open('acts.txt','w') as acts_file:
        json.dump(acts_new_data,acts_file)

    return jsonify({}),201

@app.route('/api/v1/categories/<name>/acts/size',methods=['GET'])
def acts_size(name):
    if request.method!='GET':
        return jsonify({}),405
    with open('categories.txt','r') as categories_file:
        data=json.load(categories_file)
    if len(data[name])==0:
        return jsonify({}),204
    l=len(data[name])
    
    return jsonify({"Length":l}),200

@app.route('/api/v1/categories/<name>/acts',methods=['GET'])
def acts_size_less_than_500(name):
    if request.method!='GET':
        return jsonify({}),405
    #try:
    #    startRange = request.args.get('start')
    #    endRange = request.args.get('end')
    #    with open('categories.txt','r') as categories_file:
    #       data=json.load(categories_file)  
    #    acts=[]  
    #    l=data[name]
    #    if(endRange>len(l)):
    #        return jsonify({}),400

    #    for i in range(startRange,endRange+1):
    #        acts.append(l[i])
    #        return jsonify({"Range of Acts":acts}),200
    #except:
    #    pass


    with open('categories.txt','r') as categories_file:
        data=json.load(categories_file)
    l=data[name]
    a=[]
    acts=[]
    if(len(l)==0):
        return jsonify({}),204
    if(len(l)>=500):
        return jsonify({}),413
    for i in l:
        acts.append(i)

    for i in acts:
        with open('acts.txt','r') as users_file:
            data=json.load(users_file)
        for j in data:
            if j["actId"]==i:
                a.append(j)
    return jsonify({"Acts":a}),200

@app.route('/api/v1/acts/upvote',methods=['POST'])
def upvote():
   # if request.method!='POST':
        #return jsonify({}),405
    try:
        actId=request.form['actId']
        print(actId)
        #username=request.form['username']
    except:
        pass
    try:
        r=request.get_json()
        actId=r['actId']
    except:
        pass
    #alert("kk")
    print ("Name;",actId)
    with open('acts.txt','r') as acts_file:
        data=json.load(acts_file)
    flag=0
    for i in data:
        if(i["actId"]==actId):
            flag=1
            print i
            i['vote']=i['vote']+1
            break
    if(flag==0): 
        return jsonify("Failed to Upvote"),400
    
    with open('acts.txt','w') as acts_file:
        json.dump(data,acts_file)
    return jsonify({}),200


@app.route('/api/v1/categories/<name>/acts?start=<startRange>&end=<endRange>',methods=['GET'])
def range_acts(name,startRange,endRange):
    if request.method!='GET':
        return jsonify({}),405
    with open('categories.txt','r') as categories_file:
        data=json.load(categories_file)  
    a=[]
    flag=0
    for i in data.keys():
        if i==name:
            flag=1
    if flag==0:
        return jsonify({}),204
    acts=[]  
    l=data[name]
    if(endRange>len(l)):
        return jsonify({}),413

    for i in range(startRange,endRange+1):
        acts.append(l[i])

    for i in acts:
        with open('acts.txt','r') as users_file:
            data=json.load(users_file)
        for j in data:
            if j["actId"]==i:
                a.append(j)
            
        return jsonify({"Range of Acts":acts}),201
    
            

@app.route('/api/v1/categories', methods=['POST'])
def add_category():
    if request.method!='POST':
        return jsonfiy({}),405
    try:
        r=request.get_json()
        name=r['name']
    except:
        pass

    try:
        name=request.form['name']

    except:
        pass
        
    new_data=[]
    old_data=[]
    with open('categories.txt') as categories_file:
        old_data=json.load(categories_file)

    for i in old_data.keys():
        if i==name:
            return jsonify({}),400
    
    old_data[name]=[]
    new_data=old_data
    with open('categories.txt','w') as categories_file:
        json.dump(new_data,categories_file)
    return jsonify({}),200


@app.route('/api/v1/categories/<name>', methods=['DELETE'])
def remove_category(name):
    if request.method!='DELETE':
        return jsonify({}),405
    with open('categories.txt') as categories_file:
        old_data=json.load(categories_file)

    flag=0
    for i in old_data.keys():
        if i==name:
            flag=1
    if(flag==0):
        return jsonify({}),400


    del(old_data[name])
    new_data=old_data
            
    with open('categories.txt','w') as categories_file:
        json.dump(new_data,categories_file)

    return jsonify({}),200    


@app.route('/api/v1/acts/<actId>',methods=['DELETE'])
def remove_act(actId):
    if (request.method!='DELETE'):
        return jsonify({}),405

    with open('acts.txt') as acts_file:
        old_data=json.load(acts_file)
    new_data=[]
    flag=0
    for i in old_data:
            if(i["actId"]==actId):
                flag=1
    if(flag==0):
        return jsonify({}),400
    
    for i in old_data:
            if(i["actId"]==actId):
                old_data.remove(i)
    new_data=new_data
    with open('acts.txt','w') as acts_file:
        json.dump(new_data,acts_file)

    return jsonify({}),200





@app.route('/api/v1/categories', methods=['GET'])
def display1_categories():
    if(request.method!='GET'):
        return jsonify({}),405
    with open('categories.txt') as categories_file:
        old_data=json.load(categories_file)
     
    CATEGORIES={}   
    for i in old_data.keys():
        CATEGORIES[i]=len(old_data[i])

    isnotempty = (CATEGORIES and True) or False
    if(isnotempty==False):
        return jsonify({}),204
  
    
    return jsonify({"CATEGORIES":CATEGORIES}),200

#@app.route('/api/v1/categories', methods=['GET'])
#def display_categories():
#    text = open('categories.txt', 'r+')
#    content = text.read()
#    
#    return jsonify({'CATEGORIES':content}),201

@app.route('/get_image/<image_name>')
def get_image(image_name):
    filename = 'images/'+image_name
    return send_file(filename, mimetype='image/gif')

@app.route('/get_caption/<actId>',methods=['GET'])
def get_caption(actId):
    with open ('acts.txt') as acts_file:
        data=json.load(acts_file)
    for i in data:
        if(i["actId"]==actId):
            return ({"l"}),201

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)