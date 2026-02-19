function ajaxPost(url, payload) {
   return new Promise((resolve, reject) => {
      $.ajax({
         type: 'POST',
         url,
         contentType: 'application/json',
         dataType: 'json',
         data: JSON.stringify(payload ?? {}),
         success: resolve,
         error: (_xhr, status, err) => reject(err || new Error(status))
      });
   });
}

export function createAnimalsApi() {
   async function getExhibitsInRegion(region) {
      const res = await ajaxPost('/get-exhibits-in-region', { region });
      return res?.exhibits ?? [];
   }

   async function getAnimalsInExhibit(exhibit) {
      const res = await ajaxPost('/get-animals-in-exhibit', { exhibit });
      return res?.animals ?? [];
   }

   async function getAnimalInformation(species) {
      const res = await ajaxPost('/get-animal-information', { species });
      const info = (res?.information && res.information[0]) ? res.information[0] : null;
      return info;
   }

   return {
      getExhibitsInRegion,
      getAnimalsInExhibit,
      getAnimalInformation
   };
}