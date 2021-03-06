#!/usr/bin/env python

import os
import sys
import unittest

from sqlalchemy.orm.query import Query
from sqlalchemy import Column, String

sys.path = [ os.path.abspath(os.path.dirname(__file__)) ] + sys.path

from support import BaseModel, TestBase


class Person(BaseModel):
    name = Column(String)



class BasicTest(TestBase):
    def seed(self):
        global dp, jp
        dp = Person(name='dpepper').save()
        jp = Person(name='josh').save()


    def test_properties(self):
        self.assertEqual(
            'person',
            Person.__tablename__
        )

        self.assertIsInstance(Person.query, Query)

        self.assertEqual(
            dp,
            Person.first
        )

        self.assertEqual(
            [ dp, jp ],
            Person.all
        )


    def test_get(self):
        self.assertEqual(
            dp,
            Person.get(1)
        )

        self.assertEqual(
            dp,
            Person.get('1')
        )

        self.assertEqual(
            dp,
            Person.get(u'1')
        )


    def test_multiget(self):
        self.assertEqual(
            [ dp ],
            Person.get([ 1 ])
        )

        self.assertEqual(
            [ dp, jp ],
            Person.get([ 1, 2 ])
        )

        # supports type set
        self.assertEqual(
            [ dp, jp ],
            Person.get(set([ 1, 2 ]))
        )

        # supports type dict_keys and dict_items
        data = { 1 : 1, 2 : 2 }
        self.assertEqual(
            [ dp, jp ],
            Person.get(data.keys())
        )
        self.assertEqual(
            [ dp, jp ],
            Person.get(data.values())
        )


    def test_get_typecast(self):
        self.assertEqual(dp, Person.get(1))
        self.assertEqual(dp, Person.get('1'))
        self.assertEqual([ dp, jp ], Person.get([ '1', '2' ]))


    def test_get_errors(self):
        with self.assertRaises(TypeError):
            # missing param
            Person.get()

        with self.assertRaises(TypeError):
            # invalid param
            Person.get(None)

        with self.assertRaises(TypeError):
            # invalid key type
            Person.get([ 1, [ 2 ] ])


    def test_where(self):
        self.assertIsInstance(Person.where(), Query)

        # args
        self.assertEqual(
            dp,
            Person.where(Person.id == 1).one()
        )

        self.assertEqual(
            dp,
            Person.where(Person.name == 'dpepper').one()
        )

        self.assertEqual(
            [ dp, jp ],
            Person.where(Person.id.in_([1, 2])).all()
        )

        # kwargs
        self.assertEqual(
            dp,
            Person.where(id=1).one()
        )

        self.assertEqual(
            dp,
            Person.where(name='dpepper').one()
        )

        self.assertEqual(
            dp,
            Person.where(name=u'dpepper').one()
        )

        self.assertEqual(
            dp,
            Person.where(id=1, name='dpepper').one()
        )

        self.assertEqual(
            [ dp, jp ],
            Person.where(name=['dpepper', 'josh']).all()
        )

        self.assertIsNone(
            Person.where(id=123).one_or_none()
        )

        self.assertIsNone(
            Person.where(id=2, name='dpepper').one_or_none()
        )

        self.assertEqual(
            [ dp, jp ],
            Person.where(id=[1, 2]).all()
        )

        # args and kwargs
        self.assertEqual(
            dp,
            Person.where(Person.id == 1, id=1).one()
        )

        self.assertIsNone(
            Person.where(Person.id == 1, id=2).one_or_none()
        )

        self.assertEqual(
            dp,
            Person.where(Person.name == 'dpepper', id=[1, 2]).one()
        )


    def test_limit(self):
        self.assertEqual(
            [ dp ],
            list(Person.limit(1))
        )

        self.assertEqual(
            [ dp, jp ],
            list(Person.limit(5))
        )


    def test_count(self):
        self.assertEqual(2, Person.count)


    def test_delete(self):
        mara = Person(name='mara').save()
        self.assertEqual(
            mara,
            Person.where(name='mara').first()
        )
        mara.delete()
        self.assertIsNone(Person.where(name='mara').first())



if __name__ == '__main__':
    unittest.main()
