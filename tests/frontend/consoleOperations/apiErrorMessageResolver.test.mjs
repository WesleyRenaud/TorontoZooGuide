import assert from 'node:assert/strict';
import test from 'node:test';

import { ApiErrorMessageResolver } from '../../../scripts/consoleOperations/apiErrorMessageResolver.js';

test('ApiErrorMessageResolver.resolveApiErrorMessage formats api error templates from the catalog', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveApiErrorMessage('couldNotSetClosed', { name: 'Africa Savanna' }),
      'Could not set "Africa Savanna" as closed.'
   );
});

test('ApiErrorMessageResolver.resolveConsoleMutationError resolves apiErrorType payloads', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({
         success: false,
         apiErrorType: 'noAnimalFoundWithSpecies',
         apiErrorParams: { species: 'Giraffe' },
      }),
      'No animal found with species "Giraffe".'
   );
});

test('ApiErrorMessageResolver.resolveConsoleMutationError resolves invalid attraction hours errors', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({
         success: false,
         apiErrorType: 'invalidAttractionHours',
      }),
      'Attraction hours must fall within regular zoo hours for the selected date range.'
   );
});

test('ApiErrorMessageResolver.resolveConsoleMutationError resolves attraction hours time bounds errors', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({
         success: false,
         apiErrorType: 'couldNotResolveAttractionHoursTimeBounds',
      }),
      'Could not resolve zoo hours bounds for attraction hours.'
   );
});

test('ApiErrorMessageResolver.resolveConsoleMutationError falls back when api error is missing', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({ success: false }, 'fallback'),
      'fallback'
   );
});
