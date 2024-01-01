def load_index(index_file):
    index = {}
    with open(index_file, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            term_line = lines[i].strip()
            if term_line.startswith('Term:'):
                term_parts = term_line.split(': ')
                if len(term_parts) > 1:
                    current_term = term_parts[1]
                    index[current_term] = {'doc_freq': 0, 'postings': {}}
                    i += 1  # Move to the next line
                    while i < len(lines) and not lines[i].startswith('Term:'):
                        if lines[i].startswith('DocID:'):
                            doc_parts = lines[i].split(', Positions: ')
                            if len(doc_parts) > 1:
                                doc_id = int(doc_parts[0].split(': ')[1])
                                positions = list(map(int, doc_parts[1].strip().strip('][').split(', ')))
                                index[current_term]['doc_freq'] += 1
                                index[current_term]['postings'][doc_id] = positions
                        i += 1  # Move to the next line
                else:
                    i += 1  # Move to the next line if the line doesn't contain the expected term structure
            else:
                i += 1  # Move to the next line if the line doesn't start with 'Term:'
    return index