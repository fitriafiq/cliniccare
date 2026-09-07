export interface Consultation {
	id: number
	patient_name: string
	notes: string | null
	diagnosis_ids: number[]
	created_at: string
}

export interface ConsultationForm {
	patient_name: string
	notes: string
	diagnosis_ids: number[]
}