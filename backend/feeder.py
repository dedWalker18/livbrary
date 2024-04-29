import requests

def add_data():
    messages_recieved = []
    response = requests.post(" http://127.0.0.1:5000/role/admin")
    messages_recieved.append(response.json())
    response = requests.post(" http://127.0.0.1:5000/role/users")
    messages_recieved.append(response.json())
    data = {
        "name" : "admin",
        "username" : "admin",
        "password" :"admin",
        "email" : "admin@ivbrary.in",
        "roles" : "admin",
        "avatarid" : "0"
    }
    response = requests.post(" http://127.0.0.1:5000/signup", json=data)
    messages_recieved.append(response.json())

    books = [
    {
        "name": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "genre": "Fantasy",
        "location": "/pdfs/HarryPotter1.pdf",
        "cover": "/cover/HarryPotter1.png"
    },
    {
        "name": "Harry Potter and the Chamber of Secrets",
        "author": "J.K. Rowling",
        "genre": "Fantasy",
        "location": "/pdfs/HarryPotter2.pdf",
        "cover": "/cover/HarryPotter2.png"
    },
    {
        "name": "Harry Potter and the Prisoner of Azkaban",
        "author": "J.K. Rowling",
        "genre": "Fantasy",
        "location": "/pdfs/HarryPotter3.pdf",
        "cover": "/cover/HarryPotter3.png"
    },
    {
        "name": "Harry Potter and the Goblet of Fire",
        "author": "J.K. Rowling",
        "genre": "Fantasy",
        "location": "/pdfs/HarryPotter4.pdf",
        "cover": "/cover/HarryPotter4.png"
    },
    {
        "name": "Harry Potter and the Order of the Phoenix",
        "author": "J.K. Rowling",
        "genre": "Fantasy",
        "location": "/pdfs/HarryPotter5.pdf",
        "cover": "/cover/HarryPotter5.png"
    },
    {
        "name": "Harry Potter and the Half-Blood Prince",
        "author": "J.K. Rowling",
        "genre": "Fantasy",
        "location": "/pdfs/HarryPotter6.pdf",
        "cover": "/cover/HarryPotter6.png"
    },
    {
        "name": "Harry Potter and the Deathly Hallows",
        "author": "J.K. Rowling",
        "genre": "Fantasy",
        "location": "/pdfs/HarryPotter7.pdf",
        "cover": "/cover/HarryPotter7.png"
    },
    {
        "name": "Deep Learning Certificate",
        "author": "Coursera",
        "genre": "Accolades",
        "location": "/pdfs/deepLearningCert.pdf",
        "cover": "/cover/deepLearningCert.png"
    },
    {
        "name": "Elements of Programming Interview",
        "author": "Adnan Aziz",
        "genre": "Computer Science",
        "location": "/pdfs/Elements of Programming Interviews.pdf",
        "cover": "/cover/elementf_of_prograaming_interview.png"
    },
    {
        "name": "Final Project Report",
        "author": "Lakshya Ganeriwala",
        "genre": "Accolades",
        "location": "/pdfs/Final Project Report.pdf",
        "cover": "/cover/finalProjectReport.png"
    },
    {
        "name": "Hands-On Machine Learning with Scikit-Learn",
        "author": "Aurelion Geron",
        "genre": "Computer Science",
        "location": "/pdfs/Hands-On Machine Learning with Scikit-Learn and TensorFlow_ Concepts, Tools, and Techniques to Build Intelligent Systems.pdf",
        "cover": "/cover/Hands-On Machine Learning with Scikit-Learn and TensorFlow_ Concepts, Tools, and Techniques to Build Intelligent Systems.png"
    },
    {
        "name": "Pattern Recognition and Machine Learning",
        "author": "Christopher M. Bishop",
        "genre": "Computer Science",
        "location": "/pdfs/Pattern_Recognition_And_Machine_Learning.pdf",
        "cover": "/cover/patterRecognitioninML.png"
    }

    ]
    
    response = requests.post(" http://127.0.0.1:5000/loginuser", json=data)
    response = response.json()
    token = response["token"]
    messages_recieved.append(token)
    
    for book in books:
        response = requests.post(" http://127.0.0.1:5000/books", json=book, headers={
            "Authorization" : "Bearer " + token
        })
        messages_recieved.append(response.json())
    
    data = {
        "name" : "lakshya",
        "username" : "test",
        "password" :"asdf",
        "email" : "lakshya@livbrary.in",
        "roles" : "users",
        "avatarid" : "4"
    }
    response = requests.post(" http://127.0.0.1:5000/signup", json=data)
    messages_recieved.append(response.json())
    
    [print(messages) for messages in messages_recieved]
    

add_data()

# "Pride and Prejudice" by Jane Austen
# "Frankenstein" by Mary Shelley
# "Moby-Dick" by Herman Melville
# "Alice's Adventures in Wonderland" by Lewis Carroll
# "The Adventures of Sherlock Holmes" by Arthur Conan Doyle
# Science Fiction:
# "The War of the Worlds" by H.G. Wells
# "Flatland: A Romance of Many Dimensions" by Edwin A. Abbott
# "The Time Machine" by H.G. Wells
# "The Lost World" by Arthur Conan Doyle
# Comedy:
# "The Importance of Being Earnest" by Oscar Wilde
# "Three Men in a Boat" by Jerome K. Jerome
# Drama:
# "Hamlet" by William Shakespeare
# "A Doll's House" by Henrik Ibsen
# Historical:
# "The Art of War" by Sun Tzu
# "The Federalist Papers" by Alexander Hamilton, James Madison, and John Jay
# Biographies:
# "The Life of Samuel Johnson" by James Boswell
# "Autobiography of Benjamin Franklin" by Benjamin Franklin
# Philosophy:
# "Meditations" by Marcus Aurelius
# "Thus Spoke Zarathustra" by Friedrich Nietzsche
# Political Satire:
# "Gulliver's Travels" by Jonathan Swift
# "Animal Farm" by George Orwell
# Self-Help:
# "As a Man Thinketh" by James Allen
# "The Prophet" by Kahlil Gibran
# Mathematics:
# "Euclid's Elements" by Euclid
# "Flatland: A Romance of Many Dimensions" by Edwin A. Abbott (also listed under science fiction)
# Computer Science:
# "The Art of Computer Programming" by Donald E. Knuth
# "Structure and Interpretation of Computer Programs" by Harold Abelson and Gerald Jay Sussman