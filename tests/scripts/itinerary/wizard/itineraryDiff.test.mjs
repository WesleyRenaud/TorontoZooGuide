import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryValidationResult } from '../../../../scripts/itinerary/itineraryValidationResult.js';
import { ItineraryNormalizer } from '../../../../scripts/itinerary/itineraryNormalizer.js';
import { ItineraryShape } from '../../../../scripts/itinerary/itineraryShape.js';
import { ItineraryDiff } from '../../../../scripts/itinerary/wizard/itineraryDiff.js';
import { WizardDiffPresenter } from '../../../../scripts/itinerary/wizard/diff/wizardDiffPresenter.js';
import { Position } from '../../../../scripts/shared/enums/position.js';

const _animalVisibilityChangeThreshold = 20;

function _draft(overrides = {}) {
   return ItineraryShape.normalizeItineraryDraft(overrides);
}


test('Test_BuildItineraryDiff_TestSeededRemoved_ExpectRemovedAttractionsAndEncounters', () => {
   const lion = { species: 'African Lion' };
   const carousel = { name: 'Conservation Carousel' };
   const tigerTalk = { name: 'Amur Tiger' };
   const rainforest = { name: 'African Rainforest' };
   const previous = _draft({
      animals: [lion],
      attractions: [carousel],
      guardiansTalks: [tigerTalk],
      wildEncounters: [rainforest],
   });
   const validated = _draft({
      animals: [{ species: ' african lion ' }],
      attractions: [{ name: 'Greenhouse' }],
      guardiansTalks: [tigerTalk],
      wildEncounters: [],
   });

   const diff = ItineraryDiff.buildItineraryDiff(previous, validated, {}, {
      animalVisibilityChangeThreshold: _animalVisibilityChangeThreshold,
   });

   assert.deepEqual(diff.removed.animals, []);
   assert.deepEqual(diff.removed.attractions, [carousel]);
   assert.deepEqual(diff.removed.guardiansTalks, []);
   assert.deepEqual(diff.removed.wildEncounters, [rainforest]);
   assert.equal(WizardDiffPresenter.hasRemovedItems(diff.removed), true);
});


test('Test_BuildItineraryDiff_TestBackendProvided_ExpectBackendRows', () => {
   const lion = { species: 'African Lion' };
   const carousel = { name: 'Conservation Carousel' };

   const diff = ItineraryDiff.buildItineraryDiff(
      _draft({
         animals: [lion],
         attractions: [carousel],
      }),
      _draft({
         animals: [lion],
         attractions: [carousel],
      }),
      {
         attractions: [carousel],
      },
      { animalVisibilityChangeThreshold: _animalVisibilityChangeThreshold }
   );

   assert.deepEqual(diff.removed.attractions, [carousel]);
});


test('Test_BuildItineraryDiff_TestEmptyBackendTalks_ExpectInferredRemoved', () => {
   const talk = { name: 'Only On Mondays' };
   const previous = _draft({
      guardiansTalks: [talk],
   });
   const validated = _draft();

   const diff = ItineraryDiff.buildItineraryDiff(previous, validated, _draft(), {
      animalVisibilityChangeThreshold: _animalVisibilityChangeThreshold,
   });

   assert.deepEqual(diff.removed.guardiansTalks, [talk]);
   assert.equal(WizardDiffPresenter.hasRemovedItems(diff.removed), true);
});


test('Test_BuildItineraryDiff_TestBackendTalkMerge_ExpectMerged', () => {
   const missingTalk = { name: 'Not On New Day Schedule' };
   const cancelledName = 'Cancelled On Schedule';
   const removalReason = 'Cancelled.';
   const cancelledTalk = {
      name: cancelledName,
      removalReason,
   };

   const diff = ItineraryDiff.buildItineraryDiff(
      _draft({
         guardiansTalks: [
            missingTalk,
            { name: cancelledName },
         ],
      }),
      _draft(),
      {
         guardiansTalks: [cancelledTalk],
      },
      { animalVisibilityChangeThreshold: _animalVisibilityChangeThreshold }
   );

   assert.equal(diff.removed.guardiansTalks.length, 2);
   assert.ok(
      diff.removed.guardiansTalks.some(
         (talk) => talk.name === cancelledTalk.name && talk.removalReason === cancelledTalk.removalReason
      )
   );
   assert.ok(diff.removed.guardiansTalks.some((talk) => talk.name === missingTalk.name));
});


