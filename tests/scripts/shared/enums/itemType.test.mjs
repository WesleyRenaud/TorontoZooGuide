import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItemType } from '../../../../scripts/shared/enums/itemType.js';
import itemTypeValues from '../../../../shared/enums/itemType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_ItemType_TestConstants_ExpectWireValues', () => {
   assert.equal(ItemType.ANIMAL, 'animal');
   assert.equal(ItemType.GIFT_SHOP, 'giftShop');
   assert.equal(ItemType.GUARDIANS_TALK, 'guardiansTalk');
   assert.equal(ItemType.ITINERARY_EVENT, 'itineraryEvent');
   assert.equal(ItemType.TRANSPORTATION_STATION, 'transportationStation');
   assert.equal(ItemType.WILD_ENCOUNTER, 'wildEncounter');
   assert.equal(ItemType.TRANSPORTATION_ROUTE, 'transportationRoute');
   assert.equal(ItemType.TRANSPORTATION_ROUTE_MARKER, 'transportationRouteMarker');
});

test('Test_ItemType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(itemTypeValues)) {
      assert.equal(ItemType[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itemType.json'), 'utf8')
   );
   assert.deepEqual(itemTypeValues, diskValues);
   assert.deepEqual(Object.keys(itemTypeValues).sort(), Object.keys(ItemType).filter((key) => key === key.toUpperCase()).sort());
});
