def build_trie(word_set):
    # 1. Start with an empty dictionary for the root
    root_node = {}

    for word in word_set:
        current_node = root_node

        for char in word:
            # 2. If the character isn't a child of the current node, add it
            if char not in current_node:
                current_node[char] = {}

            # 3. Move our pointer deeper into the tree
            current_node = current_node[char]

        # 4. After the loop finishes the word, mark it as a valid word
        current_node['_is_word'] = True

    return root_node