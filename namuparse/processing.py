from namuwiki.extractor import extract_text
from namuparse.onmark import onmarkParse

class Processing:
    def __init__(self, string: str):
        self.string = string
    
    def __str__(self):
        return self.string

    def preprocessing(self) -> None:
        self.string = onmarkParse.replace_macros(None, self.string)
        self.string = onmarkParse.process_table(None, self.string)

    def processing(string: str) -> str:
        proc: Processing = Processing(string)
        proc.preprocessing()
        return extract_text(proc.string)

if __name__ == '__main__':
    string = open('in.in', encoding='utf-8').read()
    print(Processing.processing(string)[:20])