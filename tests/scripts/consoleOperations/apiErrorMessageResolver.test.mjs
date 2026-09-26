import assert from 'node:assert/strict';
import test from 'node:test';

import { ApiErrorMessageResolver } from '../../../scripts/consoleOperations/apiErrorMessageResolver.js';
import { ApiErrorType } from '../../../scripts/shared/enums/apiErrorType.js';
import { FormatString } from '../../../scripts/strings/formatString.js';
import { Strings } from '../../../scripts/strings.js';


test('Test_ResolveApiErrorMessage_TestCatalogTemplate_ExpectFormattedMessage', () => {
   const name = 'Africa Savanna';
   const apiErrorType = ApiErrorType.COULD_NOT_SET_CLOSED;
   const apiErrorParams = { name };

   const message = ApiErrorMessageResolver.resolveApiErrorMessage(apiErrorType, apiErrorParams);

   assert.equal(
      message,
      FormatString.formatString(Strings.apiErrors[apiErrorType], apiErrorParams)
   );
});


test('Test_ResolveApiErrorMessage_TestNull_ExpectNull', () => {
   const apiErrorType = null;

   const message = ApiErrorMessageResolver.resolveApiErrorMessage(apiErrorType);

   assert.equal(message, null);
});


test('Test_ResolveApiErrorMessage_TestNumber_ExpectNull', () => {
   const apiErrorType = 12;

   const message = ApiErrorMessageResolver.resolveApiErrorMessage(apiErrorType);

   assert.equal(message, null);
});


test('Test_ResolveApiErrorMessage_TestUnknownType_ExpectNull', () => {
   const apiErrorType = 'unknownErrorType';

   const message = ApiErrorMessageResolver.resolveApiErrorMessage(apiErrorType);

   assert.equal(message, null);
});


test('Test_ResolveConsoleMutationError_TestSpeciesMissing_ExpectCatalogMessage', () => {
   const species = 'Giraffe';
   const apiErrorType = ApiErrorType.NO_ANIMAL_FOUND_WITH_SPECIES;
   const apiErrorParams = { species };
   const result = {
      success: false,
      apiErrorType,
      apiErrorParams,
   };

   const message = ApiErrorMessageResolver.resolveConsoleMutationError(result);

   assert.equal(
      message,
      FormatString.formatString(Strings.apiErrors[apiErrorType], apiErrorParams)
   );
});


test('Test_ResolveConsoleMutationError_TestInvalidAttractionHours_ExpectCatalogMessage', () => {
   const apiErrorType = ApiErrorType.INVALID_ATTRACTION_HOURS;
   const result = {
      success: false,
      apiErrorType,
   };

   const message = ApiErrorMessageResolver.resolveConsoleMutationError(result);

   assert.equal(message, Strings.apiErrors[apiErrorType]);
});


test('Test_ResolveConsoleMutationError_TestHoursBounds_ExpectCatalogMessage', () => {
   const apiErrorType = ApiErrorType.COULD_NOT_RESOLVE_ATTRACTION_HOURS_TIME_BOUNDS;
   const result = {
      success: false,
      apiErrorType,
   };

   const message = ApiErrorMessageResolver.resolveConsoleMutationError(result);

   assert.equal(message, Strings.apiErrors[apiErrorType]);
});


test('Test_ResolveConsoleMutationError_TestMissingApiError_ExpectFallback', () => {
   const fallbackMessage = 'fallback';
   const result = { success: false };

   const message = ApiErrorMessageResolver.resolveConsoleMutationError(result, fallbackMessage);

   assert.equal(message, fallbackMessage);
});


test('Test_ResolveConsoleMutationError_TestUnknownType_ExpectFallback', () => {
   const fallbackMessage = 'fallback';
   const result = {
      success: false,
      apiErrorType: 'unknownErrorType',
   };

   const message = ApiErrorMessageResolver.resolveConsoleMutationError(result, fallbackMessage);

   assert.equal(message, fallbackMessage);
});
