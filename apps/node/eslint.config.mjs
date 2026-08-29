import js from '@eslint/js'
import eslintConfigPrettier from 'eslint-config-prettier/flat'
import node from 'eslint-plugin-n'
import promise from 'eslint-plugin-promise'
import { defineConfig, globalIgnores } from 'eslint/config'
import globals from 'globals'
import tseslint from 'typescript-eslint'

// ESLint flat config is an ordered list of configuration objects.
// Docs: https://eslint.org/docs/latest/use/configure/configuration-files
const sourceFiles = ['src/**/*.{js,cjs,mjs,jsx,ts,cts,mts,tsx}']

export default defineConfig([
  // Ignore generated and temporary artifacts across all config blocks below.
  // Docs: https://eslint.org/docs/latest/use/configure/ignore#ignore-files
  globalIgnores(['dist/**', 'coverage/**', 'tmp/**']),

  {
    // Common baseline for source code: modern syntax, ESM by default,
    // Node globals, and JSX parsing when the file extension allows it.
    // Docs: https://eslint.org/docs/latest/use/configure/language-options#specify-javascript-options
    name: 'node/source',
    files: sourceFiles,
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: 'module',
      globals: globals.node,
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    linterOptions: {
      // Fail when an eslint-disable comment is no longer needed.
      // Docs: https://eslint.org/docs/latest/use/configure/configuration-files#report-unused-disable-directives
      reportUnusedDisableDirectives: 'error',
    },
  },

  {
    // CommonJS files need their own scope and parsing mode.
    // Docs: https://eslint.org/docs/latest/use/configure/language-options#specify-javascript-options
    name: 'node/commonjs-source',
    files: ['src/**/*.{cjs,cts}'],
    languageOptions: {
      sourceType: 'commonjs',
    },
  },

  {
    // Runtime rules: Node-supported APIs/modules and Promise best practices.
    // `extends` composes presets inside this block.
    // Docs: https://eslint.org/docs/latest/use/configure/configuration-files#extending-configurations
    name: 'node/runtime-rules',
    files: sourceFiles,
    extends: [
      node.configs['flat/recommended-module'],
      promise.configs['flat/recommended'],
    ],
    settings: {
      n: {
        // Extensions eslint-plugin-n tries when validating import resolution.
        // Docs: https://github.com/eslint-community/eslint-plugin-n#eslintconfigjs
        tryExtensions: [
          '.js',
          '.cjs',
          '.mjs',
          '.jsx',
          '.ts',
          '.cts',
          '.mts',
          '.tsx',
          '.json',
          '.node',
        ],
      },
    },
  },

  {
    // Recommended ESLint core rules for plain JavaScript.
    // Docs: https://eslint.org/docs/latest/use/configure/configuration-files#use-predefined-configurations
    name: 'node/javascript-rules',
    files: ['src/**/*.{js,cjs,mjs,jsx}'],
    extends: [js.configs.recommended],
  },

  {
    // TypeScript rules with type information. They are slower, but catch
    // issues that syntax-only linting cannot see.
    // Docs: https://typescript-eslint.io/users/configs/#projects-with-type-checking
    name: 'node/typescript-rules',
    files: ['src/**/*.{ts,cts,mts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommendedTypeChecked,
      tseslint.configs.stylisticTypeChecked,
    ],
    languageOptions: {
      parserOptions: {
        // Use the best matching TSConfig through Project Service, aligning
        // linting with the TypeScript view used by editors.
        // Docs: https://typescript-eslint.io/packages/parser/#projectservice
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      // Enforces `import type` for imports used only as TypeScript types.
      // Docs: https://typescript-eslint.io/rules/consistent-type-imports/
      '@typescript-eslint/consistent-type-imports': 'error',

      // Allows empty functions in this project. Empty functions can be useful
      // for intentional no-op callbacks, but can also hide unfinished code.
      // Docs: https://typescript-eslint.io/rules/no-empty-function/
      '@typescript-eslint/no-empty-function': 'off',

      // Reports unused variables, arguments, and caught errors. Names starting
      // with `_` are treated as intentionally unused by the options below.
      // Docs: https://typescript-eslint.io/rules/no-unused-vars/
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          argsIgnorePattern: '^_',
          caughtErrorsIgnorePattern: '^_',
          ignoreRestSiblings: true,
          varsIgnorePattern: '^_',
        },
      ],

      // Reports declarations used before they are defined, using
      // TypeScript-aware scope analysis.
      // Docs: https://typescript-eslint.io/rules/no-use-before-define/
      '@typescript-eslint/no-use-before-define': 'error',
    },
  },

  // Keep this last: it disables formatting rules that would conflict with
  // Prettier. Formatting checks still run separately via `yarn format:check`.
  // Docs: https://github.com/prettier/eslint-config-prettier#installation
  eslintConfigPrettier,
])
