import sys
from difflib import SequenceMatcher


def get_best_match(query,
                   corpus,
                   step=4,
                   flex=3,
                   case_sensitive=False,
                   verbose=False):
    """Return best matching substring of corpus.

    Parameters
    ----------
    query : str
    corpus : str
    step : int
        Step size of first match-value scan through corpus. Can be thought of
        as a sort of "scan resolution". Should not exceed length of query.
    flex : int
        Max. left/right substring position adjustment value. Should not
        exceed length of query / 2.

    Outputs
    -------
    output0 : str
        Best matching substring.
    output1 : float
        Match ratio of best matching substring. 1 is perfect match.

    https://stackoverflow.com/questions/36013295/find-best-substring-match
    """

    def ratio(a, b):
        """Compact alias for SequenceMatcher."""
        return SequenceMatcher(None, a, b).ratio()

    def scan_corpus(step):
        """Return list of match values from corpus-wide scan."""
        match_values = []

        m = 0
        while m + qlen - step <= len(corpus):
            match_values.append(ratio(query, corpus[m : m-1+qlen]))
            if verbose:
                print(query, "-", corpus[m: m + qlen], ratio(query, corpus[m: m + qlen]))
            m += step

        return match_values

    def index_max(v):
        """Return index of max value."""
        return max(range(len(v)), key=v.__getitem__)

    def adjust_left_right_positions():
        """Return left/right positions for best string match."""
        # bp_* is synonym for 'Best Position Left/Right' and are adjusted
        # to optimize bmv_*
        p_l, bp_l = [pos] * 2
        p_r, bp_r = [pos + qlen] * 2

        # bmv_* are declared here in case they are untouched in optimization
        bmv_l = match_values[int(p_l / step)]
        bmv_r = match_values[int(p_r / step)]

        for f in range(flex):
            ll = ratio(query, corpus[p_l - f: p_r])
            if ll > bmv_l:
                bmv_l = ll
                bp_l = p_l - f

            lr = ratio(query, corpus[p_l + f: p_r])
            if lr > bmv_l:
                bmv_l = lr
                bp_l = p_l + f

            rl = ratio(query, corpus[p_l: p_r - f])
            if rl > bmv_r:
                bmv_r = rl
                bp_r = p_r - f

            rr = ratio(query, corpus[p_l: p_r + f])
            if rr > bmv_r:
                bmv_r = rr
                bp_r = p_r + f

            if verbose:
                print("\n" + str(f))
                print("ll: -- value: {} -- snippet: {}".format(
                    ll, corpus[p_l - f: p_r]
                ))
                print("lr: -- value: {} -- snippet: {}".format(
                    lr, corpus[p_l + f: p_r]
                ))
                print("rl: -- value: {} -- snippet: {}".format(
                    rl, corpus[p_l: p_r - f]
                ))
                print("rr: -- value: {} -- snippet: {}".format(
                    rl, corpus[p_l: p_r + f]
                ))

        return bp_l, bp_r, ratio(query, corpus[bp_l : bp_r])

    if not case_sensitive:
        query = query.lower()
        corpus = corpus.lower()

    qlen = len(query)

    if flex >= qlen/2:
        print("Warning: flex exceeds length of query / 2. Setting to default.")
        flex = 3

    match_values = scan_corpus(step)
    pos = index_max(match_values) * step

    pos_left, pos_right, match_value = adjust_left_right_positions()

    return corpus[pos_left: pos_right].strip(), match_value


def int_to_roman(num):
    """
    https://stackoverflow.com/questions/42875103/integer-to-roman-number
    https://stackoverflow.com/questions/33486183/convert-from-numbers-to-roman-notation
    """
    conv = (
        ("M", 1000),
        ("CM", 900),
        ("D", 500),
        ("CD", 400),
        ("C", 100),
        ("XC", 90),
        ("L", 50),
        ("XL", 40),
        ("X", 10),
        ("IX", 9),
        ("V", 5),
        ("IV", 4),
        ("I", 1)
    )
    roman = ""
    i = 0
    while num > 0:
        while conv[i][1] > num:
            i += 1
        roman += conv[i][0]
        num -= conv[i][1]
    return roman


def roman_to_int(roman):
    """
    https://gist.github.com/kristopherjohnson/f4eca9018c5085fc736b2f29a202b8f8
    """
    vals = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }
    total = 0
    lastValue = sys.maxsize
    for char in list(roman):
        value = vals[char.upper()]
        if value > lastValue:
            total += value - 2 * lastValue
        else:
            total += value
        lastValue = value
    return total
