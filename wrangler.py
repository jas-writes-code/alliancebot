import json
#text and data wrangling that i'll probably need fairly often

def load(item):
    if item == "config":
        with open("config.json", "r") as f:
            file = json.load(f)
    else:
        with open(f'data/{item}.json', 'r') as f:
            file = json.load(f)
    return file

def save(file, item):
    if file == "config":
        with open("config.json", "w") as f:
            json.dump(item, f)
    else:
        with open(f'data/{file}.json', 'w') as f:
            json.dump(item, f, indent=4)

def newlength(text: str, limit: int = 1900) -> list[str]:
    chunks = []
    remaining = text

    while len(remaining) > limit:
        # Try to split at the last double newline before limit
        split_index = remaining.rfind("\n\n", 0, limit)
        if split_index != -1:
            split_index += 2  # include the "\n\n"
            chunks.append(remaining[:split_index])
            remaining = remaining[split_index:]
            continue

        # If no "\n\n" found, try splitting at the last space before limit
        split_index = remaining.rfind(" ", 0, limit)
        if split_index != -1:
            chunks.append(remaining[:split_index])
            remaining = remaining[split_index + 1:]
            continue

        # As a last resort, hard cut
        chunks.append(remaining[:limit])
        remaining = remaining[limit:]

    # Add whatever is left
    if remaining:
        chunks.append(remaining)

    return chunks