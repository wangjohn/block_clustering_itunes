from operator import attrgetter

class MaxBlockCover:
    def __init__(self, hash_of_blocks):
        self.blocks = hash_of_blocks

    # the current algorithm is an 2-approximation. Not going to do any better than this because the problem is NP-hard.
    def get_max_covering(self):
        # first sort the blocks by their heuristic score
        sorted_indices = self.blocks.keys()
        sorted_indices.sort()
        output = []

        # now get the set of blocks with a high total score 
        for indices in sorted_indices:
            (new_i, new_j) = indices
            should_append = True
            for output_block in output:
                (old_i, old_j) = output_block.indices
                # if the new block doesn't intersect with the old ones, append it
                if ((new_i >= old_i and new_j <= old_j) or (new_i >= old_i and new_i <= old_j) or (new_j <= old_j and new_j >= old_i)):
                    should_append = False
                    break
            if should_append:
                output.append(self.blocks[indices])
        return output

