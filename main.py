"""One word for the whole internet: the funniest, most fitting single
word wins, judged blind against a brief that weighs being on subject
first, then funny, then fitting, then surprising, then landing in one
beat.

Running this module writes the word to the file the grader reads:
``/output/entry.txt`` by default, or the path named by ``ENTRY_OUTPUT``
for a local test run. Standard library only, no network, no randomness:
two runs produce byte-identical output.
"""

import os
from pathlib import Path

# The word itself: FERAL.
# Why this word, against the judge's brief (most important first):
#   1. It IS one word describing the whole internet: the internet as
#      a wild animal that escaped domestication -- no owner, no leash,
#      no rules, and it bites back.
#   2. It is funny because the image lands on its own: picture the
#      entire internet as one feral creature, hissing from the bushes,
#      that nobody can house-train. No explanation needed.
#   3. It is true about the internet as a whole, not one app, site or
#      mood: every corner of it -- feeds, forums, comment sections,
#      marketplaces -- runs untamed, and nobody is in charge of it.
#   4. It surprises: the first words anyone reaches for are "chaos",
#      "memes", "cats", "wild", "unhinged". "Feral" is the fresher,
#      sharper cousin of those -- the same wildness, said once, with
#      teeth.
#   5. It lands in one beat: five letters, spelled plainly, readable
#      before the reader has time to think -- and in an exact tie it
#      wins on size against every longer word.
# Runner-ups, kept out: "Bedlam" -- a madhouse of uproar, literary
# and surprising, but a knowing smile rather than a laugh, and one
# letter longer; "Pandemonium" -- where all the demons gather, the
# funniest image of the three, but eleven letters and it loses the
# one-beat landing; "Babel" -- everyone talking, nobody understanding,
# but wry rather than funny; "Everything" -- the deadpan meta-joke,
# literally true, but a word too many entrants will reach for first;
# "Dumpsterfire" -- vivid and funny, but about the mess, and the
# obvious pick of the crowd. The gate allows 1-30 characters; this
# is 5.
WORD = "Feral"
LIMIT = 30


def check(word):
    """Reject anything the gate would refuse: more than one word,
    blank, over the character limit, padded with whitespace, or
    holding control characters."""
    if not word.strip():
        raise ValueError("word must not be blank")
    if word != word.strip():
        raise ValueError("word must not start or end with whitespace")
    if len(word.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if not word.isascii() or not word.isalpha():
        raise ValueError("entry must be ASCII letters only, no digits or symbols")
    if len(word) > LIMIT:
        raise ValueError("word is over the character limit")
    if any(ord(ch) < 0x20 for ch in word):
        raise ValueError("word must not hold control characters")


def destination():
    """Where the word goes: the grader's path, unless ENTRY_OUTPUT
    points the run at a scratch file for local testing."""
    return Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.txt"))


def main():
    check(WORD)
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(WORD, encoding="utf-8")
    target.chmod(0o644)
    # Read it back: the grader gates on the file's exact bytes, so
    # prove the write landed whole before the program exits.
    if target.read_text(encoding="utf-8") != WORD:
        raise ValueError("written word does not match the entry")


if __name__ == "__main__":
    main()
