<template>
	<div class="p-6 max-w-4xl mx-auto space-y-4">
		<div class="flex items-center justify-between">
			<h1 class="text-xl font-semibold">Consultations</h1>
			<UButton to="/consultations/new" label="New Consultation" icon="ph-plus" />
		</div>

		<UTable :data="consultations ?? []" :columns :loading="status === 'pending'">
			<template #patient_name-cell="{ row }">
				{{ row.original.patient_name }}
			</template>

			<template #diagnosis_ids-cell="{ row }">
				<div class="flex flex-wrap gap-1">
					<UBadge v-for="id in row.original.diagnosis_ids" :key="id" variant="subtle"
						:label="diagnosisLabel(id)" />
				</div>
			</template>

			<template #notes-cell="{ row }">
				<span class="text-muted">{{ row.original.notes || '—' }}</span>
			</template>

			<template #created_at-cell="{ row }">
				{{ formatDate(row.original.created_at) }}
			</template>
		</UTable>
	</div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

const { data: consultations, status } = await useFetch<Consultation[]>('/consultation/', {
	baseURL: config.public.apiBase,
})

const { data: diagnoses } = await useFetch<Diagnosis[]>('/diagnosis/', {
	baseURL: config.public.apiBase,
})

function diagnosisLabel(id: number) {
	return diagnoses.value?.find((d) => d.id === id)?.code ?? `#${id}`
}

function formatDate(value: string) {
	return new Date(value).toLocaleString()
}

const columns = [
	{ accessorKey: 'patient_name', header: 'Patient' },
	{ accessorKey: 'diagnosis_ids', header: 'Diagnoses' },
	{ accessorKey: 'notes', header: 'Notes' },
	{ accessorKey: 'created_at', header: 'Date' },
]
</script>
