import assert from 'node:assert/strict';
import { test } from 'node:test';

import { OpenTimelineView } from '../../../../../scripts/itinerary/panel/components/openTimelineView.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_MakeOpenPill_TestEmptyLabel_ExpectNull', () => {
   const label = '';

   const pill = OpenTimelineView.makeOpenPill(label);

   assert.equal(pill, null);
});


test('Test_MakeOpenPill_TestNullLabel_ExpectNull', () => {
   const label = null;

   const pill = OpenTimelineView.makeOpenPill(label);

   assert.equal(pill, null);
});


test('Test_MakeOpenPill_TestNoRemove_ExpectCompact', () => {
   const label = 'Tundra Grill';

   const pill = OpenTimelineView.makeOpenPill(label);

   assert.ok(pill.classList.contains('itinerary-day-open-pill'));
   assert.equal(pill.classList.contains('itinerary-day-open-pill--with-menu'), false);
   assert.equal(pill.querySelector('.itinerary-day-open-pill-label')?.textContent, label);
   assert.equal(pill.querySelector('.itinerary-day-open-pill-menu'), null);
});


test('Test_MakeOpenPill_TestOnRemove_ExpectMenu', () => {
   const label = 'Breakfast';
   const menuAriaLabel = 'Breakfast options';
   const removeLabel = 'Remove';

   const pill = OpenTimelineView.makeOpenPill(label, {
      onRemove: () => {},
      menuAriaLabel,
      removeLabel,
   });

   assert.ok(pill.classList.contains('itinerary-day-open-pill--with-menu'));
   assert.equal(
      pill.querySelector('.itinerary-day-open-pill-menu-btn')?.getAttribute('aria-label'),
      menuAriaLabel
   );
   assert.equal(
      pill.querySelector('.itinerary-day-open-pill-menu-item')?.textContent,
      removeLabel
   );
   assert.equal(pill.querySelector('.itinerary-day-open-pill-menu-panel')?.hidden, true);
});


test('Test_MakeBoundaryMarker_TestEmptyLabel_ExpectNull', () => {
   const label = '';

   const marker = OpenTimelineView.makeBoundaryMarker(label);

   assert.equal(marker, null);
});


test('Test_MakeBoundaryMarker_TestDefault_ExpectArrival', () => {
   const label = 'Arrival';

   const marker = OpenTimelineView.makeBoundaryMarker(label);

   assert.ok(marker.classList.contains('itinerary-day-boundary-marker'));
   assert.equal(marker.getAttribute('aria-label'), label);
   assert.equal(marker.getAttribute('data-boundary-marker-kind'), 'arrival');
   assert.ok(marker.querySelector('.itinerary-day-boundary-marker-icon'));
   assert.equal(marker.querySelector('.itinerary-day-boundary-marker-btn'), null);
});


test('Test_MakeBoundaryMarker_TestStartsAtAnchor_ExpectDeparture', () => {
   const label = 'Departure';
   const visitBoundaryPlacement = 'starts-at-anchor';

   const marker = OpenTimelineView.makeBoundaryMarker(label, {
      visitBoundaryPlacement,
   });

   assert.equal(marker.getAttribute('data-boundary-marker-kind'), 'departure');
});


test('Test_MakeBoundaryMarker_TestOnRemove_ExpectMenu', () => {
   const label = 'Arrival';
   const menuAriaLabel = 'Arrival options';
   const removeLabel = 'Clear arrival';

   const marker = OpenTimelineView.makeBoundaryMarker(label, {
      onRemove: () => {},
      menuAriaLabel,
      removeLabel,
   });

   assert.ok(marker.classList.contains('itinerary-day-boundary-marker--with-menu'));
   assert.equal(
      marker.querySelector('.itinerary-day-boundary-marker-btn')?.getAttribute('aria-label'),
      menuAriaLabel
   );
   assert.equal(
      marker.querySelector('.itinerary-day-open-pill-menu-item')?.textContent,
      removeLabel
   );
});
