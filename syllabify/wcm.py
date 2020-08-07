#!/usr/bin/env python
#
# Copyright (c) 2014 Kyle Gorman
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# wcm.py: Stoel-Gammon's Word Complexity Measure


from syllabify import syllabify
import nltk
#nltk.download('cmudict')
arpabet = nltk.corpus.cmudict.dict()

## constants
DORSALS = frozenset("K G NG".split())
LIQUIDS = frozenset("L R".split())
VOICED_AF = frozenset("V DH Z ZH".split())
AF = frozenset("F TH S SH CH".split()) | VOICED_AF


def wcm(word):
    """
    The "Word Complexity Measure", as proposed in:

    C. Stoel-Gammon. 2010. The Word Complexity Measure: Description and 
    application to developmental phonology and disorders. Clinical
    Linguistics and Phonetics 24(4-5): 271-282.
    """
    phonemes = arpabet[word][0]
    syls = syllabify.syllabify(phonemes) 
    # begin scoring
    score = 0
    ## Word patterns:
    # (1) Productions with more than two syllables receive 1 point
    if len(syls) > 2:
        score += 1
    # (2) Productions with stress on any syllable but the first receive 
    # 1 point
    if len(syls) > 1 and not syls[0][1][-1].endswith("1"):
        score += 1
    ## Syllable structures
    # (1) Productions with a word-final consonant receive 1 point
    if syls[-1][2] != []:
        score += 1
    # (2) Productions with a syllable cluster (defined as a sequence of 
    # two or more consonants within a syllable) receive one point for 
    # each cluster:
    for syl in syls:
        if len(syl[0]) > 1:
            score += 1
        if len(syl[2]) > 1:
            score += 1
    ## Sound classes:
    # (1) Productions with a velar consonant receive 1 point for each 
    # velar
    for syl in syls:
        score += sum(ph in DORSALS for ph in (syl[0] + syl[2]))
    # (2) Productions with a liquid, a syllabic liquid, or a rhotic vowel 
    # receive 1 point for each liquid, syllabic liquid, and rhotic vowel
    for syl in syls:
        score += sum(ph in LIQUIDS for ph in (syl[0] + syl[2]))
        score += sum(len(ph) > 1 and ph[1] == "R" for ph in syl[1])
    # (3) Productions with a fricative or affricate receive 1 point for
    # each fricative and affricate
        score += sum(ph in AF for ph in (syl[0] + syl[2]))
    # (4) Productions with a voiced fricative or affricate receive 1 point
    # for each fricative and affricate (in addition to the point received
    # for #3)
    for syl in syls:
        score += sum(ph in VOICED_AF for ph in (syl[0] + syl[2]))
    ## and we're done
    print(word, score)
    return score


wcm('voice')
wcm('communications')
wcm('elevate')
wcm('portal')
wcm('services')
wcm('cloud')
wcm('com')
wcm('io')
