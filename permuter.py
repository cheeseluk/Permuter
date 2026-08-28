def trie_permuter(string, current_trie_node):
    # Base Case: Last character remaining

    if not string:
        return

    seen_characters = set()

    for i in range(len(string)):
        current_char = string[i]

        # Skip duplicate characters in the string to avoid duplicate permutations
        if current_char in seen_characters and current_char != "?":
            continue

        seen_characters.add(current_char)

        #Wild Card
        if current_char == "?":
            available_chars = [key for key in current_trie_node.keys() if key!= '_is_word']

            for wild_char in available_chars:
                next_trie_node = current_trie_node[wild_char]

                if next_trie_node.get('_is_word'):
                    yield wild_char

                remaining_chars = string[:i] + string[i+1:]
                for sub_permutations in trie_permuter(remaining_chars, next_trie_node):
                    yield wild_char + sub_permutations

        #  proceed if this character path exists in our Trie
        elif current_char in current_trie_node:
            next_trie_node = current_trie_node[current_char]

            if next_trie_node.get('_is_word'):
                yield current_char

            remaining_chars = string[:i] + string[i+1:]

            # Recurse down the tree
            for sub_permutations in trie_permuter(remaining_chars, next_trie_node):
                yield current_char + sub_permutations
