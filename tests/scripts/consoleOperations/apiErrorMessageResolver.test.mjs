import assert from 'node:assert/strict';
import test from 'node:test';

import { ApiErrorMessageResolver } from '../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ApiErrorType } from '../../../scripts/shared/enums/apiErrorType.js';

test('Test_ResolveApiErrorMessage_TestCatalogTemplate_ExpectFormattedMessage', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveApiErrorMessage(
         ApiErrorType.COULD_NOT_SET_CLOSED,
         { name: 'Africa Savanna' }
      ),
      'Could not set "Africa Savanna" as closed.'
   );
});

test('Test_ResolveApiErrorMessage_TestInvalidTypeOrTemplate_ExpectNull', () => {
   assert.equal(ApiErrorMessageResolver.resolveApiErrorMessage(null), null);
   assert.equal(ApiErrorMessageResolver.resolveApiErrorMessage(12), null);
   assert.equal(ApiErrorMessageResolver.resolveApiErrorMessage('unknownErrorType'), null);
});

test('Test_ResolveConsoleMutationError_TestSpeciesMissing_ExpectCatalogMessage', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({
         success: false,
         apiErrorType: ApiErrorType.NO_ANIMAL_FOUND_WITH_SPECIES,
         apiErrorParams: { species: 'Giraffe' },
      }),
      'No animal found with species "Giraffe".'
   );
});

test('Test_ResolveConsoleMutationError_TestInvalidAttractionHours_ExpectCatalogMessage', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({
         success: false,
         apiErrorType: ApiErrorType.INVALID_ATTRACTION_HOURS,
      }),
      'Attraction hours must fall within regular zoo hours for the selected date range.'
   );
});

test('Test_ResolveConsoleMutationError_TestHoursBounds_ExpectCatalogMessage', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({
         success: false,
         apiErrorType: ApiErrorType.COULD_NOT_RESOLVE_ATTRACTION_HOURS_TIME_BOUNDS,
      }),
      'Could not resolve zoo hours bounds for attraction hours.'
   );
});

test('Test_ResolveConsoleMutationError_TestMissingApiError_ExpectFallback', () => {
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({ success: false }, 'fallback'),
      'fallback'
   );
   assert.equal(
      ApiErrorMessageResolver.resolveConsoleMutationError({
         success: false,
         apiErrorType: 'unknownErrorType',
      }, 'fallback'),
      'fallback'
   );
});
