import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   makeBoundaryMarker,
   makeOpenPill,
} from '../../scripts/itinerary/panel/components/openTimelinePill.js';

test('makeOpenPill returns null for an empty label', () => {
   assert.equal(makeOpenPill(''), null);
   assert.equal(makeOpenPill(null), null);
});

test('makeOpenPill keeps a compact pill without a remove handler', () => {
   const pill = makeOpenPill('Lunch');

   assert.ok(pill.classList.contains('itinerary-day-open-pill'));
   assert.equal(pill.classList.contains('itinerary-day-open-pill--with-menu'), false);
   assert.equal(
      pill.querySelector('.itinerary-day-open-pill-label')?.textContent,
      'Lunch'
   );
   assert.equal(pill.querySelector('.itinerary-day-open-pill-menu'), null);
});

test('makeOpenPill adds a remove menu when onRemove is provided', () => {
   const pill = makeOpenPill('Breakfast', {
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

test('makeBoundaryMarker returns null for an empty label', () => {
   assert.equal(makeBoundaryMarker(''), null);
});

test('makeBoundaryMarker renders a read-only arrival marker by default', () => {
   const marker = makeBoundaryMarker('Arrival');

   assert.ok(marker.classList.contains('itinerary-day-boundary-marker'));
   assert.equal(marker.getAttribute('aria-label'), 'Arrival');
   assert.equal(marker.getAttribute('data-boundary-marker-kind'), 'arrival');
   assert.ok(marker.querySelector('.itinerary-day-boundary-marker-icon'));
   assert.equal(marker.querySelector('.itinerary-day-boundary-marker-btn'), null);
});

test('makeBoundaryMarker renders a departure marker for starts-at-anchor placement', () => {
   const marker = makeBoundaryMarker('Departure', {
      visitBoundaryPlacement: 'starts-at-anchor',
   });

   assert.equal(marker.getAttribute('data-boundary-marker-kind'), 'departure');
});

test('makeBoundaryMarker adds a remove menu when onRemove is provided', () => {
   const marker = makeBoundaryMarker('Arrival', {
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
