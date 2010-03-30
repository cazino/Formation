

def change_lines(raw_string):
    """
    Remove endline chars and insert new one every 100~120 chars
    """
    def split_recursive(cleaned_string):
        if len(cleaned_string) <= 120:
            return cleaned_string
        index = cleaned_string.rfind(' ', 0, 120)
        return cleaned_string[0:index] + '\n' + split_recursive(cleaned_string[index + 1:len(cleaned_string)])            
    return split_recursive(raw_string.replace("\n", " ").replace('\r', ' '))
    
    
    
