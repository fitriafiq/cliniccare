// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  css: ['assets/css/main.css'],
	runtimeConfig: {
		public: {
			apiBase: 'http://localhost:8000',
		},
	},
	modules: [
		'@nuxt/ui',
	],
	ui: {
		colorMode: false,
	},
	icon: {
		clientBundle: {
			scan: true
		}
	},
})