test('Test_BuildItineraryDiff_TestVisibilityDelta_ExpectReducedAndImproved', () => {
   const lion = { species: 'African Lion', likelihood: 90 };
   const tiger = { species: 'Amur Tiger', likelihood: 0.25 };
   const leopard = { species: 'Snow Leopard', likelihood: 70 };
   const previous = _draft({
      animals: [lion, tiger, leopard],
   });
   const validated = _draft({
      animals: [
         { species: lion.species, likelihood: 60 },
         { species: tiger.species, likelihood: 0.7 },
         { species: leopard.species, likelihood: 55 },
      ],
   });

   const diff = ItineraryDiff.buildItineraryDiff(previous, validated, {}, {
      animalVisibilityChangeThreshold: _animalVisibilityChangeThreshold,
   });

   assert.deepEqual(
      diff.reducedVisibility.animals.map((animal) => animal.species),
      [lion.species]
   );
   assert.deepEqual(
      diff.improvedVisibility.animals.map((animal) => animal.species),
      [tiger.species]
   );
   assert.equal(WizardDiffPresenter.hasReducedVisibility(diff.reducedVisibility), true);
   assert.equal(WizardDiffPresenter.hasImprovedVisibility(diff.improvedVisibility), true);
   assert.equal(diff.reducedVisibility.animals[Position.FIRST].species, lion.species);
   assert.equal(diff.improvedVisibility.animals[Position.FIRST].species, tiger.species);
});


test('Test_BuildItineraryDiff_TestLostTimes_ExpectUnscheduled', () => {
   const lionSpecies = 'African Lion';
   const carouselName = 'Conservation Carousel';
   const exhibit = 'Africa Savanna';

   const diff = ItineraryDiff.buildItineraryDiff(
      _draft({
         animals: [
            {
               species: lionSpecies,
               exhibit,
               start_time: '09:00',
               end_time: '09:08',
            },
         ],
         attractions: [
            {
               name: carouselName,
               start_time: '09:08',
               end_time: '09:16',
            },
         ],
      }),
      _draft({
         animals: [
            {
               species: lionSpecies,
               exhibit,
               start_time: '',
               end_time: '',
            },
         ],
         attractions: [
            {
               name: carouselName,
               start_time: '',
               end_time: '',
            },
         ],
      }),
      {},
      { animalVisibilityChangeThreshold: _animalVisibilityChangeThreshold }
   );

   assert.deepEqual(
      diff.unscheduled.animals.map((animal) => animal.species),
      [lionSpecies]
   );
   assert.deepEqual(
      diff.unscheduled.attractions.map((attraction) => attraction.name),
      [carouselName]
   );
   assert.equal(WizardDiffPresenter.hasUnscheduledItems(diff.unscheduled), true);
});


test('Test_BuildItineraryDiff_TestDeletedTalks_ExpectNotUnscheduled', () => {
   const talkName = 'Spotted Hyena';
   const location = 'Africa Savanna';

   const diff = ItineraryDiff.buildItineraryDiff(
      _draft({
         guardiansTalks: [
            {
               name: talkName,
               start_time: '13:00',
               end_time: '13:30',
               location,
            },
         ],
      }),
      _draft({
         guardiansTalks: [
            {
               name: talkName,
               is_deleted: true,
               location,
            },
         ],
      }),
      {},
      { animalVisibilityChangeThreshold: _animalVisibilityChangeThreshold }
   );

   assert.equal(diff.unscheduled.guardiansTalks, undefined);
   assert.deepEqual(diff.removed.guardiansTalks, []);
});


test('Test_BuildItineraryDiff_TestDeletedEncounters_ExpectNotUnscheduled', () => {
   const encounterName = 'African Rainforest';

   const diff = ItineraryDiff.buildItineraryDiff(
      _draft({
         wildEncounters: [
            {
               name: encounterName,
               start_time: '13:00',
               end_time: '13:45',
            },
         ],
      }),
      _draft({
         wildEncounters: [
            {
               name: encounterName,
               is_deleted: true,
            },
         ],
      }),
      {},
      { animalVisibilityChangeThreshold: _animalVisibilityChangeThreshold }
   );

   assert.equal(diff.unscheduled.wildEncounters, undefined);
   assert.deepEqual(diff.removed.wildEncounters, []);
});


test('Test_ApplyItineraryDiffToValidation_TestPriorRemoved_ExpectPreserved', () => {
   const talkName = 'Spotted Hyena';
   const location = 'Africa Savanna';
   const previous = _draft({
      date: '2026-06-21',
      guardiansTalks: [
         {
            name: talkName,
            start_time: '13:00',
            end_time: '13:30',
            location,
         },
      ],
   });
   const validatedItinerary = ItineraryNormalizer.normalizeItinerary({
      date: '2026-06-22',
      guardiansTalks: [
         {
            name: talkName,
            is_deleted: true,
            location,
         },
      ],
   });
   const diff = ItineraryDiff.buildItineraryDiff(
      previous,
      validatedItinerary,
      {},
      validatedItinerary.itineraryConfig ?? {}
   );

   ItineraryValidationResult.applyItineraryDiffToValidation(validatedItinerary, diff);

   assert.equal(validatedItinerary.validation.unscheduled.guardiansTalks, undefined);
   assert.deepEqual(
      validatedItinerary.validation.removed.guardiansTalks.map((talk) => talk.name),
      [talkName]
   );
   assert.equal(WizardDiffPresenter.hasUnscheduledItems(validatedItinerary.validation.unscheduled), false);
   assert.equal(WizardDiffPresenter.hasRemovedItems(validatedItinerary.validation.removed), true);
   assert.equal(
      validatedItinerary.validation.removed.guardiansTalks[Position.FIRST].name,
      talkName
   );
});


