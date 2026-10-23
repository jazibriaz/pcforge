{{/* Labels on every object. */}}
{{- define "pcforge.labels" -}}
app.kubernetes.io/name: pcforge
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{/* Labels the Service and PDB use to find the pods. Never change these after first deploy:
     a Deployment's selector is immutable. */}}
{{- define "pcforge.selectorLabels" -}}
app: pcforge
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
