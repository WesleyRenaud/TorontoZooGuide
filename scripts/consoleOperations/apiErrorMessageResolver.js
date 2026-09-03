import { APP_STRINGS } from '../strings.js';
import { formatString } from '../strings/formatString.js';

export class ApiErrorMessageResolver {
   static resolveApiErrorMessage(
      apiErrorType,
      apiErrorParams = {},
      strings = APP_STRINGS.apiErrors
   ) {
      if (!apiErrorType || typeof apiErrorType !== 'string') {
         return null;
      }

      const template = strings[apiErrorType];

      if (typeof template !== 'string') {
         return null;
      }

      return formatString(template, apiErrorParams);
   }

   static resolveConsoleMutationError(
      result,
      fallbackMessage = APP_STRINGS.common.genericFailed
   ) {
      if (!result?.apiErrorType) {
         return fallbackMessage;
      }

      return ApiErrorMessageResolver.resolveApiErrorMessage(
         result.apiErrorType,
         result.apiErrorParams
      ) ?? fallbackMessage;
   }
}