test('Test_BuildItineraryDiff_TestDroppedTalksEncounters_ExpectRemoved', () => {
   const talkName = 'African Lion';
   const encounterName = 'African Rainforest';

   const diff = ItineraryDiff.buildItineraryDiff(
      _draft({
         guardiansTalks: [
            {
               name: talkName,
               start_time: '16:30',
               end_time: '16:45',
            },
         ],
         wildEncounters: [
            {
               name: encounterName,
               start_time: '16:30',
               end_time: '16:45',
            },
         ],
      }),
      _draft(),
      {},
      { animalVisibilityChangeThreshold: _animalVisibilityChangeThreshold }
   );

   assert.deepEqual(
      diff.removed.guardiansTalks.map((talk) => talk.name),
      [talkName]
   );
   assert.deepEqual(
      diff.removed.wildEncounters.map((encounter) => encounter.name),
      [encounterName]
   );
   assert.equal(WizardDiffPresenter.hasRemovedItems(diff.removed), true);
   assert.equal(WizardDiffPresenter.hasUnscheduledItems(diff.unscheduled), false);
});


test('Test_BuildItineraryDiff_TestMatchingAttraction_ExpectTransportKept', () => {
   const transportationName = 'Zoomobile';
   const previous = _draft({
      attractions: [{ name: transportationName, addedAsAttraction: true }],
   });
   const validated = _draft({
      transportations: [{
         name: transportationName,
         added_as_attraction: true,
      }],
   });

   const diff = ItineraryDiff.buildItineraryDiff(previous, validated);

   assert.deepEqual(diff.removed.attractions, []);
   assert.equal(WizardDiffPresenter.hasRemovedItems(diff.removed), false);
   assert.equal(WizardDiffPresenter.isValidatedItineraryEmpty(validated), false);
});


test('Test_BuildItineraryDiff_TestTransportOnly_ExpectAttractionRemoved', () => {
   const transportationName = 'Zoomobile';
   const attraction = { name: transportationName, addedAsAttraction: true };
   const previous = _draft({
      attractions: [attraction],
   });
   const validated = _draft({
      transportations: [{
         name: transportationName,
         added_as_attraction: false,
      }],
   });

   const diff = ItineraryDiff.buildItineraryDiff(previous, validated);

   assert.deepEqual(diff.removed.attractions, [attraction]);
   assert.equal(WizardDiffPresenter.hasRemovedItems(diff.removed), true);
});


test('Test_IsValidatedItineraryEmpty_TestNull_ExpectTrue', () => {
   const itinerary = null;

   const isEmpty = WizardDiffPresenter.isValidatedItineraryEmpty(itinerary);

   assert.equal(isEmpty, true);
});


test('Test_IsValidatedItineraryEmpty_TestEmptyDraft_ExpectTrue', () => {
   const itinerary = _draft();

   const isEmpty = WizardDiffPresenter.isValidatedItineraryEmpty(itinerary);

   assert.equal(isEmpty, true);
});


test('Test_IsValidatedItineraryEmpty_TestAnimals_ExpectFalse', () => {
   const itinerary = _draft({
      animals: [{ species: 'African Lion' }],
   });

   const isEmpty = WizardDiffPresenter.isValidatedItineraryEmpty(itinerary);

   assert.equal(isEmpty, false);
});


test('Test_IsValidatedItineraryEmpty_TestTransportations_ExpectFalse', () => {
   const itinerary = _draft({
      transportations: [{ name: 'Zoomobile' }],
   });

   const isEmpty = WizardDiffPresenter.isValidatedItineraryEmpty(itinerary);

   assert.equal(isEmpty, false);
});


test('Test_HasRemovedItems_TestNull_ExpectFalse', () => {
   const removed = null;

   const hasRemoved = WizardDiffPresenter.hasRemovedItems(removed);

   assert.equal(hasRemoved, false);
});


test('Test_HasUnscheduledItems_TestNull_ExpectFalse', () => {
   const unscheduled = null;

   const hasUnscheduled = WizardDiffPresenter.hasUnscheduledItems(unscheduled);

   assert.equal(hasUnscheduled, false);
});


test('Test_HasReducedVisibility_TestEmptyAnimals_ExpectFalse', () => {
   const reduced = { animals: [] };

   const hasReduced = WizardDiffPresenter.hasReducedVisibility(reduced);

   assert.equal(hasReduced, false);
});


test('Test_HasImprovedVisibility_TestEmptyAnimals_ExpectFalse', () => {
   const improved = { animals: [] };

   const hasImproved = WizardDiffPresenter.hasImprovedVisibility(improved);

   assert.equal(hasImproved, false);
});
