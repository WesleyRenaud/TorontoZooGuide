import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   buildRemovedItemsPopupSections,
   hasRemovedItemsPopupContent,
} from '../../scripts/itinerary/panel/components/removedItemsPopupContent.js';
import { updateItineraryAdjustmentTypesFromConfig } from '../../scripts/itinerary/itineraryAdjustmentTypes.js';
import { buildSpeciesExhibitKey } from '../../scripts/itinerary/speciesExhibitKey.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

test('hasRemovedItemsPopupContent is re-exported from the content module', () => {
   assert.equal(
      hasRemovedItemsPopupContent({
         removed: {
            animals: [{ species: 'Lion', exhibit: 'Savanna' }],
         },
      }),
      true
   );
});

test.describe('removedItemsPopupContent', () => {
   installDomTestHooks({
      before: () => {
         updateItineraryAdjustmentTypesFromConfig({
            adjustmentTypes: {
               ARRIVAL_TIME_ADJUSTED: 'arrivalTimeAdjusted',
               DEPARTURE_TIME_ADJUSTED: 'departureTimeAdjusted',
            },
         });
      },
   });

   test('buildRemovedItemsPopupSections renders adjustment and unscheduled sections', () => {
      const sections = buildRemovedItemsPopupSections({
         adjustments: [{
            type: 'arrivalTimeAdjusted',
            previousValue: '09:00',
            value: '09:30',
         }],
         unscheduled: {
            animals: [{
               species: 'African Lion',
               exhibit: 'Africa Savanna',
            }],
         },
      });

      assert.equal(sections.length, 2);
      assert.equal(
         sections[0]?.querySelector('.itin-removed-section-title')?.textContent,
         APP_STRINGS.itinerary.removedItems.itineraryTimesTitle
      );
      assert.equal(
         sections[1]?.querySelector('.itin-removed-section-title')?.textContent,
         APP_STRINGS.itinerary.dayPlanner.unscheduledTitle
      );
      assert.ok(sections[0]?.querySelector('.itin-panel-item'));
      assert.ok(sections[1]?.querySelector('.itin-panel-item'));
   });

   test('buildRemovedItemsPopupSections adds keep buttons for removed animals', () => {
      const keptKeys = new Set();
      const sections = buildRemovedItemsPopupSections({
         removed: {
            animals: [{
               species: 'African Lion',
               exhibit: 'Africa Savanna',
            }],
         },
         onToggleKeepAnimal: (animal) => {
            keptKeys.add(buildSpeciesExhibitKey(animal));
         },
         isKeepAnimalSelected: (key) => keptKeys.has(key),
      });

      const keepButton = sections[0]?.querySelector('.itin-removed-keep-btn');

      assert.ok(keepButton);
      assert.equal(
         keepButton?.textContent,
         APP_STRINGS.itinerary.removedItems.keepInItinerary
      );

      keepButton?.click();

      assert.equal(
         keepButton?.textContent,
         APP_STRINGS.itinerary.dayPlanner.remove
      );
      assert.equal(keepButton?.classList.contains('is-selected'), true);
   });

   test('buildRemovedItemsPopupSections wires view-alternatives actions', () => {
      const viewedSteps = [];

      const sections = buildRemovedItemsPopupSections({
         removed: {
            guardiansTalks: [{
               name: 'African Lion',
               location: 'Africa Savanna',
            }],
         },
         removePopupOnly: () => {},
         onViewAlternatives: (stepKey) => {
            viewedSteps.push(stepKey);
         },
      });

      const alternativesButton = sections[0]?.querySelector('.itin-removed-alt-btn');

      assert.ok(alternativesButton);
      assert.equal(
         alternativesButton?.textContent,
         APP_STRINGS.itinerary.removedItems.viewAlternatives
      );

      alternativesButton?.click();

      assert.deepEqual(viewedSteps, ['guardiansTalks']);
   });
});
