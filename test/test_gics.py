import unittest

from gics import GICS


class TestGICS(unittest.TestCase):

    def test_raises_when_invalid_GICS_version(self):
        with self.assertRaises(ValueError):
            GICS('10', 'blabla')

    def test_it_should_default_when_not_specified_version(self):
        gics = GICS('60')
        self.assertEqual('Real Estate', gics.sector.name)

    def test_marks_non_existent_codes_as_invalid(self):
        gics = GICS('9999')
        self.assertFalse(gics.is_valid)

    def test_marks_existent_codes_as_valid(self):
        gics = GICS('10')
        self.assertTrue(gics.is_valid)

    def test_supports_older_versions_if_specified(self):
        gics_old = GICS("4040", "20140228")
        gics_new = GICS("4040", "20160901")

        self.assertEqual('Financials', gics_old.sector.name)
        self.assertEqual('Real Estate', gics_old.industry_group.name)
        self.assertFalse(gics_new.is_valid)

    def test_returns_null_for_all_levels_on_invalid_GICS_code(self):
        gics = GICS("123")

        self.assertIsNone(gics.sector)
        self.assertIsNone(gics.industry_group)
        self.assertIsNone(gics.industry)
        self.assertIsNone(gics.sub_industry)

    def test_resolves_level_1_and_leaves_the_rest_null(self):
        gics = GICS("10")

        self.assertIsNotNone(gics.sector)
        self.assertIsNone(gics.industry_group)
        self.assertIsNone(gics.industry)
        self.assertIsNone(gics.sub_industry)

    def test_resolves_level2_and_leaves_the_rest_null(self):
        gics = GICS("1010")

        self.assertIsNotNone(gics.sector)
        self.assertIsNotNone(gics.industry_group)
        self.assertIsNone(gics.industry)
        self.assertIsNone(gics.sub_industry)

    def test_resolves_level_3_and_leaves_the_rest_null(self):
        gics = GICS("101010")

        self.assertIsNotNone(gics.sector)
        self.assertIsNotNone(gics.industry_group)
        self.assertIsNotNone(gics.industry)
        self.assertIsNone(gics.sub_industry)

    def test_resolves_level_4_and_sets_description(self):
        gics = GICS("10101010")

        self.assertIsNotNone(gics.sector)
        self.assertIsNotNone(gics.industry_group)
        self.assertIsNotNone(gics.industry)
        self.assertIsNotNone(gics.sub_industry)
        self.assertIsNotNone(gics.sub_industry.description)

    def test_resolves_GICS_partial_code_of_sub_components(self):
        gics = GICS("10101010")

        self.assertEqual('10', gics.sector.code)
        self.assertEqual('1010', gics.industry_group.code)
        self.assertEqual('101010', gics.industry.code)
        self.assertEqual('10101010', gics.sub_industry.code)

    def test_translates_name_to_level_properly(self):
        gics = GICS("10101010")

        self.assertEqual(gics.level(1), gics.sector)
        self.assertEqual(gics.level(2), gics.industry_group)
        self.assertEqual(gics.level(3), gics.industry)
        self.assertEqual(gics.level(4), gics.sub_industry)

    def test_accepts_null_code_GICS_and_marks_it_as_invalid(self):
        gics = GICS()

        self.assertFalse(gics.is_valid)

    def test_lists_all_sectors_as_children_for_an_invalid_GICS(self):
        gics = GICS()

        self.assertIsInstance(gics.children, list)
        self.assertEqual(11, len(gics.children))
        for child in gics.children:
            self.assertEqual(2, len(child.code))

    def test_lists_all_industry_groups_as_children_for_a_sector_level_GICS(self):
        gics = GICS('10')

        self.assertIsInstance(gics.children, list)
        self.assertEqual(1, len(gics.children))
        for child in gics.children:
            self.assertEqual(4, len(child.code))

    def test_lists_all_industries_as_children_for_an_industry_group_level_GICS(self):
        gics = GICS('1010')

        self.assertIsInstance(gics.children, list)
        self.assertEqual(2, len(gics.children))
        for child in gics.children:
            self.assertEqual(6, len(child.code))

    def test_lists_all_sub_industries_as_children_for_an_industry_level_GICS(self):
        gics = GICS('101010')

        self.assertIsInstance(gics.children, list)
        self.assertEqual(2, len(gics.children))
        for child in gics.children:
            self.assertEqual(8, len(child.code))

    def test_sub_industry_level_GICS_returns_empty_array_for_children(self):
        gics = GICS('10101010')

        self.assertIsInstance(gics.children, list)
        self.assertEqual(0, len(gics.children))

    def test_resolves_if_it_is_the_same_with_another_GICS(self):
        gics1 = GICS('1010')
        gics2 = GICS('1010')

        self.assertTrue(gics1.is_same(gics2))
        self.assertTrue(gics2.is_same(gics1))

    def test_resolves_if_it_is_not_the_same_with_another_GICS(self):
        gics1 = GICS('1010')
        gics2 = GICS('101010')

        self.assertFalse(gics1.is_same(gics2))
        self.assertFalse(gics2.is_same(gics1))

    def test_resolves_if_it_is_the_same_correctly_with_invalid_GICS(self):
        self.assertFalse(GICS('invalid').is_same(GICS('10')))
        self.assertFalse(GICS('10').is_same(GICS('invalid')))
        self.assertTrue(GICS('invalid').is_same(GICS('invalid')))

    def test_resolves_if_a_GICS_contains_another_GICS(self):
        self.assertTrue(GICS('10').contains(GICS('10101010')))
        self.assertTrue(GICS('10').contains(GICS('101010')))
        self.assertTrue(GICS('10').contains(GICS('1010')))
        self.assertFalse(GICS('10').contains(GICS('10')))
        self.assertFalse(GICS('1010').contains(GICS('10')))
        self.assertFalse(GICS('invalid').contains(GICS('10')))
        self.assertFalse(GICS('10').contains(GICS('invalid')))
        self.assertFalse(GICS('invalid').contains(GICS('invalid')))

    def test_resolves_if_a_GICS_is_immediately_contained_in_another_one(self):
        self.assertFalse(GICS('10').contains_immediate(GICS('10101010')))
        self.assertFalse(GICS('10').contains_immediate(GICS('101010')))
        self.assertTrue(GICS('10').contains_immediate(GICS('1010')))
        self.assertFalse(GICS('10').contains_immediate(GICS('10')))
        self.assertFalse(GICS('1010').contains_immediate(GICS('10')))
        self.assertFalse(GICS('invalid').contains_immediate(GICS('10')))
        self.assertFalse(GICS('10').contains_immediate(GICS('invalid')))
        self.assertFalse(GICS('invalid').contains_immediate(GICS('invalid')))

    def test_resolves_if_a_GICS_is_within_another_GICS(self):
        self.assertTrue(GICS('10101010').is_within(GICS('10')))
        self.assertTrue(GICS('101010').is_within(GICS('10')))
        self.assertTrue(GICS('101010').is_within(GICS('1010')))
        self.assertTrue(GICS('1010').is_within(GICS('10')))
        self.assertFalse(GICS('10').is_within(GICS('10')))
        self.assertFalse(GICS('1010').is_within(GICS('1010')))
        self.assertFalse(GICS('invalid').is_within(GICS('10')))
        self.assertFalse(GICS('10').is_within(GICS('invalid')))
        self.assertFalse(GICS('invalid').is_within(GICS('invalid')))

    def test_resolves_if_a_GICS_is_immediate_within_another_GICS(self):
        self.assertFalse(GICS('10101010').is_immediate_within(GICS('10')))
        self.assertFalse(GICS('101010').is_immediate_within(GICS('10')))
        self.assertTrue(GICS('101010').is_immediate_within(GICS('1010')))
        self.assertTrue(GICS('1010').is_immediate_within(GICS('10')))
        self.assertFalse(GICS('10').is_immediate_within(GICS('10')))
        self.assertFalse(GICS('1010').is_immediate_within(GICS('1010')))
        self.assertFalse(GICS('invalid').is_immediate_within(GICS('10')))
        self.assertFalse(GICS('10').is_immediate_within(GICS('invalid')))
        self.assertFalse(GICS('invalid').is_immediate_within(GICS('invalid')))

    def test_defaults_to_latest_definition(self):
        gics_deprecated = GICS('45101010')
        gics_new = GICS('50203010')

        self.assertFalse(gics_deprecated.is_valid)
        self.assertTrue(gics_new.is_valid)
        self.assertEqual('Interactive Media & Services', gics_new.sub_industry.name)
