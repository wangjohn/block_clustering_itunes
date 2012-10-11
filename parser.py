from parameters import * 
import re

class Fitness:
    def __init__(self, description, params = Parameters()):
        lines = description.split('\n')
        self.text = lines
        self.potential_blocks = {}
        self.parameters = params

    def check_first_n_letters(self, n):
        list_indices = []
        for i in xrange(len(self.text)):
            line = self.text[i]
            current_letters = line[0:n+1]

            new_block_indices = (i,i)
            for j in xrange(self.parameters.list_spacing, 0, -1):
                previous_letters = self.text[i-j][0:n+1]
                if previous_letters == current_letters:
                    new_block_indices = (i,j)

            # add these indices to the list_indices if we've potentially found a list
            if new_block_indices[0] != new_block_indices[1]:
                if list_indices and list_indices[-1][1] < new_block_indices[0]:
                    list_indices.append(new_block_indices)
                elif list_indices and list_indices[-1][1] >= new_block_indices[0]:
                    # if we intersect with the last block, then we merge them together into a single block
                    last_block_indices = list_indices.pop()
                    list_indices.append((last_block_indices[0], new_block_indices[1]))
        # create the blocks based on the list indices that we just found
        new_block_list = []
        for indices in list_indices:
            new_block = Block(indices, self.text[indices[0]:indices[1]+1])
            length = indices[1] - indices[0]
            list_score = length*self.parameters.list_length_weight + n*1.5
            new_block.set_subscore('list', list_score)
            new_block_list.append(new_block)

        return new_block_list

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

    def get_potential_blocks(self):
        num_lines = len(self.text)

        title_indices = []          # get the line indices of the probable titles
        double_line_breaks = []    # get the line indices of where \n\n happens
        for i in xrange(num_lines):
            # if this is a title, append it to the list
            score = self.check_if_title(self.text[i])
            title_indices.append((i, score))

            # if this is a double line break, append it to the list
            result = self.check_double_line_break(self.text[i])
            if result:
                double_line_breaks.append(i)

        # we will assume that a block starts at the first line.
        for i in xrange(len(double_line_breaks)):
            current_dlb = double_line_breaks[i]
            if i == 0:
		        indices = (0, current_dlb)
            else:
                indices = (double_line_breaks[i-1]+1, current_dlb)
            new_block = Block(indices, self.text[indices[0]:indices[1]+1])
            new_block.set_subscore('double_line_break', self.parameters.double_line_break_score)
            self.potential_blocks[indices] = new_block

        # we will use titles to check whether these blocks are reasonable
        self.num_titles_per_block(title_indices, self.potential_blocks)
        
        # check if we can merge any of these blocks into a list block
        for j in xrange(1, 3, 1):
            new_potential_blocks = self.check_first_n_letters(j)


    def num_titles_per_block(self, title_indices, blocks_hash):
        block_indices = blocks_hash.keys()
        block_indices.sort()
        block_counter = 0
        current_block = block_indices[block_counter]
        for (title_position, title_score) in title_indices:
            while title_position > current_block[1] and block_counter < len(block_indices) - 1:
                block_counter += 1
                current_block = block_indices[block_counter]
            score = 0
            if title_position <= current_block[1] and title_position >= current_block[0]:
                # basically, we scale the score by how close the title is to the top of the block.
                if current_block[1] - current_block[0] == 0:
                    score = title_score
                else:
                    score = title_score*(float(current_block[1] - title_position) / (current_block[1] - current_block[0]))
		    block_object = blocks_hash[current_block]
		    block_object.set_subscore('title', score)


class Block:
    def __init__(self, indices, text):
        self.indices = indices
        self.text = text

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

    def merge_scores(self, other_block):
        self.title_score = max(self.title_score, other_block.title_score)
        self.double_line_break_score = max(self.double_line_break_score, other_block.double_line_break_score)
        self.list_score = max(self.list_score, other_block.list_score)
        self.url_score = max(self.url_score, other_block.url_score)
        self.recompute_score()

    def __hash__(self):
        return hash(self.indices)

    def __str__(self):
        return str(self.indices) + ":\n" + '\n'.join(self.text)

    def recompute_score(self):
        self.score = self.double_line_break_score + self.title_score	
# if block has both list and url elements, then something went wrong and we should penalize for that
        if self.list_score and self.url_score:
            self.score -= self.parameters.list_url_collision_penalty 
        else:
            if self.list_score:
                self.score += self.list_score
            if self.url_score:
                self.score += self.url_score
	
    def set_subscore(self, score_type, score):
        locals()[self.score_hash[score_type]] = score
        self.recompute_score()
                 
