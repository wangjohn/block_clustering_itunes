class MaxBlockCover:
    def __init__(self, list_of_blocks):
        self.blocks = list_of_blocks

    # the current algorithm is an 2-approximation. Not going to do any better than this because the problem is NP-hard.
    def get_max_covering(self, max_index=None):
        # first sort the blocks by their heuristic score
        sorted_blocks = sorted(self.blocks, attrgetter('score'))
        output = []

        # now get the set of blocks with a high total score 
        for block in sorted_blocks:
            (new_i, new_j) = block.indices
            should_append = True
            for output_block in output:
                (old_i, old_j) = output_block.indices
                # if the new block doesn't intersect with the old ones, append it
                if not ((new_i >= old_i and new_j <= old_j) or (new_i >= old_i and new_i <= old_j) or (new_j <= old_j and new_i <= new_j)):
                    should_append = False
                    break
            if should_append:
                output.append(block)
        return output

