package models

type ClinicalTrialRequest struct {
	AccessKey int64  `json:"access_key"`
	ClinicalTrial int `json:"clinical_trial"`
}
