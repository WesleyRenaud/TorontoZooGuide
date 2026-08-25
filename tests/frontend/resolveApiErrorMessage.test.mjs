import assert from 'node:assert/strict';
import test from 'node:test';

import {
   resolveApiErrorMessage,
   resolveConsoleMutationError,
} from '../../scripts/consoleOperations/resolveApiErrorMessage.js';

test('resolveApiErrorMessage formats api error templates from the catalog', () => {
   assert.equal(
      resolveApiErrorMessage('couldNotSetClosed', { name: 'Africa Savanna' }),
      'Could not set "Africa Savanna" as closed.'
   );
});

test('resolveConsoleMutationError resolves apiErrorType payloads', () => {
   assert.equal(
      resolveConsoleMutationError({
         success: false,
         apiErrorType: 'noAnimalFoundWithSpecies',
         apiErrorParams: { species: 'Giraffe' },
      }),
      'No animal found with species "Giraffe".'
   );
});

test('resolveConsoleMutationError resolves invalid attraction hours errors', () => {
   assert.equal(
      resolveConsoleMutationError({
         success: false,
         apiErrorType: 'invalidAttractionHours',
      }),
      'Attraction hours must fall within regular zoo hours for the selected date range.'
   );
});

test('resolveConsoleMutationError resolves attraction hours time bounds errors', () => {
   assert.equal(
      resolveConsoleMutationError({
         success: false,
         apiErrorType: 'couldNotResolveAttractionHoursTimeBounds',
      }),
      'Could not resolve zoo hours bounds for attraction hours.'
   );
});

test('resolveConsoleMutationError falls back when api error is missing', () => {
   assert.equal(
      resolveConsoleMutationError({ success: false }, 'fallback'),
      'fallback'
   );
});
