export function getLikelihoodPhrase(likelihood) {
   const value = Number(likelihood) || 0;

   if (value >= 95) return 'Very high';
   if (value >= 80) return 'High';
   if (value >= 60) return 'Medium';
   if (value >= 40) return 'Moderate';
   if (value >= 20) return 'Low';

   return 'Very low';
}
