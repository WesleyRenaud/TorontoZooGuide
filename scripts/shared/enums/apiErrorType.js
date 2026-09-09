import apiErrorTypeValues from '../../../shared/enums/apiErrorType.json' with { type: 'json' };

export class ApiErrorType {
   static {
      Object.assign(ApiErrorType, apiErrorTypeValues);
   }
}
