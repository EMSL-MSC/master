#!/usr/bin/env python


from mcehandler import count_events
from nose.tools import raises, eq_

def test_count_events_counts_properly():
    cases = [
        ({'a': [('MCE', 1, 'Test'), ('MCE_MAINT', 2 ,'Test')]}, {'a': 0}),
        ({'a': [('MCE_MAINT', 1, 'Test'), ('MCE', 2, 'Test')]}, {'a': 1}),
        ({'a': [('MCE', 1, 'Test')]}, {'a': 1}),
        ({'a': [('MCE', 1, 'Test')], 'b': [('MCE',1,'Test')]},
         {'a': 1, 'b': 1}
        ),
        (
            {
                'a': [('MCE', 1, 'Test1'), ('MCE', 1, 'Test2')],
                'b': [('MCE',1,'Test2')]
            },
            {'a': 1, 'b': 1}
        ),
        (
            {
                'a': [
                    ('MCE', 1, 'Test1'),
                    ('MCE', 1, 'Test2'),
                    ('MCE', 1, 'Test1')
                ],
                'b': [('MCE',1,'Test2')]
            },
            {'a': 2, 'b': 1}
        ),
        (
            {
                'a': [
                    ('MCE', -1, 'Test1'),
                    ('MCE', 1, 'Test2'),
                    ('MCE', 1, 'Test1')
                ],
                'b': [('MCE',1,'Test2')]
            },
            {'a': 1, 'b': 1}
        ),
    ]
    for case in cases:
        res = count_events(case[0], 0)
        yield eq_, res, case[1]

@raises(ValueError)
def test_count_events_fails_on_non_float():
    count_events({'a': [('MCE', 'Hello', 'Test'),
                                        ('MCE', 'Goodbye', 'Test')]}, 0)
