import numpy as np
from nltk.corpus import inaugural, stopwords
from nltk.stem import PorterStemmer

from whylogs.core.configs import SummaryConfig
from whylogs.experimental.core.metrics.nlp_metric import (
    BagOfWordsMetric,
    log_nlp,
    LsiMetric,
    NlpConfig,
    SvdMetric,
    SvdMetricConfig,
    UpdatableSvdMetric,
    _preprocessifier,
)

# from nltk.tokenize import word_tokenize

# import nltk
# nltk.download('stopwords')
# nltk.download('inaugural')

# inverted index weighting utility functions


def global_freq(A: np.ndarray) -> np.ndarray:
    gf = np.zeros(A.shape[0])
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            gf[i] += A[i, j]
    return gf


def entropy(A: np.ndarray) -> np.ndarray:
    gf = global_freq(A)
    g = np.ones(A.shape[0])
    logN = np.log(A.shape[1])
    assert logN > 0.0
    for i in range(A.shape[0]):
        assert gf[i] > 0.0
        for j in range(A.shape[1]):
            p_ij = A[i, j] / gf[i]
            g[i] += p_ij * np.log(p_ij) / logN if p_ij > 0.0 else 0.0
    return g


def log_entropy(A: np.ndarray) -> None:
    g = entropy(A)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] = g[i] * np.log(A[i, j] + 1.0)


# the NLTK tokenizer produces punctuation as terms, so stop them
stop_words = set(
    stopwords.words("english")
    + [
        ".",
        ",",
        ":",
        ";",
        '."',
        ',"',
        '"',
        "'",
        " ",
        "?",
        "[",
        "]",
        ".]",
        "' ",
        '" ',
        "?",
        "? ",
        "-",
        "- ",
        "/",
        '?"',
        "...",
        "",
    ]
)

# build weighted inverted index of inaugural speeches
stemmer = PorterStemmer()

vstopped = {w for w in inaugural.words() if w.casefold() not in stop_words}
vocab = {stemmer.stem(w.casefold()) for w in vstopped}
vocab_size = len(vocab)

vocab_map = {}
rev_map = [""] * vocab_size
dim = 0
for w in vocab:
    if w not in vocab_map:
        vocab_map[w] = dim
        rev_map[dim] = w
        dim += 1

doc_lengths = []
ndocs = len(inaugural.fileids())
doc = 0
index = np.zeros((vocab_size, ndocs))
for fid in inaugural.fileids():
    stopped = [t.casefold() for t in inaugural.words(fid) if t.casefold() not in stop_words]
    stemmed = [stemmer.stem(w) for w in stopped]
#    print(f"{fid} : {stemmed}")
#    print()
    doc_lengths.append(len(stemmed))
    for w in stemmed:
        index[vocab_map[w], doc] += 1
    doc += 1

print(f"doc lenghts {doc_lengths}\nmean: {np.array(doc_lengths).mean()}\nstd: {np.std(doc_lengths)}\nmax: {max(doc_lengths)}\nmin: {min(doc_lengths)}\nnum docs: {len(doc_lengths)}\nnum terms: {vocab_size}")
print()

A = index.copy()
log_entropy(A)

gf = global_freq(index)
g = entropy(index)


# build reference profile

num_concepts = 10
old_doc_decay_rate = 0.8
svd_config = SvdMetricConfig(k=num_concepts, decay=old_doc_decay_rate)
svd = UpdatableSvdMetric.zero(svd_config)

nlp_config = NlpConfig(svd=svd)
ref_bow = BagOfWordsMetric.zero(nlp_config)
ref_lsi = LsiMetric.zero(nlp_config)

for fid in inaugural.fileids():
    stopped = [t.casefold() for t in inaugural.words(fid) if t.casefold() not in stop_words]
    stemmed = [stemmer.stem(w) for w in stopped]

    doc_vec = np.zeros(vocab_size)
    for w in stemmed:
        doc_vec[vocab_map[w]] += 1
    for i in range(vocab_size):
        doc_vec[i] = g[i] * np.log(doc_vec[i] + 1.0)

    ref_bow.columnar_update(_preprocessifier(stemmed, doc_vec))
    ref_lsi.columnar_update(_preprocessifier(stemmed, doc_vec))  # update SVD & residual

print(f"\nU: {svd.U.value}\nS: {svd.S.value}\n")
assert svd.namespace == "updatable_svd"
assert ref_lsi.svd.namespace == "updatable_svd"


concepts = svd.U.value.transpose()
for i in range(concepts.shape[0]):
    pos_idx = sorted(range(len(concepts[i])), key=lambda x: concepts[i][x])[-10:]
    neg_idx = sorted(range(len(concepts[i])), key=lambda x: -1 * concepts[i][x])[-5:]
    print(", ".join([rev_map[j] for j in pos_idx])) # + [rev_map[j] for j in neg_idx]))
print()

# save reference profile locally
write_me = ref_lsi.to_protobuf()  # small--only has 3 DistributionMetrics and a FrequentItemsMetric
svd_write_me = ref_lsi.svd.to_protobuf()  # big--contains the SVD approximation & parameters


# production tracking, no reference update

prod_svd = SvdMetric.from_protobuf(svd_write_me)  # use UpdatableSvdMetric to train in production

print(svd)
print(prod_svd)

nlp_config = NlpConfig(svd=prod_svd)
print(type(nlp_config.svd.U.value))

#nlp_config = NlpConfig(svd)
prod_lsi = LsiMetric.zero(cfg=nlp_config)


residuals = []
for fid in inaugural.fileids():
    stopped = [t.casefold() for t in inaugural.words(fid) if t.casefold() not in stop_words]
    stemmed = [stemmer.stem(w) for w in stopped]

    doc_vec = np.zeros(vocab_size)
    for w in stemmed:
        doc_vec[vocab_map[w]] += 1
    for i in range(vocab_size):
        doc_vec[i] = g[i] * np.log(doc_vec[i] + 1.0)

    residuals.append(prod_lsi.svd.residual(doc_vec))
    prod_lsi.columnar_update(_preprocessifier(stemmed, doc_vec))  # update residual only, not SVD

print(f"\nresiduals: {residuals}\n")

# if we trained with production data
# write_me = prod_nlp.svd.to_protobuf()

# send to whylabs, no SVD state
send_me = prod_lsi.to_protobuf()

# get stats on doc length, term length, SVD "fit"
view_me = prod_lsi.to_summary_dict(SummaryConfig())
# print(view_me)

