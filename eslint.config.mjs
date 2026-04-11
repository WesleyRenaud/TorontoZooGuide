export default [
   {
      ignores: [
         '.git/**',
         '.vscode/**',
         '__pycache__/**',
         'images/**',
         'node_modules/**'
      ]
   },
   {
      files: [ 'scripts/**/*.js' ],
      languageOptions: {
         ecmaVersion: 'latest',
         sourceType: 'module'
      },
      rules: {
         'array-bracket-spacing': [ 'error', 'never' ],
         'computed-property-spacing': [ 'error', 'never' ],
         'space-in-parens': [ 'error', 'never' ],
         'no-unused-vars': [ 'error', { args: 'none', caughtErrors: 'none', ignoreRestSiblings: true } ],
         'no-trailing-spaces': [ 'error', { skipBlankLines: false, ignoreComments: false } ]
      }
   }
];
