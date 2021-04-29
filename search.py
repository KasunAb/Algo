try:
    # This 'enchant' library also includes a function to calculate levenshtein distance
    # If you WANT, you can install this library
    # Run 'pip install pyenchant' in the command line (CMD) to install this library
    # NO NEED TO CHANGE THE CODE. It will automatically use this library if available
    import enchant

    ENCHANT = True
    print("Using enchant library\n")
except ModuleNotFoundError:
    ENCHANT = False

# Constants
SOURCE_FILE = "text.txt"  # put all the text from pdf file to this text file. line breaks are ignored
THRESHOLD = 1.1  # increase the threshold to get more search results


def levenshtein(s1, s2):  # do not modify
    if ENCHANT:
        return enchant.utils.levenshtein(s1, s2)
    M, N = len(s1), len(s2)
    l1 = list(range(N + 1))
    for i in range(1, M + 1):
        l2 = [0] * (N + 1)
        l2[0] = i
        c = s1[i - 1]
        for j in range(N):
            if s2[j] == c:
                l2[j + 1] = l1[j]
            else:
                l2[j + 1] = min(l2[j], l1[j], l1[j + 1]) + 1
        l1 = l2
    return l1[-1]


f = open(SOURCE_FILE, "r", encoding = "utf-8")
original = f.read().replace("\n", " ")
source = original.lower()
len_src = len(source)
print("press ctrl+c to stop")
while True:
    print("\nEnter search phrase : ", end="")
    text = input().strip().lower()
    len_text = len(text)
    long = len_text > 30
    threshold = THRESHOLD
    if long:
        text_original = text
        text = text[:20]
        len_text_original = len_text
        len_text = len(text)
        threshold = THRESHOLD + 0.1
    try:
        prev = -len_src - len_text
        for i in range(0, len_src - len_text, len_text):
            s = source[i : i + len_text * 2]
            dist = levenshtein(s, text)
            if dist / len_text < threshold:
                if long:
                    s = source[i : i + len_text_original * 2]
                    dist = levenshtein(s, text_original)
                    if dist / len_text_original < THRESHOLD:
                        if i - prev <= len_text:
                            continue
                        print(original[i : i + len_text_original * 3])
                        prev = i
                else:
                    if i - prev <= len_text:
                        continue
                    print(original[i : i + len_text * 3])
                    prev = i
    except KeyboardInterrupt:
        pass
