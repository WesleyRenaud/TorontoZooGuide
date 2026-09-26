import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchBuilder } from '../../../scripts/search/searchBuilder.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';


test('Test_FlattenSearchRows_TestNormalizedGroups_ExpectTypedRows', () => {
   const lion = { species: 'African Lion' };
   const shop = { name: 'Zootique' };
   const carousel = { name: 'Conservation Carousel' };
   const talk = { name: 'Amur Tiger' };
   const encounter = { name: 'African Rainforest' };
   const response = {
      [ScheduleItemKind.ANIMAL.itemType]: [lion],
      gift_shops: [shop],
      [ScheduleItemKind.ATTRACTION.itemType]: [carousel],
      [ScheduleItemKind.GUARDIANS_TALK.itemType]: [talk],
      [ScheduleItemKind.WILD_ENCOUNTER.itemType]: [encounter],
      unsupported: [{ name: 'Not a search group' }],
   };

   const rows = SearchBuilder.flattenSearchRows(response);

   assert.deepEqual(rows, [
      { ...lion, type: ItemType.ANIMAL },
      { ...shop, type: ItemType.GIFT_SHOP },
      { ...carousel, type: ItemType.ATTRACTION },
      { ...talk, type: ItemType.GUARDIANS_TALK },
      { ...encounter, type: ItemType.WILD_ENCOUNTER },
   ]);
});


test('Test_FlattenSearchRows_TestNull_ExpectEmpty', () => {
   const response = null;

   const rows = SearchBuilder.flattenSearchRows(response);

   assert.deepEqual(rows, []);
});


test('Test_FlattenSearchRows_TestNonArrayGroup_ExpectEmpty', () => {
   const response = { attractions: 'Conservation Carousel' };

   const rows = SearchBuilder.flattenSearchRows(response);

   assert.deepEqual(rows, []);
});
