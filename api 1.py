from http import client
from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'textbook'
app.config['MONGO_URI'] = "mongodb://localhost:27017/textbook"

mongo = PyMongo(app)

@app.route('/books',methods=['GET'])
def get_all_result():
    books = mongo.db.books
    grade = "Grade " + request.args['grade']
    subject =  request.args['subject']
    board = request.args['board']



    output = []
    #if all theree parameters are passed
    if(len(subject)!=0 and len(board) != 0):
        for b in books.find({"$and":[{"book_subject": subject},{"book_grade": grade},{"book_board": board}]}):
            output.append({'book_name': b["book_name"], 'book_board': b["book_board"], 'book_grade' : b["book_grade"], 'book_subject': b["book_subject"],  'book_id': b["book_id"], 'book_cover': b["book_cover"], 'book_rank': b["book_rank"] })

    #if board and grade is passed
    elif(len(subject)==0 and len(board) != 0):
        for b in books.find({"$and":[{"book_grade": grade},{"book_board": board}]}):
            output.append({'book_name': b["book_name"], 'book_board': b["book_board"], 'book_grade' : b["book_grade"], 'book_subject': b["book_subject"],  'book_id': b["book_id"], 'book_cover': b["book_cover"], 'book_rank': b["book_rank"] })

    #if subject and grade is passed
    elif(len(subject)!=0 and len(board) != 0):
        for b in books.find({"$and":[{"book_subject": subject},{"book_grade": grade}]}):
            output.append({'book_name': b["book_name"], 'book_board': b["book_board"], 'book_grade' : b["book_grade"], 'book_subject': b["book_subject"],  'book_id': b["book_id"], 'book_cover': b["book_cover"], 'book_rank': b["book_rank"] })

    #if only grade is passed                        
    else:
        for b in books.find({"book_grade": grade}):
            output.append({'book_name': b["book_name"], 'book_board': b["book_board"], 'book_grade' : b["book_grade"], 'book_subject': b["book_subject"],  'book_id': b["book_id"], 'book_cover': b["book_cover"], 'book_rank': b["book_rank"] })
            
    


    return make_response(jsonify({'books' : output}))



if __name__ =='__main__':
    app.run(debug=True)
    


