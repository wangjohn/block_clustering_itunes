from urlparse import urlparse

class Parser:
    def __init__(self, description):
        self.description = description

    def calculate_likely_blocks(self):
        self.description

class LineOfText:
    def __init__(self, line):
        self.line = line

class Fitness:
    def __init__(self, description):
        lines = description.split('\n')
        self.text = lines
	    self.potential_blocks = {}

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
        
    def check_double_line_break(self, line):
        # once we split up the text into lines by \n, we should have a line with nothing inside
        # if we have a \n\n anywhere in the text
        if line.strip():
            return False
        return True

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
            final_result = self.parameters.strict_title_points
        elif first_inline_title:
            final_result = self.parameters.first_inline_title_points
        elif any_inline_title:
            final_result = self.parameters.any_inline_title_points
        return final_result 

    def dp_get_fitness(self):
        num_lines = len(self.text)

        title_indices = []          # get the line indices of the probable titles
        double_line_breaks = []    # get the line indices of where \n\n happens
        for i in xrange(num_lines):
            score = self.check_if_title(self.text[i])
            if score >= self.parameters.title_score_threshold:
                # if this is a title, append it to the list
                title_indices.append(i)
            if i > 1:
                # if this is a double line break, append it to the list
                result = self.check_double_line_break(self.text[i])
                if result:
                    double_line_breaks.append(i)

        # we will assume that a block starts at the first line.
        for i in xrange(len(double_line_breaks)):
            current_dlb = double_line_breaks[i]
            if not block_indices:
		indices = (0, current_dlb)
            else:
		indices = (double_line_breaks[i-1]+1, current_dlb)
		new_block = Block(indices)
		new_block.set_subscore('double_line_break', self.parameters.double_line_break_score)
		self.potential_blocks[indices] = new_block

        # we will use titles to check whether these blocks are reasonable
        self.num_titles_per_block(title_indices, self.potential_blocks)

    def num_titles_per_block(title_indices, blocks_hash):
        block_indices = blocks_hash.keys.sort()
        block_counter = 0
        current_block = block_indices[block_counter]
        for title_position in title_indices:
            while title_position > current_block[1]:
                block_counter += 1
                current_block = block_indices[block_counter]
            if title_position <= current_block[1] and title_position >= current_block[0]:
                score = float(current_block[1] - title_position) / current_block[0]
		block_object = blocks_hash[current_block]
		block_object.set_subscore('title', self.parameters.title_score)


class Block:
	def __init__(self, indices):
		self.indices = indices
		self.score = None
		self.title_score = 0 
		self.double_line_break_score = 0
		self.list_score = None
		self.url_score = None
		self.score_hash = {
			'title': 'self.title_score',
			'double_line_break': 'self.double_line_break_score',
			'list': 'self.list_score',
			'url': 'self.url_score',
		}

	def __hash__(self):
		return hash(self.indices)

	def recompute_score(self):
		self.score = self.double_line_break_score + self.title_score	
		if self.list_score and self.url_score:
			self.score -= self.parameters.list_url_collision_penalty 
	
	def set_subscore(self, score_type, score):
		eval(self.score_hash[score_type] + "=" + str(score))
		self.recompute_score()
                 
