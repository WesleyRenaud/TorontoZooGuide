export function ajaxPost(url, payload) {
   return new Promise((resolve, reject) => {
      $.ajax({
         type: 'POST',
         url,
         contentType: 'application/json',
         dataType: 'json',
         data: JSON.stringify(payload ?? {}),
         success: resolve,
         error: (xhr, status, err) => reject(err || new Error(status)),
      });
   });
}