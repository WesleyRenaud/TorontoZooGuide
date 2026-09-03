import assert from 'node:assert/strict';
import test from 'node:test';

import { ApiErrorMessageResolver } from '../../../scripts/consoleOperations/apiErrorMessageResolver.js';

test('Test_ResolveApiErrorMessage_TestCatalogTemplate_ExpectFormattedMessage', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveApiErrorMessage('couldNotSetClosed', { name: 'Africa Savanna' }),
      'Could not set "Africa Savanna" as closed.'
   );
});

test('Test_ResolveConsoleMutationError_TestSpeciesMissing_ExpectCatalogMessage', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({
         success: false,
         apiErrorType: 'noAnimalFoundWithSpecies',
         apiErrorParams: { species: 'Giraffe' },
      }),
      'No animal found with species "Giraffe".'
   );
});

test('Test_ResolveConsoleMutationError_TestInvalidAttractionHours_ExpectCatalogMessage', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({
         success: false,
         apiErrorType: 'invalidAttractionHours',
      }),
      'Attraction hours must fall within regular zoo hours for the selected date range.'
   );
});

test('Test_ResolveConsoleMutationError_TestHoursBounds_ExpectCatalogMessage', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({
         success: false,
         apiErrorType: 'couldNotResolveAttractionHoursTimeBounds',
      }),
      'Could not resolve zoo hours bounds for attraction hours.'
   );
});

test('Test_ResolveConsoleMutationError_TestMissingApiError_ExpectFallback', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({ success: false }, 'fallback'),
      'fallback'
   );
});
