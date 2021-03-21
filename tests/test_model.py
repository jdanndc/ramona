from ramona.model import Model

def test_model_counts():
    model = Model()
    model.add_text("a b c").recalculate()
    # by default, we add a "beginning of sentence" bos marker
    assert(len(model.counts.keys()) == 2)

    model.reset().add_text("a b c", bos=False).recalculate()
    assert(len(model.counts.keys()) == 1)
    assert(list(model.counts[('a', 'b')].keys()) == ['c'])

    model.reset().add_text("a b c", bos=False).recalculate()
    # ('a','b')
    assert(len(model.counts.keys()) == 1)

    model.reset().add_text("a b c a", bos=False).recalculate()
    # ('a','b'), ('b','c')
    assert(len(model.counts.keys()) == 2)

    model.reset().add_text("a b c a b", bos=False).recalculate()
    # ('a','b'), ('b','c'), ('c','a')
    assert(len(model.counts.keys()) == 3)

    model.reset().add_text("a b c a b c", bos=False).recalculate()
    # ('a','b'), ('b','c'), ('c','a')
    assert(len(model.counts.keys()) == 3)

    model.reset().add_text("a b c a b d", bos=False).recalculate()
    assert(len(model.counts.keys()) == 3)
    assert(len(model.counts[('a', 'b')].keys()) == 2)
    assert(len(model.counts[('b', 'c')].keys()) == 1)

    model.reset().add_text("a b c    a b d     a b c", bos=False).recalculate()
    # counts[('a','b')] -> { 'c': 2, 'd': 1 }
    assert(len(model.counts[('a', 'b')].keys()) == 2)
    assert(sorted(list(model.counts[('a', 'b')].keys())) == ['c', 'd'])
    assert(model.counts[('a', 'b')]['c'] == 2)
    assert(model.counts[('a', 'b')]['d'] == 1)
    # counts[('b','c')] -> { 'a': 1 }
    assert(len(model.counts[('b', 'c')].keys()) == 1)
    assert(model.counts[('b', 'c')]['a'] == 1)

def test_model_reset():
    model = Model()
    assert(model.start_states is None)
    assert(model.states is None)
    model.add_text("foo bar baz bar foo foo bar bimp bop foo bar baz")
    # these only get filled after we call generate
    assert(model.states is None)
    assert(model.start_states is None)
    assert(len(model.counts.keys()) != 0)
    model.reset()
    assert(model.states is None)
    assert(model.start_states is None)
    assert(len(model.counts.keys()) == 0)
