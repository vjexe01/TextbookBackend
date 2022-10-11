from http import client
from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
import time

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'textbook'
app.config['MONGO_URI'] = "mongodb://localhost:27017/textbook"

mongo = PyMongo(app)


#custom function to convert dict into json
def to_json(self):
    return{
    "book_board" : self["book_board"],  
    "book_grade" : self["book_grade"],  
    "book_subject" : self["book_subject"], 
    "book_name" : self["book_name"], 
    "book_id" : self["book_id"],  
    "book_cover" : self["book_cover"],  
    "book_rank" : self["book_rank"]
    }




@app.route('/books',methods=['GET'])
def get_all_result():
    sttime = time.time()
    books = mongo.db.books
    grade = "Grade " + request.args['grade']
    subject =  request.args['subject']
    board = request.args['board']


    output = []
    #if all theree parameters are passed
    if(len(subject)!=0 and len(board) != 0):
        for b in books.find({"book_subject": subject,"book_grade": grade,"book_board": board}):
            output.append(to_json(b))
           
    #if board and grade is passed
    elif(len(subject)==0 and len(board) != 0):
        for b in books.find({"book_grade": grade,"book_board": board}):
            output.append(to_json(b))

    #if subject and grade is passed
    elif(len(subject)!=0 and len(board) == 0):
        for b in books.find({"book_subject": subject,"book_grade": grade}):
            output.append(to_json(b))

    #if only grade is passed                        
    else:
        for b in books.find({"book_grade": grade}):
            output.append(to_json(b))


    #calculate the time taken to search in the database        
    endtime = time.time()
    time_taken = (endtime-sttime)


    #to insert the log
    log = {
        'grade' : grade,
        'subject': subject,
        'board' : board,
        'time_taken' : time_taken,
    }
    inserted_id = mongo.db.Logs.insert_one(log).inserted_id

    return make_response(jsonify({'Books' : output}))


@app.route('/book-search',methods=['GET'])
def search_result():
    sttime = time.time()
    books = mongo.db.books
    grade = "Grade " + request.args['grade']
    subject =  request.args['subject']
    board = request.args['board']
    query = request.args['query']


    output = []
    #if all theree parameters are passed
    if(len(subject)!=0 and len(board) != 0):
        for b in books.find({"book_subject": subject,"book_grade": grade,"book_board": board}):
            output.append(to_json(b))
           
    #if board and grade is passed
    elif(len(subject)==0 and len(board) != 0):
        for b in books.find({"book_grade": grade,"book_board": board}):
            output.append(to_json(b))

    #if subject and grade is passed
    elif(len(subject)!=0 and len(board) == 0):
        for b in books.find({"book_subject": subject,"book_grade": grade}):
            output.append(to_json(b))

    #if only grade is passed                        
    else:
        for b in books.find({"book_grade": grade}):
            output.append(to_json(b))
    
    result = []

    for entry in output:
        if entry['book_name'] == query:
            result = entry
            break

    #calculate the time taken to search in the database        
    endtime = time.time()
    time_taken = (endtime-sttime)


    #to insert the log
    log = {
        'grade' : grade,
        'subject': subject,
        'board' : board,
        'time_taken' : time_taken,
        'query' : query
    }
    inserted_id = mongo.db.Logs.insert_one(log).inserted_id

    return make_response(jsonify({'books' : result}))


if __name__ =='__main__':
    app.run(debug=True,port=3005)
    


