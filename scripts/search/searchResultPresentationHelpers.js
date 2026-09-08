export class SearchResultPresentationHelpers {
   static buildNamedResultPresentation(fallbackTitle, getSubtitle) {
      return {
         getTitle: (row) => row.name || fallbackTitle,
         getSubtitle,
      };
   }
}
