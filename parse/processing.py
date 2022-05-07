from namuwiki.extractor import extract_text
from parser import onmark_parse

class Processing:
    def __init__(self, string: str):
        self.string = string
    
    def __str__(self):
        return self.string

    def preprocessing(self) -> None:
        self.string = onmark_parse.replace_macros(None, self.string)

    def processing(string: str) -> list[str]:
        proc: Processing = Processing(string)
        proc.preprocessing()
        return extract_text(proc.string).split('\n')

if __name__ == '__main__':
    string = open('in.in', encoding='utf-8').read()
    print(Processing.processing(string)[:20])