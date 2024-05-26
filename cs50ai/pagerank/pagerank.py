import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    number_of_pages = len(corpus)
    outgoing_links = corpus.get(page, set())
    probability_dict = {}

    for pagename in corpus:
        if outgoing_links:
            if pagename in outgoing_links:
                probability_dict[pagename] = (1 - damping_factor) / number_of_pages + damping_factor / len(outgoing_links)
            else:
                probability_dict[pagename] = (1 - damping_factor) / number_of_pages
        else:
            probability_dict[pagename] = 1 / number_of_pages

    return probability_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_counts = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))

    for i in range(n):
        page_counts[current_page] += 1
        probabilities = transition_model(corpus, current_page, damping_factor)
        next_page = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
        current_page = next_page

    # Normalize counts to get fair results
    total_samples = sum(page_counts.values())
    pagerank = {page: count / total_samples for page, count in page_counts.items()}

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)

    pagerank = {page: 1 / num_pages for page in corpus}
    new_pagerank = {}

    while True:

        for page in corpus.keys():
            incoming_pagerank = 0
            # calculate the sum of incoming pagerank
            for link in corpus[page]:
                # no incoming link
                if len(link) == 0:
                    incoming_pagerank += (pagerank[incoming_page] / num_pages)
                else:
                    incoming_pagerank = sum(pagerank[incoming_page] / len(corpus[incoming_page]) for incoming_page in corpus if page in corpus[incoming_page])

            new_pagerank[page] = (1 - damping_factor) / num_pages + damping_factor * incoming_pagerank

        # normalize the new page rank:
        norm_factor = sum(new_pagerank.values())
        new_pagerank = {page : (rank / norm_factor) for page, rank in new_pagerank.items()}

        not_converged = True
        if not_converged:
            for i in corpus:
                converged = abs(new_pagerank[i] - pagerank[i])
                # Set limit to converged as 0.001
                if converged >= 0.001:
                    not_converged = False
                pagerank[i] = new_pagerank[i]
            if not_converged:
                break

    return new_pagerank


if __name__ == "__main__":
    main()
