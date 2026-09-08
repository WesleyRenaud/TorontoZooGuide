import assert from 'node:assert/strict';
import test from 'node:test';

import { RowBuilder } from '../../../../scripts/itinerary/panel/rowBuilder.js';
import { ItemView } from '../../../../scripts/itinerary/panel/components/itemView.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_BuildUniqueAnimals_TestDuplicates_ExpectMergedLikelihood', () => {
   const unique = RowBuilder.buildUniqueAnimals([
      { species: 'African Lion', exhibit: 'Savanna', likelihood: 40 },
      { species: 'African Lion', exhibit: 'Savanna', likelihood: 80 },
      { species: 'Amur Tiger', exhibit: 'Eurasia', likelihood: 50 },
   ]);

   assert.equal(unique.length, 2);
   const lion = unique.find((animal) => animal.species === 'African Lion');
   assert.equal(lion.likelihood, 80);
});

test('Test_BuildRows_TestNormalizeAndProps_ExpectItemRows', () => {
   const original = ItemView.makeItemRow;
   ItemView.makeItemRow = (props) => ({ props });

   try {
      const rows = RowBuilder.buildRows(
         [{ name: 'Carousel' }],
         {
            normalizeItem: (item) => ({ ...item, normalized: true }),
            buildRowProps: (item) => ({ title: item.name, normalized: item.normalized }),
         }
      );

      assert.deepEqual(rows, [{ props: { title: 'Carousel', normalized: true } }]);
   } finally {
      ItemView.makeItemRow = original;
   }
});

test('Test_BuildNamedRows_TestImageAndMeta_ExpectRowProps', () => {
   const original = ItemView.makeItemRow;
   ItemView.makeItemRow = (props) => props;

   try {
      const [row] = RowBuilder.buildNamedRows(
         [{ name: 'Carousel', region: 'Americas' }],
         {
            normalizeItem: (item) => item,
            defaultName: 'Attraction',
            imageDirectory: 'attractions',
            getName: (item) => item.name,
            getMetaLines: (item) => [`Region: ${item.region}`],
            getAlertLine: () => 'Alert',
            getLink: () => null,
         }
      );

      assert.equal(row.name, 'Carousel');
      assert.equal(row.imageSrc, 'images/details/attractions/carousel.png');
      assert.deepEqual(row.metaLines, ['Region: Americas']);
      assert.equal(row.alertLine, 'Alert');
   } finally {
      ItemView.makeItemRow = original;
   }
});
