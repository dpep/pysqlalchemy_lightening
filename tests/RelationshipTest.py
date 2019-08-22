#!/usr/bin/env python

import os
import sys
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '.')) ] + sys.path

from models import Person, Pet, Food


Person.query.delete()
Pet.query.delete()
Food.query.delete()

dp = Person(name='dpepper').save()
brownie = Pet(name='brownie')
dp.pets.append(brownie)

jp = Person(name='josh').save()

carrots = Food(name='carrots').save()
grass = Food(name='grass').save()
apple = Food(name='apple').save()



class BasicTest(unittest.TestCase):
    def test_upgrade(self):
        # was implicitly upgraded to Rekeyable and Pluckable
        self.assertTrue(hasattr(dp.pets, 'rekey'))
        self.assertTrue(hasattr(dp.pets, 'pluck'))


    def test_shift_upgrade(self):
        # lshift is aliased to append
        pet = Pet(name='sammy')
        dp.pets << pet

        self.assertIn(pet, dp.pets)


    def test_one_to_many(self):
        self.assertEqual(
            [ dp.id ],
            dp.pets.pluck('person_id')
        )

        self.assertEqual(
            [ 'brownie' ],
            dp.pets.pluck('name')
        )

        self.assertEqual(
            [],
            jp.pets
        )


    def test_many_to_one(self):
        brownie.food = grass

        self.assertEqual(
            grass,
            brownie.food
        )

        # foreign key implicitly updated by event handler
        self.assertEqual(
            grass.id,
            brownie.food_id
        )

        # test update
        brownie.food = carrots

        self.assertEqual(
            carrots,
            brownie.food
        )

        self.assertEqual(
            carrots.id,
            brownie.food_id
        )

        # test delete
        brownie.food = None
        self.assertIsNone(brownie.food)
        self.assertIsNone(brownie.food_id)


    def test_many_to_one_foreign_key(self):
        '''
        Ensure that setting the foreign key column correctly resets
        the relationship value, ie. changing Pet.food_id changes Pet.food
        '''
        hopper = Pet(name='hopper').save()
        carrots = Food.where(name='carrots').one()
        grass = Food.where(name='grass').one()
        Pet.query.session.flush()

        self.assertIsNone(hopper.food)
        self.assertIsNone(hopper.food_id)

        hopper.food_id = carrots.id

        self.assertEqual(
            carrots.id,
            hopper.food_id
        )

        # implicitly updated by event handler
        self.assertEqual(
            carrots,
            hopper.food
        )

        hopper.food_id = grass.id

        self.assertEqual(
            grass.id,
            hopper.food_id
        )

        self.assertEqual(
            grass,
            hopper.food
        )

        hopper.food_id = None
        self.assertIsNone(hopper.food_id)
        self.assertIsNone(hopper.food)


    def test_secondary_many_to_one(self):
        '''
        key name may differ from foreign table name,
          eg. Pet.treat_id maps to Food.id
        '''
        self.assertIsNone(brownie.treat_id)
        self.assertIsNone(brownie.treat)
        self.assertIsNone(brownie.food)

        brownie.treat = apple

        self.assertEqual(
            apple,
            brownie.treat
        )
        self.assertEqual(
            apple.id,
            brownie.treat_id
        )

        # should not have changed
        self.assertIsNone(brownie.food)

        brownie.food = grass
        self.assertEqual(
            grass.id,
            brownie.food_id
        )

        # should not have changed
        self.assertEqual(
            apple.id,
            brownie.treat_id
        )

        # test delete
        brownie.treat = None
        self.assertIsNone(brownie.treat)
        self.assertIsNone(brownie.treat_id)

        # should not have changed
        self.assertEqual(
            grass.id,
            brownie.food_id
        )


if __name__ == '__main__':
    unittest.main()
