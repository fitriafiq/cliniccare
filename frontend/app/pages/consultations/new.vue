<template>
	<div class="p-6 max-w-lg mx-auto space-y-4">
		<div class="flex items-center gap-2">
			<UButton to="/consultations" variant="ghost" icon="ph-arrow-left" square />
			<h1 class="text-xl font-semibold">New Consultation</h1>
		</div>

		<UForm :state :validate="validate" class="space-y-4" @submit="onSubmit">
			<UFormField label="Patient name" name="patient_name" required>
				<UInput v-model="state.patient_name" placeholder="John Doe" class="w-full" />
			</UFormField>

			<UFormField label="Diagnoses" name="diagnosis_ids" required>
				<USelectMenu v-model="state.diagnosis_ids" :items="diagnosisItems" value-key="value" multiple
					placeholder="Select diagnoses" class="w-full" />
			</UFormField>

			<UFormField label="Notes" name="notes">
				<UTextarea v-model="state.notes" placeholder="Optional notes" class="w-full" :rows="4" />
			</UFormField>

			<UButton type="submit" label="Save Consultation" :disabled="submitting" :loading="submitting" />
		</UForm>
	</div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const toast = useToast()

const { data: diagnoses } = await useFetch<Diagnosis[]>('/diagnosis/', {
	baseURL: config.public.apiBase,
})

const diagnosisItems = computed(
	() => diagnoses.value?.map((diagnosis) => ({
		label: `${diagnosis.code} — ${diagnosis.description}`,
		value: diagnosis.id
	})) ?? []
)

const state = reactive<ConsultationForm>({
	patient_name: '',
	notes: '',
	diagnosis_ids: [],
})

const submitting = ref(false)

function validate(state: ConsultationForm) {
	const errors = []

	if (!state.patient_name.trim()) {
		errors.push({
			name: 'patient_name',
			message: 'Patient name is required'
		})
	}

	if (state.diagnosis_ids.length === 0) {
		errors.push({
			name: 'diagnosis_ids',
			message: 'Pick at least one diagnosis'
		})
	}

	return errors
}

async function onSubmit() {
	submitting.value = true

	try {
		await $fetch('/consultation/', {
			method: 'POST',
			baseURL: config.public.apiBase,
			body: {
				patient_name: state.patient_name,
				notes: state.notes.trim() || null,
				diagnosis_ids: state.diagnosis_ids,
			},
		})
		toast.add({
			title: 'Consultation saved',
			color: 'success'
		})
		await navigateTo('/consultations')
	} catch (error: any) {
		toast.add({
			title: 'Failed to save consultation',
			description: error?.data?.detail ?? String(error),
			color: 'error'
		})
	} finally {
		submitting.value = false
	}
}
</script>