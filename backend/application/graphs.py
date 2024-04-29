import matplotlib.pyplot as plt
from .models import *
from .timestamps import *
from wordcloud import WordCloud

def plotGraph():
    userbooks = user_books.query.all()
    genres = Genre.query.all()
    names = []
    genres = []
    authors = []
    
    if len(userbooks) >= 1:
        for ub in userbooks:
            book = Books.query.filter_by(id = ub.book_id).first()
            names.append(book.name)
            genres.append(book.genre_name)
            authors.append(book.author)
        genre_dict = dict(zip(names, genres))
        author_dict = dict(zip(names, authors))
          
        genre_counts = {}
        for genres in genre_dict.values():
            if genres in genre_counts:
                genre_counts[genres] += 1
            else:
                genre_counts[genres] = 1

        author_counts = {}
        for authors in author_dict.values():
            if authors in author_counts:
                author_counts[authors] += 1
            else:
                author_counts[authors] = 1    
        
        genre_names = list(genre_counts.keys())
        genre_values = list(genre_counts.values())

        plt.figure(figsize=(4, 4))
        plt.bar(genre_names, genre_values)
        plt.xlabel("Genre")
        plt.ylabel("Number of Books")
        plt.title("Book Genres Distribution Among Users")
        plt.xticks(rotation=45, ha='right') 
        filenamePath = "static/images/graphs1_"
        plt.savefig(filenamePath, bbox_inches='tight', dpi=100)
        plt.close()
        
        plt.figure(figsize=(4, 4))
        plt.pie(genre_values, labels=genre_names, autopct="%1.1f%%", startangle=140)
        plt.title("Book Genres Distribution (Pie Chart) Among Users")
        plt.axis('equal')  
        plt.tight_layout()
        filenamePath = "static/images/graphs2_"
        plt.savefig(filenamePath + ".png", bbox_inches='tight', dpi=100)    
        plt.close()
        
        wordcloud = WordCloud(width=800, height=600, background_color='white')
        
        combined_counts = {}
        for genre, frequency in genre_counts.items():
            combined_counts[genre] = combined_counts.get(genre, 0) + frequency
        
        for author, frequency in author_counts.items():
            combined_counts[author] = combined_counts.get(author, 0) + frequency

        wordcloud.generate_from_frequencies(combined_counts)

        plt.figure(figsize=(4, 4))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.title("Book Genres & Author Word Cloud")
        filenamePath = "static/images/graphs3_"
        plt.savefig(filenamePath + ".png", bbox_inches='tight')
        plt.close()
        
        pathstoReturn = []
        for i in [1,2,3]:
            pathstoReturn.append(f"static/images/graphs{i}_" + ".png")
            
        return pathstoReturn

    else:
        return "NOBOOKS"
        