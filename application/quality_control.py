from math import sqrt

def wilson_score(upvotes, downvotes):
    n = upvotes + downvotes
    if n == 0:
        return 0

    # Z-score of lower bound which gives 85% certainty
    z = 1.04
    phat = float(upvotes) / n
    return (phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

def sort_lines_by_wilson_score(lines):
    wilson_scores = [(wilson_score(line.upvotes, line.downvotes), line) for line in lines]
    wilson_scores.sort(reverse=True) # sorts descendingly
    return [line for (score, line) in wilson_scores]

def best_line(lines):
    if not lines:
        return [], []
    wilson_scores = [(wilson_score(line.upvotes, line.downvotes), line) for line in lines]
    sorted_lines = sort_lines_by_wilson_score(lines)
    # returns line with highest wilson score
    sorted_lines.sort(reverse=True)
    print "best line sorted_lines[0]"
    print sorted_lines[0]
    return sorted_lines[0], sorted_lines[1:]

