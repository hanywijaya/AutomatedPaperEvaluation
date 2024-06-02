from Database import Database
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

class Article:
    def __init__(self):
        self.conn = Database().conn
        self.data = None

    def getOne(self, essayId):
        self.data = []
        data = self.conn.execute("SELECT * FROM essay where id = ?", (essayId,)).fetchone()
        self.conn.close()
        return data
    
    def getAll(self,id):
        self.data = []
        data = self.conn.execute("SELECT * FROM essay WHERE userId = ?", (id,)).fetchall()
        self.conn.close()
        return data 
    
    def getAll2(self):
        self.data = []
        data = self.conn.execute("SELECT * FROM essay").fetchall()
        self.conn.close()
        return data

    def insert(self, essayInput, userID, score1, score2):
        conn = get_db_connection()
        # cursor = conn.cursor()
        print("SCORES = " , score1  , score2)
        str_score1 = str(score1)
        str_score2 = str(score2)
        conn.execute('INSERT INTO essay (content, userID, scoreFocusnPurpose, ideasnDevelopment) VALUES (?, ?, ?, ?)',
                       (essayInput, userID, str_score1, str_score2))
        
        lastId = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        print(lastId)
        
        conn.commit()
        conn.close()

        return lastId

    def updateEssay(self, id, newEssay, newScore1, newScore2):
        conn = get_db_connection()
        
        str_score1 = str(newScore1)
        str_score2 = str(newScore2)
        conn.execute('UPDATE essay SET content = ?, scoreFocusnPurpose = ?, ideasnDevelopment = ? WHERE id = ?',
                        (newEssay, str_score1, str_score2, id))
        
        conn.commit()
        conn.close()

    def getDesc1(self, score):
        desc1 = [
            "Please input your essay.",
            "Complete confusion about the topic or inability to grasp the idea of the task; lack of purpose.",
            "Ideas are limited showing sign of confusion, misunderstanding on the prompt.",
            "Mostly simplistic essay, signs of confusion, little and no sense of purpose that control the topic.",
            "Mostly intelligble purposes, unclear objective.",
            "Competent and well-developed purposes, shows adequate understanding of the topic.",
            "Full development of clear purposes to the topics chosen, answers corretcly what the instruction asks."
        ]

        return desc1[score]
    
    def getDesc2(self, score):
        desc2 = [
            "Please input your essay.",
            "Clear absence of support for the essay.",
            "Lack of support for main ideas, and/or illogical development of the essay.",
            "Insufficient ideas development, irrelevant response to the task given.",
            "Main points and ideas are only indirectly supported with reasoning; support isn't sufficient or specific, but is loosely relevant to the main points.",
            "Ideas supported sufficiently; support is sound, valid, and logical.",
            "Consistent evidence with iriginality and depth; all ideas work together as a unified whole, main points are sufficiently supported with reasons."
        ]

        return desc2[score]

