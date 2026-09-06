import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RemovedItemsPopupContent } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupContent.js';
import { RemovedItemsPopupSectionSpecs } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupSectionSpecs.js';
import { ItineraryAdjustmentTypes } from '../../../../../scripts/itinerary/itineraryAdjustmentTypes.js';
import { SpeciesExhibitKey } from '../../../../../scripts/itinerary/speciesExhibitKey.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

test('Test_RemovedItemsPopupSectionSpecs_TestRemovedItemsPopupSectionSpecsHasRemovedItemsPopupContentReportsRemovedAnimals_ExpectOk', () => {
   assert.equal(
      RemovedItemsPopupSectionSpecs.hasRemovedItemsPopupContent({
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
         ItineraryAdjustmentTypes.updateItineraryAdjustmentTypesFromConfig({
            adjustmentTypes: {
               ARRIVAL_TIME_ADJUSTED: 'arrivalTimeAdjusted',
               DEPARTURE_TIME_ADJUSTED: 'departureTimeAdjusted',
            },
         });
      },
   });

   test('Test_BuildRemovedItemsPopupSections_TestBuildRemovedItemsPopupSectionsRendersAdjustmentAndUnscheduledSections_ExpectOk', () => {
      const sections = RemovedItemsPopupContent.buildRemovedItemsPopupSections({
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
         Strings.itinerary.removedItems.itineraryTimesTitle
      );
      assert.equal(
         sections[1]?.querySelector('.itin-removed-section-title')?.textContent,
         Strings.itinerary.dayPlanner.unscheduledTitle
      );
      assert.ok(sections[0]?.querySelector('.itin-panel-item'));
      assert.ok(sections[1]?.querySelector('.itin-panel-item'));
   });

   test('Test_BuildRemovedItemsPopupSections_TestBuildRemovedItemsPopupSectionsAddsKeepButtonsForRemovedAnimals_ExpectOk', () => {
      const keptKeys = new Set();
      const sections = RemovedItemsPopupContent.buildRemovedItemsPopupSections({
         removed: {
            animals: [{
               species: 'African Lion',
               exhibit: 'Africa Savanna',
            }],
         },
         onToggleKeepAnimal: (animal) => {
            keptKeys.add(SpeciesExhibitKey.buildSpeciesExhibitKey(animal));
         },
         isKeepAnimalSelected: (key) => keptKeys.has(key),
      });

      const keepButton = sections[0]?.querySelector('.itin-removed-keep-btn');

      assert.ok(keepButton);
      assert.equal(
         keepButton?.textContent,
         Strings.itinerary.removedItems.keepInItinerary
      );

      keepButton?.click();

      assert.equal(
         keepButton?.textContent,
         Strings.itinerary.dayPlanner.remove
      );
      assert.equal(keepButton?.classList.contains('is-selected'), true);
   });

   test('Test_BuildRemovedItemsPopupSections_TestBuildRemovedItemsPopupSectionsWiresViewAlternativesActions_ExpectOk', () => {
      const viewedSteps = [];

      const sections = RemovedItemsPopupContent.buildRemovedItemsPopupSections({
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
         Strings.itinerary.removedItems.viewAlternatives
      );

      alternativesButton?.click();

      assert.deepEqual(viewedSteps, ['guardiansTalks']);
   });
});
