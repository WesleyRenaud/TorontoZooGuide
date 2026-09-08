import assert from 'node:assert/strict';
import { test } from 'node:test';

import { OpenTimelineView } from '../../../../../scripts/itinerary/panel/components/openTimelineView.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_MakeOpenPill_TestEmptyLabel_ExpectNull', () => {
   assert.equal(OpenTimelineView.makeOpenPill(''), null);
   assert.equal(OpenTimelineView.makeOpenPill(null), null);
});

test('Test_MakeOpenPill_TestNoRemove_ExpectCompact', () => {
   const pill = OpenTimelineView.makeOpenPill('Lunch');

   assert.ok(pill.classList.contains('itinerary-day-open-pill'));
   assert.equal(pill.classList.contains('itinerary-day-open-pill--with-menu'), false);
   assert.equal(
      pill.querySelector('.itinerary-day-open-pill-label')?.textContent,
      'Lunch'
   );
   assert.equal(pill.querySelector('.itinerary-day-open-pill-menu'), null);
});

test('Test_MakeOpenPill_TestOnRemove_ExpectMenu', () => {
   const pill = OpenTimelineView.makeOpenPill('Breakfast', {
      onRemove: () => {},
      menuAriaLabel: 'Breakfast options',
      removeLabel: 'Remove',
   });

   assert.ok(pill.classList.contains('itinerary-day-open-pill--with-menu'));
   assert.equal(
      pill.querySelector('.itinerary-day-open-pill-menu-btn')?.getAttribute('aria-label'),
      'Breakfast options'
   );
   assert.equal(
      pill.querySelector('.itinerary-day-open-pill-menu-item')?.textContent,
      'Remove'
   );
   assert.equal(
      pill.querySelector('.itinerary-day-open-pill-menu-panel')?.hidden,
      true
   );
});

test('Test_MakeBoundaryMarker_TestEmptyLabel_ExpectNull', () => {
   assert.equal(OpenTimelineView.makeBoundaryMarker(''), null);
});

test('Test_MakeBoundaryMarker_TestDefault_ExpectArrival', () => {
   const marker = OpenTimelineView.makeBoundaryMarker('Arrival');

   assert.ok(marker.classList.contains('itinerary-day-boundary-marker'));
   assert.equal(marker.getAttribute('aria-label'), 'Arrival');
   assert.equal(marker.getAttribute('data-boundary-marker-kind'), 'arrival');
   assert.ok(marker.querySelector('.itinerary-day-boundary-marker-icon'));
   assert.equal(marker.querySelector('.itinerary-day-boundary-marker-btn'), null);
});

test('Test_MakeBoundaryMarker_TestStartsAtAnchor_ExpectDeparture', () => {
   const marker = OpenTimelineView.makeBoundaryMarker('Departure', {
      visitBoundaryPlacement: 'starts-at-anchor',
   });

   assert.equal(marker.getAttribute('data-boundary-marker-kind'), 'departure');
});

test('Test_MakeBoundaryMarker_TestOnRemove_ExpectMenu', () => {
   const marker = OpenTimelineView.makeBoundaryMarker('Arrival', {
      onRemove: () => {},
      menuAriaLabel: 'Arrival options',
      removeLabel: 'Clear arrival',
   });

   assert.ok(marker.classList.contains('itinerary-day-boundary-marker--with-menu'));
   assert.equal(
      marker.querySelector('.itinerary-day-boundary-marker-btn')?.getAttribute('aria-label'),
      'Arrival options'
   );
   assert.equal(
      marker.querySelector('.itinerary-day-open-pill-menu-item')?.textContent,
      'Clear arrival'
   );
});
