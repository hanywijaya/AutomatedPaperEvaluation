from Models.Article import Article

# class web
class Web:
    def __init__(self):
        self.article = Article()
        self.calc = Calculate()

    def home(self):
        # this is text to render
        # ambil data dari database
        return self.article.getAll()

    def register(self):
        pass

    def result(self):
        return self.calc.get_res()

class Calculate:
    def __init__(self) -> None:
        self.model = None

    def get_res(self):
        # dummy data
                # this will be used to handle result data to template of result
        focus = 0
        ideas = 0

        res = {
            "focus":focus,
            "ideas":ideas 
        }
        return res