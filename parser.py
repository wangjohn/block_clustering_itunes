from urlparse import urlparse

class Parser:
    def __init__(self, description):
        self.description = description

    def calculate_likely_blocks(self):
        self.description



class Tokens:
    def __init__(self, list_of_tokens=[]):
        self.tokens = {}
        for token in list_of_tokens:
            self.tokens[token] = 


class LineOfText:
    def __init__(self, line):
        self.line = line

class Fitness:
    def __init__(self, sub_description):
        self.text = sub_description

    def check_first_n_letters(self, n):
        first_letters = {}
        numbers_score = 0
        for line in self.text:
            current_letters = line[0:n+1]
            
            # check if the first letters of each line are the same (for lists)
            if current_letters in first_letters:
                first_letters[current_letters] += 1
            else:
                first_letters[current_letters] = 1

            # check if the first letters of each line are numbers
            if re.match('^\d+'):
                numbers_score += 1
        best_letters = None
        for key, value in first_letters.iteritems():
            if best_letters == None or value > best_letters[1]:
                best_letters = (key, value)
        current_max_score = max(best_letters[1], numbers_score)
        return current_max_score
        
    def check_double_line_break(self, line1, line2):
        if line1
        # implement a check for \n\n
        return False

    def check_for_url(self):
        result = re.findall("(https?://|ftp://)?(www.)(.*?)(.com|.net|.io)", self.text)
        if result:
            return len(result)
        else:
            return False

    def check_if_title(self, first_line):
        # check if this is a title
        strict_title = re.match("^(.*):\s*$", first_line)
        first_inline_title = re.match("^(.*):\s*", first_line) 
        any_inline_title = re.match("\s?(.*):\s*", first_line)
        
        # look at different stages of being a title. Can be a strict title
        # where colon ends the line, and various subsets of being a title
        final_result = 0
        if strict_title:
            final_result += 10
        elif first_inline_title:
            final_result += 5
        elif first_inline_title:
            final_result += 1
        return final_result 

    def dp_get_fitness(self):
        num_lines = len(self.text)

        title_scores = []          # get the line indices of the probable titles
        double_line_breaks = []    # get the line indices of where \n\n happens
        for i in xrange(num_lines):
            score = self.check_if_title(self.text[i])
            if score >= 10:
                # if this is a title, append it to the list
                title_scores.append(i)
            if i > 1:
                # if this is a double line break, append it to the list
                result = self.check_double_line_break(self.text[i-1], self.text[i])
                if result:
                    double_line_breaks.append(i)

        # we will assume that a block starts at the first line.
        block_indices = []
        for i in xrange(len(double_line_breaks)):
            current_dlb = double_line_breaks[i]
            if not block_indices:
                block_indices.append((0, current_dlb))
            else:
                block_indices.append((double_line_breaks[i-1], current_dlb))

    
