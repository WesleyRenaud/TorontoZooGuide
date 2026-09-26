import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RemovedItemsPopupView } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupView.js';
import { RemovedItemsPopupSectionBuilder } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupSectionBuilder.js';
import { SpeciesExhibitKey } from '../../../../../scripts/itinerary/speciesExhibitKey.js';
import { ItineraryAdjustmentType } from '../../../../../scripts/shared/enums/itineraryAdjustmentType.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_HasRemovedItemsPopupContent_TestRemovedAnimals_ExpectTrue', () => {
   const species = 'African Lion';
   const exhibit = 'Savanna';

   const hasContent = RemovedItemsPopupSectionBuilder.hasRemovedItemsPopupContent({
      removed: {
         animals: [{ species, exhibit }],
      },
   });

   assert.equal(hasContent, true);
});


test('Test_BuildRemovedItemsPopupSections_TestAdjustmentAndUnscheduled_ExpectSections', () => {
   const previousValue = '09:00';
   const value = '09:30';
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';

   const sections = RemovedItemsPopupView.buildRemovedItemsPopupSections({
      adjustments: [{
         type: ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
         previousValue,
         value,
      }],
      unscheduled: {
         animals: [{
            species,
            exhibit,
         }],
      },
   });

   assert.equal(sections.length, 2);
   assert.equal(
      sections.at(Position.FIRST)?.querySelector('.itin-removed-section-title')?.textContent,
      Strings.itinerary.removedItems.itineraryTimesTitle
   );
   assert.equal(
      sections.at(Position.SECOND)?.querySelector('.itin-removed-section-title')?.textContent,
      Strings.itinerary.dayPlanner.unscheduledTitle
   );
   assert.ok(sections.at(Position.FIRST)?.querySelector('.itin-panel-item'));
   assert.ok(sections.at(Position.SECOND)?.querySelector('.itin-panel-item'));
});


test('Test_BuildRemovedItemsPopupSections_TestRemovedAnimals_ExpectKeepButtons', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const animal = { species, exhibit };
   const keptKeys = new Set();

   const sections = RemovedItemsPopupView.buildRemovedItemsPopupSections({
      removed: {
         animals: [animal],
      },
      onToggleKeepAnimal: (keptAnimal) => {
         keptKeys.add(SpeciesExhibitKey.buildSpeciesExhibitKey(keptAnimal));
      },
      isKeepAnimalSelected: (key) => keptKeys.has(key),
   });
   const keepButton = sections.at(Position.FIRST)?.querySelector('.itin-removed-keep-btn');

   assert.ok(keepButton);
   assert.equal(
      keepButton?.textContent,
      Strings.itinerary.removedItems.keepInItinerary
   );
   keepButton?.click();
   assert.equal(keepButton?.textContent, Strings.itinerary.dayPlanner.remove);
   assert.equal(keepButton?.classList.contains('is-selected'), true);
});


test('Test_BuildRemovedItemsPopupSections_TestViewAlternatives_ExpectStep', () => {
   const viewedSteps = [];
   const talkName = 'African Lion';
   const location = 'Africa Savanna';

   const sections = RemovedItemsPopupView.buildRemovedItemsPopupSections({
      removed: {
         guardiansTalks: [{
            name: talkName,
            location,
         }],
      },
      removePopupOnly: () => {},
      onViewAlternatives: (stepKey) => {
         viewedSteps.push(stepKey);
      },
   });
   const alternativesButton = sections.at(Position.FIRST)?.querySelector('.itin-removed-alt-btn');
   alternativesButton?.click();

   assert.ok(alternativesButton);
   assert.equal(
      alternativesButton?.textContent,
      Strings.itinerary.removedItems.viewAlternatives
   );
   assert.deepEqual(viewedSteps, ['guardiansTalks']);
});
