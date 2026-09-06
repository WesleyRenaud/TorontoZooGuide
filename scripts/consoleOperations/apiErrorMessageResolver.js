import { Strings } from '../strings.js';
import { FormatString } from '../strings/formatString.js';

export class ApiErrorMessageResolver {
   static resolveApiErrorMessage(
      apiErrorType,
      apiErrorParams = {},
      strings = Strings.apiErrors
   ) {
      if (!apiErrorType || typeof apiErrorType !== 'string') {
         return null;
      }

      const template = strings[apiErrorType];

      if (typeof template !== 'string') {
         return null;
      }

      return FormatString.formatString(template, apiErrorParams);
   }

   static resolveConsoleMutationError(
      result,
      fallbackMessage = Strings.common.genericFailed
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
