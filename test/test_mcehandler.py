#!/usr/bin/env python


from mcehandler import count_num_events_since_clear
from nose.tools import raises, eq_

def test_count_num_events_since_clear_counts_properly():
    cases = [
        ({'a': [('MCE', 1, 'Test'), ('MCE_MAINT', 2 ,'Test')]}, {'a': 0}),
        ({'a': [('MCE_MAINT', 1, 'Test'), ('MCE', 2, 'Test')]}, {'a': 1}),
        ({'a': [('MCE', 1, 'Test')]}, {'a': 1}),
        ({'a': [('MCE', 1, 'Test')], 'b': [('MCE',1,'Test')]}, {'a': 1, 'b':
                                                                1})
        ]
    for case in cases:
        res = count_num_events_since_clear(case[0])
        yield eq_, res, case[1]

@raises(ValueError)
def test_count_num_events_since_clear_fails_on_non_float():
    count_num_events_since_clear({'a': [('MCE', 'Hello', 'Test'),
                                        ('MCE', 'Goodbye', 'Test')]})
