import assert from 'node:assert/strict';
import test from 'node:test';

import { ItemView } from '../../../../scripts/itinerary/panel/components/itemView.js';
import { RowBuilder } from '../../../../scripts/itinerary/panel/rowBuilder.js';
import { RowPresenter } from '../../../../scripts/itinerary/panel/rowPresenter.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_BuildUniqueAnimals_TestDuplicates_ExpectMergedLikelihood', () => {
   const species = 'African Lion';
   const exhibit = 'Savanna';
   const firstLikelihood = 40;
   const secondLikelihood = 80;
   const animals = [
      { species, exhibit, likelihood: firstLikelihood },
      { species, exhibit, likelihood: secondLikelihood },
      { species: 'Amur Tiger', exhibit: 'Eurasia', likelihood: 50 },
   ];

   const unique = RowBuilder.buildUniqueAnimals(animals);

   const lion = unique.find((animal) => animal.species === species);

   assert.equal(unique.length, animals.length - 1);
   assert.equal(lion.likelihood, Math.max(firstLikelihood, secondLikelihood));
});


test('Test_BuildRows_TestNormalizeAndProps_ExpectItemRows', () => {
   const original = ItemView.makeItemRow;
   const name = 'Conservation Carousel';
   ItemView.makeItemRow = (props) => ({ props });

   try {
      const rows = RowBuilder.buildRows(
         [{ name }],
         {
            normalizeItem: (item) => ({ ...item, normalized: true }),
            buildRowProps: (item) => ({ title: item.name, normalized: item.normalized }),
         }
      );

      assert.deepEqual(rows, [{ props: { title: name, normalized: true } }]);
   } finally {
      ItemView.makeItemRow = original;
   }
});


test('Test_BuildNamedRows_TestImageAndMeta_ExpectRowProps', () => {
   const original = ItemView.makeItemRow;
   const name = 'Conservation Carousel';
   const region = 'Americas';
   const imageDirectory = 'attractions';
   const alertLine = 'Alert';
   ItemView.makeItemRow = (props) => props;

   try {
      const rows = RowBuilder.buildNamedRows(
         [{ name, region }],
         {
            normalizeItem: (item) => item,
            defaultName: 'Attraction',
            imageDirectory,
            getName: (item) => item.name,
            getMetaLines: (item) => [`Region: ${item.region}`],
            getAlertLine: () => alertLine,
            getLink: () => null,
         }
      );
      const row = rows.at(Position.FIRST);

      assert.equal(row.name, name);
      assert.equal(row.imageSrc, RowPresenter.buildImageSrc(imageDirectory, name));
      assert.deepEqual(row.metaLines, [`Region: ${region}`]);
      assert.equal(row.alertLine, alertLine);
   } finally {
      ItemView.makeItemRow = original;
   }
});
